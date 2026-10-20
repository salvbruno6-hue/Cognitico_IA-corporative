"""Governed semantic dependency analysis for ELO requirements.

This module interprets the explicit ``RequirementNode.requirement_dependencies``
contract inside the canonical Reasoning owner. The legacy ``dependencies`` field
keeps its existing generic lineage/provenance meaning and is deliberately not
reinterpreted as a RequirementNode graph edge.

The module does not execute providers, persist edges, create a second relation
engine, or replace ``TaskPlan``. Persistent relation ownership remains with the
existing ELO/Supabase relation surfaces.

The dependency boundary is epistemic and fail-closed: malformed graphs are
invalid, unresolved prerequisites block downstream resolution, and a blocked
requirement is never reclassified as a confirmed gap merely because its
prerequisites are not ready.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from enum import StrEnum
from typing import TYPE_CHECKING, Mapping, Sequence

from .requirement_analysis import (
    ConfidenceBand,
    GapAssessment,
    RequirementClaim,
    RequirementNode,
    RequirementState,
)

if TYPE_CHECKING:
    from .requirement_resolution import (
        RequirementResolutionFlow,
        RequirementResolutionResult,
    )


class RequirementDependencyState(StrEnum):
    READY = "READY"
    BLOCKED = "BLOCKED"


_RESOLVED_DEPENDENCY_STATES = frozenset(
    {
        RequirementState.KNOWN,
        RequirementState.DOCUMENTED,
        RequirementState.RETRIEVED,
        RequirementState.CALCULATED,
    }
)
_DEPENDENCY_REASONING_MARKER = "requirement-dependencies:v1"


@dataclass(frozen=True, slots=True)
class RequirementDependencyStatus:
    requirement_id: str
    state: RequirementState | None
    evidence_ids: tuple[str, ...] = ()
    human_validation_required: bool = False
    automatic_trust_failed: bool = False

    def __post_init__(self) -> None:
        if not self.requirement_id or not self.requirement_id.strip():
            raise ValueError("dependency status requires requirement_id")

    @property
    def resolved(self) -> bool:
        return (
            self.state in _RESOLVED_DEPENDENCY_STATES
            and not self.human_validation_required
            and not self.automatic_trust_failed
        )


@dataclass(frozen=True, slots=True)
class RequirementDependencyValidation:
    invalid_requirement_ids: tuple[str, ...] = ()
    duplicate_requirement_ids: tuple[str, ...] = ()
    duplicate_dependencies: tuple[tuple[str, str], ...] = ()
    unknown_dependencies: tuple[tuple[str, str], ...] = ()
    self_dependencies: tuple[str, ...] = ()
    cycles: tuple[tuple[str, ...], ...] = ()
    topological_order: tuple[str, ...] = ()

    @property
    def valid(self) -> bool:
        return not any(
            (
                self.invalid_requirement_ids,
                self.duplicate_requirement_ids,
                self.duplicate_dependencies,
                self.unknown_dependencies,
                self.self_dependencies,
                self.cycles,
            )
        )


@dataclass(frozen=True, slots=True)
class RequirementDependencyAssessment:
    requirement_id: str
    state: RequirementDependencyState
    direct_dependencies: tuple[str, ...]
    transitive_dependencies: tuple[str, ...]
    statuses: tuple[RequirementDependencyStatus, ...]
    blockers: tuple[RequirementDependencyStatus, ...]
    dependency_claim_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.requirement_id or not self.requirement_id.strip():
            raise ValueError("dependency assessment requires requirement_id")
        if self.state is RequirementDependencyState.READY and self.blockers:
            raise ValueError("READY dependency assessment cannot contain blockers")
        if self.state is RequirementDependencyState.BLOCKED and not self.blockers:
            raise ValueError("BLOCKED dependency assessment requires blockers")

    @property
    def human_validation_required(self) -> bool:
        return any(blocker.human_validation_required for blocker in self.blockers)


@dataclass(frozen=True, slots=True)
class DependencyAwareRequirementResolutionResult:
    """Requirement-resolution result paired with the dependency gate evidence."""

    dependency_assessment: RequirementDependencyAssessment
    resolution: RequirementResolutionResult

    def __post_init__(self) -> None:
        if self.dependency_assessment.requirement_id != self.resolution.requirement_id:
            raise ValueError("dependency and resolution results must belong to one requirement")


class RequirementDependencyGraph:
    """Validate and evaluate typed requirement dependencies deterministically."""

    def __init__(self, nodes: Sequence[RequirementNode]):
        self.nodes = tuple(nodes)
        self._nodes_by_id: dict[str, RequirementNode] = {}
        for node in self.nodes:
            self._nodes_by_id.setdefault(node.requirement_id, node)
        self._adjacency, self.validation = _build_and_validate_graph(self.nodes)

    def _require_valid(self) -> None:
        if not self.validation.valid:
            raise ValueError("requirement dependency graph is invalid")

    def transitive_dependencies(self, requirement_id: str) -> tuple[str, ...]:
        self._require_valid()
        if requirement_id not in self._nodes_by_id:
            raise KeyError(requirement_id)

        collected: set[str] = set()

        def visit(current_id: str) -> None:
            for dependency_id in self._adjacency[current_id]:
                if dependency_id in collected:
                    continue
                visit(dependency_id)
                collected.add(dependency_id)

        visit(requirement_id)
        order_index = {
            item: index for index, item in enumerate(self.validation.topological_order)
        }
        return tuple(sorted(collected, key=order_index.__getitem__))

    def assess(
        self,
        *,
        requirement_id: str,
        assessments: Mapping[str, GapAssessment],
        current_claims: Mapping[str, Sequence[RequirementClaim]] | None = None,
    ) -> RequirementDependencyAssessment:
        self._require_valid()
        if requirement_id not in self._nodes_by_id:
            raise KeyError(requirement_id)

        _validate_assessment_mapping(assessments)
        normalized_current_claims = _validate_current_claim_mapping(current_claims or {})

        direct = self._adjacency[requirement_id]
        transitive = self.transitive_dependencies(requirement_id)
        statuses: list[RequirementDependencyStatus] = []
        supporting_by_dependency: dict[str, tuple[RequirementClaim, ...]] = {}
        assessment_evidence_by_dependency: dict[str, tuple[str, ...]] = {}

        for dependency_id in transitive:
            dependency_assessment = assessments.get(dependency_id)
            if dependency_assessment is None:
                status = RequirementDependencyStatus(
                    requirement_id=dependency_id,
                    state=None,
                )
            else:
                assessment_evidence = _clean_ids(dependency_assessment.evidence_ids)
                assessment_evidence_by_dependency[dependency_id] = assessment_evidence
                supporting: tuple[RequirementClaim, ...] = ()
                supporting_claim_validation_required = False
                supporting_claim_trust_failed = (
                    dependency_assessment.state in _RESOLVED_DEPENDENCY_STATES
                    and not dependency_assessment.human_validation_required
                )
                if (
                    dependency_assessment.state in _RESOLVED_DEPENDENCY_STATES
                    and not dependency_assessment.human_validation_required
                ):
                    candidates = tuple(
                        dict.fromkeys(
                            (
                                *self._nodes_by_id[dependency_id].claims,
                                *normalized_current_claims.get(dependency_id, ()),
                            )
                        )
                    )
                    automatic_candidates = _automatic_claims_for_parameter(
                        requirement_id=dependency_id,
                        parameter=dependency_assessment.parameter,
                        claims=candidates,
                    )
                    automatic_trust_ok = bool(automatic_candidates) and _supporting_claims_pass_automatic_trust(
                        node=self._nodes_by_id[dependency_id],
                        assessment=dependency_assessment,
                        claims=automatic_candidates,
                    )
                    supporting = _supporting_claims(
                        requirement_id=dependency_id,
                        claims=candidates,
                        assessment=dependency_assessment,
                    )
                    supporting_by_dependency[dependency_id] = supporting
                    supporting_claim_validation_required = any(
                        claim.requires_human_validation for claim in supporting
                    )
                    supporting_claim_ids_canonical = all(
                        bool(claim.claim_id.strip())
                        and claim.claim_id == claim.claim_id.strip()
                        for claim in supporting
                    )
                    supporting_claim_trust_failed = (
                        not automatic_trust_ok
                        or not supporting
                        or not supporting_claim_ids_canonical
                    )

                status = RequirementDependencyStatus(
                    requirement_id=dependency_id,
                    state=dependency_assessment.state,
                    evidence_ids=assessment_evidence,
                    human_validation_required=(
                        dependency_assessment.human_validation_required
                        or supporting_claim_validation_required
                    ),
                    automatic_trust_failed=supporting_claim_trust_failed,
                )
            statuses.append(status)

        selected_support_ids = tuple(
            claim.claim_id
            for status in statuses
            if status.resolved
            for claim in supporting_by_dependency.get(status.requirement_id, ())
        )
        duplicate_support_ids = {
            claim_id
            for claim_id, count in Counter(selected_support_ids).items()
            if count > 1
        }
        if duplicate_support_ids:
            statuses = [
                replace(status, automatic_trust_failed=True)
                if status.resolved
                and any(
                    claim.claim_id in duplicate_support_ids
                    for claim in supporting_by_dependency.get(status.requirement_id, ())
                )
                else status
                for status in statuses
            ]

        dependency_claim_ids: list[str] = []
        bound_evidence_ids: list[str] = []
        for status in statuses:
            supporting = supporting_by_dependency.get(status.requirement_id, ())
            if status.resolved:
                dependency_claim_ids.extend(claim.claim_id for claim in supporting)
                bound_evidence_ids.extend(
                    evidence_id
                    for claim in supporting
                    for evidence_id in claim.provenance.evidence_ids
                )
            else:
                # Evidence for a blocker remains useful to explain why the
                # downstream requirement is blocked, but it is never bound
                # into a resolved downstream claim.
                bound_evidence_ids.extend(
                    assessment_evidence_by_dependency.get(status.requirement_id, ())
                )

        blockers = tuple(status for status in statuses if not status.resolved)
        state = (
            RequirementDependencyState.BLOCKED
            if blockers
            else RequirementDependencyState.READY
        )
        return RequirementDependencyAssessment(
            requirement_id=requirement_id,
            state=state,
            direct_dependencies=direct,
            transitive_dependencies=transitive,
            statuses=tuple(statuses),
            blockers=blockers,
            dependency_claim_ids=_clean_ids(dependency_claim_ids),
            evidence_ids=_clean_ids(bound_evidence_ids),
        )

    def ready_requirements(
        self,
        assessments: Mapping[str, GapAssessment],
        current_claims: Mapping[str, Sequence[RequirementClaim]] | None = None,
    ) -> tuple[str, ...]:
        self._require_valid()
        return tuple(
            requirement_id
            for requirement_id in self.validation.topological_order
            if self.assess(
                requirement_id=requirement_id,
                assessments=assessments,
                current_claims=current_claims,
            ).state
            is RequirementDependencyState.READY
        )


def resolve_requirement_with_dependencies(
    *,
    flow: RequirementResolutionFlow,
    graph: RequirementDependencyGraph,
    node: RequirementNode,
    parameter: str,
    prerequisite_assessments: Mapping[str, GapAssessment],
    prerequisite_claims: Mapping[str, Sequence[RequirementClaim]] | None = None,
) -> DependencyAwareRequirementResolutionResult:
    """Gate the existing resolution flow on typed prerequisite readiness.

    ``RequirementResolutionFlow`` continues to own retrieval/rule/calculation/
    inference ordering. This boundary only proves that typed prerequisite edges
    are READY. The typed edge field is cleared on the copy passed to the flow so
    direct callers cannot bypass this gate, while legacy ``dependencies`` lineage
    remains intact.
    """
    _require_runtime_graph_alignment(graph=graph, node=node)
    dependency_assessment = graph.assess(
        requirement_id=node.requirement_id,
        assessments=prerequisite_assessments,
        current_claims=prerequisite_claims,
    )

    from .requirement_resolution import (
        RequirementResolutionResult,
        _audit_scope_context,
    )

    if dependency_assessment.state is RequirementDependencyState.BLOCKED:
        resolution = RequirementResolutionResult(
            requirement_id=node.requirement_id,
            parameter=parameter,
            claims=node.claims,
            attempts=(),
            assessment=blocked_gap_assessment(
                dependency_assessment=dependency_assessment,
                parameter=parameter,
            ),
            scope_context=_audit_scope_context(node.metadata),
        )
    else:
        resolution_node = replace(node, requirement_dependencies=())
        resolution = flow.resolve(node=resolution_node, parameter=parameter)
        resolution = _bind_dependency_context(
            resolution=resolution,
            dependency_assessment=dependency_assessment,
        )

    return DependencyAwareRequirementResolutionResult(
        dependency_assessment=dependency_assessment,
        resolution=resolution,
    )


def blocked_gap_assessment(
    *,
    dependency_assessment: RequirementDependencyAssessment,
    parameter: str,
) -> GapAssessment:
    """Represent prerequisite blocking without turning it into a downstream gap."""
    if dependency_assessment.state is not RequirementDependencyState.BLOCKED:
        raise ValueError("blocked gap assessment requires BLOCKED dependencies")
    if not parameter or not parameter.strip():
        raise ValueError("parameter is required")

    reasons = ["requirement resolution is blocked by unresolved prerequisites"]
    for blocker in dependency_assessment.blockers:
        state = blocker.state.value if blocker.state is not None else "UNASSESSED"
        if blocker.automatic_trust_failed:
            reasons.append(
                f"dependency {blocker.requirement_id} is {state} but its automatic support is not governed/trusted"
            )
        elif blocker.human_validation_required:
            reasons.append(
                f"dependency {blocker.requirement_id} is {state} with pending human validation"
            )
        else:
            reasons.append(f"dependency {blocker.requirement_id} is {state}")
    return GapAssessment(
        requirement_id=dependency_assessment.requirement_id,
        parameter=parameter,
        state=RequirementState.BLOCKED,
        reasons=tuple(reasons),
        evidence_ids=dependency_assessment.evidence_ids,
        confidence=ConfidenceBand.UNVERIFIED,
        human_validation_required=dependency_assessment.human_validation_required,
    )


def audit_requirement_dependency_graph(
    graph: RequirementDependencyGraph,
) -> Mapping[str, object]:
    """Return bounded graph-validation evidence, including detected cycles."""
    validation = graph.validation
    return {
        "valid": validation.valid,
        "invalid_requirement_ids": validation.invalid_requirement_ids,
        "duplicate_requirement_ids": validation.duplicate_requirement_ids,
        "duplicate_dependencies": validation.duplicate_dependencies,
        "unknown_dependencies": validation.unknown_dependencies,
        "self_dependencies": validation.self_dependencies,
        "cycles": validation.cycles,
        "topological_order": validation.topological_order,
        "adjacency": tuple(
            (requirement_id, graph._adjacency[requirement_id])
            for requirement_id in sorted(graph._adjacency)
        ),
    }


def audit_requirement_dependency_assessment(
    assessment: RequirementDependencyAssessment,
) -> Mapping[str, object]:
    """Return an audit-safe dependency trace without arbitrary metadata."""
    return {
        "requirement_id": assessment.requirement_id,
        "state": assessment.state.value,
        "direct_dependencies": assessment.direct_dependencies,
        "transitive_dependencies": assessment.transitive_dependencies,
        "statuses": tuple(
            {
                "requirement_id": status.requirement_id,
                "state": status.state.value if status.state is not None else "UNASSESSED",
                "evidence_ids": status.evidence_ids,
                "human_validation_required": status.human_validation_required,
                "automatic_trust_failed": status.automatic_trust_failed,
            }
            for status in assessment.statuses
        ),
        "blockers": tuple(blocker.requirement_id for blocker in assessment.blockers),
        "dependency_claim_ids": assessment.dependency_claim_ids,
        "evidence_ids": assessment.evidence_ids,
    }


def audit_dependency_aware_resolution(
    result: DependencyAwareRequirementResolutionResult,
) -> Mapping[str, object]:
    """Combine bounded dependency and canonical resolution audits."""
    from .requirement_resolution import audit_requirement_resolution

    return {
        "dependencies": audit_requirement_dependency_assessment(
            result.dependency_assessment
        ),
        "resolution": audit_requirement_resolution(result.resolution),
    }


def _bind_dependency_context(
    *,
    resolution: RequirementResolutionResult,
    dependency_assessment: RequirementDependencyAssessment,
) -> RequirementResolutionResult:
    if not dependency_assessment.transitive_dependencies:
        return resolution

    final_is_automatic = resolution.assessment.state in _RESOLVED_DEPENDENCY_STATES
    assessment_evidence = set(_clean_ids(resolution.assessment.evidence_ids))
    bound_claims = tuple(
        _bind_claim_dependencies(
            claim=claim,
            parameter=resolution.parameter,
            dependency_assessment=dependency_assessment,
        )
        if _claim_supports_final_assessment(
            claim=claim,
            parameter=resolution.parameter,
            final_state=resolution.assessment.state,
            assessment_evidence=assessment_evidence,
        )
        else claim
        for claim in resolution.claims
    )

    bound_assessment = (
        replace(
            resolution.assessment,
            evidence_ids=_clean_ids(
                (
                    *resolution.assessment.evidence_ids,
                    *dependency_assessment.evidence_ids,
                )
            ),
        )
        if final_is_automatic
        else resolution.assessment
    )

    retrieval_resolution = resolution.retrieval_resolution
    if retrieval_resolution is not None and retrieval_resolution.retrieved_claim is not None:
        retrieved_claim = retrieval_resolution.retrieved_claim
        retrieved_positions = tuple(
            index
            for index, claim in enumerate(resolution.claims)
            if claim is retrieved_claim
        )
        if len(retrieved_positions) != 1:
            raise ValueError(
                "retrieval resolution claim must appear exactly once in canonical resolution claims"
            )
        retrieval_resolution = replace(
            retrieval_resolution,
            retrieved_claim=bound_claims[retrieved_positions[0]],
        )

    return replace(
        resolution,
        claims=bound_claims,
        assessment=bound_assessment,
        retrieval_resolution=retrieval_resolution,
    )


def _claim_supports_final_assessment(
    *,
    claim: RequirementClaim,
    parameter: str,
    final_state: RequirementState,
    assessment_evidence: set[str],
) -> bool:
    if final_state not in _RESOLVED_DEPENDENCY_STATES:
        return False
    if claim.predicate != parameter or claim.state is not final_state:
        return False
    claim_evidence = set(_clean_ids(claim.provenance.evidence_ids))
    if not assessment_evidence:
        return True
    if _is_evidence_free_documented_claim(claim):
        return True
    return bool(claim_evidence.intersection(assessment_evidence))


def _bind_claim_dependencies(
    *,
    claim: RequirementClaim,
    parameter: str,
    dependency_assessment: RequirementDependencyAssessment,
) -> RequirementClaim:
    if claim.predicate != parameter:
        return claim

    dependencies = _clean_ids(
        (
            *claim.dependencies,
            *dependency_assessment.transitive_dependencies,
            *dependency_assessment.dependency_claim_ids,
        )
    )
    evidence_ids = _clean_ids(
        (*claim.provenance.evidence_ids, *dependency_assessment.evidence_ids)
    )
    reasoning_parts = tuple(
        part.strip()
        for part in claim.provenance.reasoning_method.split("|")
        if part.strip()
    )
    reasoning_method = (
        claim.provenance.reasoning_method
        if _DEPENDENCY_REASONING_MARKER in reasoning_parts
        else f"{claim.provenance.reasoning_method}|{_DEPENDENCY_REASONING_MARKER}"
    )
    return replace(
        claim,
        dependencies=dependencies,
        provenance=replace(
            claim.provenance,
            reasoning_method=reasoning_method,
            evidence_ids=evidence_ids,
        ),
    )


def _require_runtime_graph_alignment(
    *,
    graph: RequirementDependencyGraph,
    node: RequirementNode,
) -> None:
    graph._require_valid()
    if node.requirement_id not in graph._nodes_by_id:
        raise KeyError(node.requirement_id)

    raw_edges = tuple(str(value).strip() for value in node.requirement_dependencies)
    if any(not edge for edge in raw_edges):
        raise ValueError("runtime requirement dependencies contain a blank identifier")
    if len(raw_edges) != len(set(raw_edges)):
        raise ValueError("runtime requirement dependencies contain duplicate edges")
    runtime_edges = tuple(sorted(raw_edges))
    if runtime_edges != graph._adjacency[node.requirement_id]:
        raise ValueError("runtime requirement dependencies do not match dependency graph")


def _validate_assessment_mapping(assessments: Mapping[str, GapAssessment]) -> None:
    for requirement_id, assessment in assessments.items():
        if assessment.requirement_id != requirement_id:
            raise ValueError(
                "dependency assessment key does not match embedded requirement_id"
            )


def _validate_current_claim_mapping(
    current_claims: Mapping[str, Sequence[RequirementClaim]],
) -> Mapping[str, tuple[RequirementClaim, ...]]:
    normalized: dict[str, tuple[RequirementClaim, ...]] = {}
    for requirement_id, claims in current_claims.items():
        materialized = tuple(claims)
        if any(claim.requirement_id != requirement_id for claim in materialized):
            raise ValueError(
                "prerequisite claim key does not match embedded requirement_id"
            )
        normalized[requirement_id] = materialized
    return normalized


def _clean_ids(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(
        dict.fromkeys(
            cleaned for value in values if (cleaned := str(value).strip())
        )
    )


def _is_evidence_free_documented_claim(claim: RequirementClaim) -> bool:
    return (
        claim.state is RequirementState.DOCUMENTED
        and not _clean_ids(claim.provenance.evidence_ids)
    )


def _automatic_claims_for_parameter(
    *,
    requirement_id: str,
    parameter: str,
    claims: Sequence[RequirementClaim],
) -> tuple[RequirementClaim, ...]:
    return tuple(
        sorted(
            (
                claim
                for claim in claims
                if claim.requirement_id == requirement_id
                and claim.predicate == parameter
                and claim.state in _RESOLVED_DEPENDENCY_STATES
            ),
            key=lambda claim: claim.claim_id,
        )
    )


def _supporting_claims(
    *,
    requirement_id: str,
    claims: Sequence[RequirementClaim],
    assessment: GapAssessment,
) -> tuple[RequirementClaim, ...]:
    evidence = set(_clean_ids(assessment.evidence_ids))
    return tuple(
        sorted(
            (
                claim
                for claim in claims
                if claim.requirement_id == requirement_id
                and claim.predicate == assessment.parameter
                and claim.state is assessment.state
                and (
                    not evidence
                    or _is_evidence_free_documented_claim(claim)
                    or bool(
                        evidence.intersection(
                            _clean_ids(claim.provenance.evidence_ids)
                        )
                    )
                )
            ),
            key=lambda claim: claim.claim_id,
        )
    )


def _supporting_claims_pass_automatic_trust(
    *,
    node: RequirementNode,
    assessment: GapAssessment,
    claims: Sequence[RequirementClaim],
) -> bool:
    """Reuse the canonical resolver trust boundary for dependency support.

    A dependency node may legitimately omit ``entity`` because it is not being
    resolved here. In that case the supporting claim's own subject becomes the
    temporary target solely for canonical trust validation. This does not infer
    cross-entity applicability: if multiple selected claims disagree on subject,
    the canonical validator rejects the set against that target.
    """
    materialized = tuple(claims)
    if not materialized:
        return True

    from .requirement_resolution import _validate_preloaded_usable_claims

    validation_node = node
    if not node.entity or not node.entity.strip():
        validation_node = replace(node, entity=materialized[0].subject)

    try:
        conflict = _validate_preloaded_usable_claims(
            node=validation_node,
            parameter=assessment.parameter,
            claims=materialized,
        )
    except ValueError:
        return False
    return conflict is None


def _build_and_validate_graph(
    nodes: Sequence[RequirementNode],
) -> tuple[dict[str, tuple[str, ...]], RequirementDependencyValidation]:
    invalid_requirement_ids = tuple(
        sorted(
            set(
                node.requirement_id
                for node in nodes
                if (
                    not node.requirement_id.strip()
                    or node.requirement_id != node.requirement_id.strip()
                )
            )
        )
    )
    id_counts = Counter(node.requirement_id for node in nodes)
    duplicate_requirement_ids = tuple(
        sorted(
            requirement_id
            for requirement_id, count in id_counts.items()
            if count > 1
        )
    )

    unique_nodes: dict[str, RequirementNode] = {}
    for node in nodes:
        unique_nodes.setdefault(node.requirement_id, node)
    known_ids = set(unique_nodes)

    duplicate_dependencies: set[tuple[str, str]] = set()
    unknown_dependencies: set[tuple[str, str]] = set()
    self_dependencies: set[str] = set()
    adjacency: dict[str, tuple[str, ...]] = {}

    for requirement_id, node in unique_nodes.items():
        normalized = tuple(
            str(value).strip() for value in node.requirement_dependencies
        )
        dependency_counts = Counter(normalized)
        duplicate_dependencies.update(
            (requirement_id, dependency_id)
            for dependency_id, count in dependency_counts.items()
            if dependency_id and count > 1
        )
        accepted: list[str] = []
        for dependency_id in normalized:
            if not dependency_id:
                unknown_dependencies.add((requirement_id, dependency_id))
                continue
            accepted.append(dependency_id)
            if dependency_id == requirement_id:
                self_dependencies.add(requirement_id)
            elif dependency_id not in known_ids:
                unknown_dependencies.add((requirement_id, dependency_id))
        adjacency[requirement_id] = tuple(sorted(set(accepted)))

    cycles = _find_cycles(adjacency=adjacency, known_ids=known_ids)
    invalid = any(
        (
            invalid_requirement_ids,
            duplicate_requirement_ids,
            duplicate_dependencies,
            unknown_dependencies,
            self_dependencies,
            cycles,
        )
    )
    topological_order = () if invalid else _topological_order(adjacency)
    validation = RequirementDependencyValidation(
        invalid_requirement_ids=invalid_requirement_ids,
        duplicate_requirement_ids=duplicate_requirement_ids,
        duplicate_dependencies=tuple(sorted(duplicate_dependencies)),
        unknown_dependencies=tuple(sorted(unknown_dependencies)),
        self_dependencies=tuple(sorted(self_dependencies)),
        cycles=cycles,
        topological_order=topological_order,
    )
    return adjacency, validation


def _find_cycles(
    *,
    adjacency: Mapping[str, Sequence[str]],
    known_ids: set[str],
) -> tuple[tuple[str, ...], ...]:
    state: dict[str, int] = {requirement_id: 0 for requirement_id in known_ids}
    stack: list[str] = []
    position: dict[str, int] = {}
    cycles: set[tuple[str, ...]] = set()

    def visit(requirement_id: str) -> None:
        state[requirement_id] = 1
        position[requirement_id] = len(stack)
        stack.append(requirement_id)
        for dependency_id in adjacency.get(requirement_id, ()):
            if dependency_id not in known_ids or dependency_id == requirement_id:
                continue
            if state[dependency_id] == 0:
                visit(dependency_id)
            elif state[dependency_id] == 1:
                start = position[dependency_id]
                cycles.add(_canonical_cycle(tuple(stack[start:])))
        stack.pop()
        position.pop(requirement_id, None)
        state[requirement_id] = 2

    for requirement_id in sorted(known_ids):
        if state[requirement_id] == 0:
            visit(requirement_id)
    return tuple(sorted(cycles))


def _canonical_cycle(nodes: tuple[str, ...]) -> tuple[str, ...]:
    if not nodes:
        return ()
    rotations = tuple(nodes[index:] + nodes[:index] for index in range(len(nodes)))
    canonical = min(rotations)
    return (*canonical, canonical[0])


def _topological_order(adjacency: Mapping[str, Sequence[str]]) -> tuple[str, ...]:
    ordered: list[str] = []
    visited: set[str] = set()

    def visit(requirement_id: str) -> None:
        if requirement_id in visited:
            return
        for dependency_id in adjacency.get(requirement_id, ()):
            visit(dependency_id)
        visited.add(requirement_id)
        ordered.append(requirement_id)

    for requirement_id in sorted(adjacency):
        visit(requirement_id)
    return tuple(ordered)