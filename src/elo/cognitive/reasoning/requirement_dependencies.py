"""Governed semantic dependency analysis for ELO requirements.

This module interprets ``RequirementNode.dependencies`` inside the canonical
Reasoning owner. It does not execute providers, persist edges, create a second
relation engine, or replace ``TaskPlan``. Persistent relation ownership remains
with the existing ELO/Supabase relation surfaces.

The dependency boundary is epistemic and fail-closed: malformed graphs are
invalid, unresolved prerequisites block downstream resolution, and a blocked
requirement is never reclassified as a confirmed gap merely because its
prerequisites are not ready.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping, Sequence

from .requirement_analysis import (
    ConfidenceBand,
    GapAssessment,
    RequirementClaim,
    RequirementNode,
    RequirementState,
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


@dataclass(frozen=True, slots=True)
class RequirementDependencyStatus:
    requirement_id: str
    state: RequirementState | None
    evidence_ids: tuple[str, ...] = ()
    human_validation_required: bool = False

    def __post_init__(self) -> None:
        if not self.requirement_id or not self.requirement_id.strip():
            raise ValueError("dependency status requires requirement_id")

    @property
    def resolved(self) -> bool:
        return self.state in _RESOLVED_DEPENDENCY_STATES


@dataclass(frozen=True, slots=True)
class RequirementDependencyValidation:
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


class RequirementDependencyGraph:
    """Validate and evaluate semantic requirement dependencies deterministically."""

    def __init__(self, nodes: Sequence[RequirementNode]):
        self.nodes = tuple(nodes)
        self.validation = _validate_graph(self.nodes)
        self._nodes_by_id: dict[str, RequirementNode] = {}
        for node in self.nodes:
            self._nodes_by_id.setdefault(node.requirement_id, node)

    def _require_valid(self) -> None:
        if not self.validation.valid:
            raise ValueError("requirement dependency graph is invalid")

    def transitive_dependencies(self, requirement_id: str) -> tuple[str, ...]:
        self._require_valid()
        if requirement_id not in self._nodes_by_id:
            raise KeyError(requirement_id)

        collected: set[str] = set()

        def visit(current_id: str) -> None:
            node = self._nodes_by_id[current_id]
            for dependency_id in sorted(set(node.dependencies)):
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
    ) -> RequirementDependencyAssessment:
        self._require_valid()
        if requirement_id not in self._nodes_by_id:
            raise KeyError(requirement_id)

        node = self._nodes_by_id[requirement_id]
        direct = tuple(sorted(set(node.dependencies)))
        transitive = self.transitive_dependencies(requirement_id)
        statuses: list[RequirementDependencyStatus] = []
        dependency_claim_ids: list[str] = []
        evidence_ids: list[str] = []

        for dependency_id in transitive:
            dependency_assessment = assessments.get(dependency_id)
            if dependency_assessment is None:
                status = RequirementDependencyStatus(
                    requirement_id=dependency_id,
                    state=None,
                )
            else:
                cleaned_evidence = _clean_ids(dependency_assessment.evidence_ids)
                status = RequirementDependencyStatus(
                    requirement_id=dependency_id,
                    state=dependency_assessment.state,
                    evidence_ids=cleaned_evidence,
                    human_validation_required=(
                        dependency_assessment.human_validation_required
                    ),
                )
                evidence_ids.extend(cleaned_evidence)
                if status.resolved:
                    dependency_claim_ids.extend(
                        _supporting_claim_ids(
                            node=self._nodes_by_id[dependency_id],
                            assessment=dependency_assessment,
                        )
                    )
            statuses.append(status)

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
            evidence_ids=_clean_ids(evidence_ids),
        )

    def ready_requirements(
        self,
        assessments: Mapping[str, GapAssessment],
    ) -> tuple[str, ...]:
        self._require_valid()
        return tuple(
            requirement_id
            for requirement_id in self.validation.topological_order
            if self.assess(
                requirement_id=requirement_id,
                assessments=assessments,
            ).state
            is RequirementDependencyState.READY
        )


def blocked_gap_assessment(
    *,
    dependency_assessment: RequirementDependencyAssessment,
    parameter: str,
) -> GapAssessment:
    """Represent dependency blocking without turning it into a downstream gap."""
    if dependency_assessment.state is not RequirementDependencyState.BLOCKED:
        raise ValueError("blocked gap assessment requires BLOCKED dependencies")
    if not parameter or not parameter.strip():
        raise ValueError("parameter is required")

    reasons = ["requirement resolution is blocked by unresolved prerequisites"]
    reasons.extend(
        f"dependency {blocker.requirement_id} is "
        f"{blocker.state.value if blocker.state is not None else 'UNASSESSED'}"
        for blocker in dependency_assessment.blockers
    )
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
        "duplicate_requirement_ids": validation.duplicate_requirement_ids,
        "duplicate_dependencies": validation.duplicate_dependencies,
        "unknown_dependencies": validation.unknown_dependencies,
        "self_dependencies": validation.self_dependencies,
        "cycles": validation.cycles,
        "topological_order": validation.topological_order,
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
            }
            for status in assessment.statuses
        ),
        "blockers": tuple(blocker.requirement_id for blocker in assessment.blockers),
        "dependency_claim_ids": assessment.dependency_claim_ids,
        "evidence_ids": assessment.evidence_ids,
    }


def _clean_ids(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(
        dict.fromkeys(
            cleaned for value in values if (cleaned := str(value).strip())
        )
    )


def _supporting_claim_ids(
    *,
    node: RequirementNode,
    assessment: GapAssessment,
) -> tuple[str, ...]:
    evidence = set(_clean_ids(assessment.evidence_ids))
    candidates = tuple(
        claim
        for claim in node.claims
        if claim.predicate == assessment.parameter
        and claim.state is assessment.state
        and (
            not evidence
            or bool(evidence.intersection(_clean_ids(claim.provenance.evidence_ids)))
        )
    )
    return tuple(sorted(claim.claim_id for claim in candidates))


def _validate_graph(nodes: Sequence[RequirementNode]) -> RequirementDependencyValidation:
    ids = [node.requirement_id for node in nodes]
    duplicate_requirement_ids = tuple(
        sorted({requirement_id for requirement_id in ids if ids.count(requirement_id) > 1})
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
        dependencies = tuple(str(value).strip() for value in node.dependencies)
        seen: set[str] = set()
        normalized: list[str] = []
        for dependency_id in dependencies:
            if not dependency_id:
                unknown_dependencies.add((requirement_id, dependency_id))
                continue
            if dependency_id in seen:
                duplicate_dependencies.add((requirement_id, dependency_id))
            seen.add(dependency_id)
            normalized.append(dependency_id)
            if dependency_id == requirement_id:
                self_dependencies.add(requirement_id)
            elif dependency_id not in known_ids:
                unknown_dependencies.add((requirement_id, dependency_id))
        adjacency[requirement_id] = tuple(sorted(set(normalized)))

    cycles = _find_cycles(adjacency=adjacency, known_ids=known_ids)
    invalid = any(
        (
            duplicate_requirement_ids,
            duplicate_dependencies,
            unknown_dependencies,
            self_dependencies,
            cycles,
        )
    )
    topological_order = () if invalid else _topological_order(adjacency)
    return RequirementDependencyValidation(
        duplicate_requirement_ids=duplicate_requirement_ids,
        duplicate_dependencies=tuple(sorted(duplicate_dependencies)),
        unknown_dependencies=tuple(sorted(unknown_dependencies)),
        self_dependencies=tuple(sorted(self_dependencies)),
        cycles=cycles,
        topological_order=topological_order,
    )


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
