"""Governed requirement-resolution subflow for ELO Reasoning.

This module coordinates one requirement parameter through the canonical
resolution attempts already modeled by :mod:`requirement_analysis`. It is not a
second cognitive execution loop and performs no provider I/O itself. External
owners remain responsible for retrieval, rules, calculations and controlled
inference; this module only fixes ordering, validates returned evidence, applies
semantic matching to retrieval candidates and decides when gap assessment is
allowed to advance.

The epistemic boundary is fail-closed: a missing provider is not an attempted
resolution path, incompatible claims are rejected, inference never becomes an
automatic fact, unresolved retrieval evidence cannot be erased by later failed
attempts, structured claims cannot cross entity boundaries without explicit
applicability evidence, preloaded automatic claims are revalidated before any
short circuit, and audit output contains only explicit evidence/status data.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Protocol, Sequence

from .requirement_analysis import (
    ConfidenceBand,
    GapAssessment,
    RequirementClaim,
    RequirementNode,
    RequirementSourceType,
    RequirementState,
    ResolutionAttempt,
    ResolutionAttemptKind,
    ResolutionAttemptStatus,
    assess_parameter_gap,
)
from .semantic_matching import (
    SemanticResolution,
    SemanticResolutionState,
    audit_semantic_resolution,
    normalize_semantic_identifier,
    normalize_semantic_value,
    resolve_requirement_parameter,
)


_CANONICAL_ORDER = (
    ResolutionAttemptKind.RETRIEVAL,
    ResolutionAttemptKind.RULE,
    ResolutionAttemptKind.CALCULATION,
    ResolutionAttemptKind.INFERENCE,
)
_VALIDATION_OK = frozenset({"VALIDATED", "APPROVED", "CONFIRMED"})
_AUTOMATIC_STATES = frozenset(
    {
        RequirementState.KNOWN,
        RequirementState.DOCUMENTED,
        RequirementState.RETRIEVED,
        RequirementState.CALCULATED,
    }
)
_TERMINAL_AUTOMATIC_STATES = _AUTOMATIC_STATES | {RequirementState.CONFLICT}


@dataclass(frozen=True, slots=True)
class ResolutionStepResult:
    """Evidence returned by one external resolution provider.

    ``claims`` are structured outputs owned by the provider. The orchestrator
    validates them before they can affect the requirement. ``evidence_ids`` are
    evidence of the attempt itself and may be empty for a genuine NOT_FOUND
    result. No arbitrary metadata or private reasoning channel is accepted.
    """

    source_reference: str
    claims: tuple[RequirementClaim, ...] = ()
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.source_reference or not self.source_reference.strip():
            raise ValueError("resolution step requires a nonblank source_reference")


class RequirementResolutionProvider(Protocol):
    """Provider contract used by the deterministic requirement subflow."""

    kind: ResolutionAttemptKind

    def resolve(
        self,
        node: RequirementNode,
        parameter: str,
        claims: Sequence[RequirementClaim],
    ) -> ResolutionStepResult: ...


@dataclass(frozen=True, slots=True)
class SemanticRetrievalPolicy:
    """Governed semantic inputs supplied by the caller for retrieval matching."""

    aliases: Mapping[str, Sequence[str]] = field(default_factory=dict)
    entity_aliases: Mapping[str, Sequence[str]] = field(default_factory=dict)
    applicability_evidence: Mapping[str, Sequence[str]] = field(default_factory=dict)
    entity_applicability_evidence: Mapping[str, Sequence[str]] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RequirementResolutionResult:
    requirement_id: str
    parameter: str
    claims: tuple[RequirementClaim, ...]
    attempts: tuple[ResolutionAttempt, ...]
    assessment: GapAssessment
    retrieval_resolution: SemanticResolution | None = None

    def __post_init__(self) -> None:
        if not self.requirement_id or not self.requirement_id.strip():
            raise ValueError("requirement resolution requires requirement_id")
        if not self.parameter or not self.parameter.strip():
            raise ValueError("requirement resolution requires parameter")
        if self.assessment.requirement_id != self.requirement_id:
            raise ValueError("assessment must belong to the resolved requirement")
        if self.assessment.parameter != self.parameter:
            raise ValueError("assessment must belong to the resolved parameter")

    @property
    def executed_order(self) -> tuple[ResolutionAttemptKind, ...]:
        return tuple(attempt.kind for attempt in self.attempts)


@dataclass(slots=True)
class RequirementResolutionFlow:
    """Run configured requirement-resolution providers in canonical order.

    Providers are optional by construction. An absent provider is skipped and
    therefore cannot satisfy the four-attempt precondition for ``GAP_CONFIRMED``.
    The mapping insertion order never affects execution order. Structured-stage
    claims must belong to the target entity by identifier-safe equality or carry
    explicit per-claim applicability evidence supplied by the caller.
    """

    providers: Mapping[ResolutionAttemptKind, RequirementResolutionProvider]
    semantic_policy: SemanticRetrievalPolicy = field(default_factory=SemanticRetrievalPolicy)
    structured_entity_applicability_evidence: Mapping[str, Sequence[str]] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        unsupported = set(self.providers) - set(_CANONICAL_ORDER)
        if unsupported:
            raise ValueError(f"unsupported resolution provider kinds: {unsupported!r}")
        for kind, provider in self.providers.items():
            if provider.kind is not kind:
                raise ValueError(
                    f"resolution provider key {kind.value} does not match provider kind "
                    f"{provider.kind.value}"
                )

    def resolve(self, *, node: RequirementNode, parameter: str) -> RequirementResolutionResult:
        if not parameter or not parameter.strip():
            raise ValueError("parameter is required")

        current_claims = list(node.claims)
        attempts: list[ResolutionAttempt] = []
        retrieval_resolution: SemanticResolution | None = None

        preloaded_conflict = _validate_preloaded_usable_claims(
            node=node,
            parameter=parameter,
            claims=current_claims,
        )
        if preloaded_conflict is not None:
            return RequirementResolutionResult(
                requirement_id=node.requirement_id,
                parameter=parameter,
                claims=tuple(current_claims),
                attempts=(),
                assessment=preloaded_conflict,
            )

        assessment = assess_parameter_gap(
            requirement_id=node.requirement_id,
            parameter=parameter,
            claims=current_claims,
            attempts=attempts,
        )
        if assessment.state in _TERMINAL_AUTOMATIC_STATES:
            return RequirementResolutionResult(
                requirement_id=node.requirement_id,
                parameter=parameter,
                claims=tuple(current_claims),
                attempts=(),
                assessment=assessment,
            )

        for kind in _CANONICAL_ORDER:
            provider = self.providers.get(kind)
            if provider is None:
                continue

            step = provider.resolve(node, parameter, tuple(current_claims))
            if not isinstance(step, ResolutionStepResult):
                raise TypeError(
                    f"{kind.value} provider must return ResolutionStepResult"
                )

            if kind is ResolutionAttemptKind.RETRIEVAL:
                retrieval_resolution = resolve_requirement_parameter(
                    node=node,
                    parameter=parameter,
                    candidates=step.claims,
                    aliases=self.semantic_policy.aliases,
                    entity_aliases=self.semantic_policy.entity_aliases,
                    applicability_evidence=self.semantic_policy.applicability_evidence,
                    entity_applicability_evidence=(
                        self.semantic_policy.entity_applicability_evidence
                    ),
                )
                status, evidence_ids = _retrieval_attempt_outcome(
                    step=step,
                    resolution=retrieval_resolution,
                )
                if retrieval_resolution.retrieved_claim is not None:
                    current_claims.append(retrieval_resolution.retrieved_claim)
            else:
                entity_evidence_ids = _validate_stage_claims(
                    kind=kind,
                    node=node,
                    parameter=parameter,
                    claims=step.claims,
                    entity_applicability_evidence=(
                        self.structured_entity_applicability_evidence
                    ),
                )
                current_claims.extend(step.claims)
                status, evidence_ids = _structured_attempt_outcome(
                    kind=kind,
                    step=step,
                    entity_applicability_evidence_ids=entity_evidence_ids,
                )

            attempt = ResolutionAttempt(
                kind=kind,
                status=status,
                source_reference=step.source_reference.strip(),
                evidence_ids=evidence_ids,
                note=_attempt_note(kind=kind, status=status),
            )
            attempts.append(attempt)

            assessment = assess_parameter_gap(
                requirement_id=node.requirement_id,
                parameter=parameter,
                claims=current_claims,
                attempts=attempts,
            )
            if assessment.state in _TERMINAL_AUTOMATIC_STATES:
                break

        assessment = assess_parameter_gap(
            requirement_id=node.requirement_id,
            parameter=parameter,
            claims=current_claims,
            attempts=attempts,
        )
        assessment = _preserve_unresolved_retrieval(
            assessment=assessment,
            retrieval_resolution=retrieval_resolution,
            attempts=attempts,
        )
        return RequirementResolutionResult(
            requirement_id=node.requirement_id,
            parameter=parameter,
            claims=tuple(current_claims),
            attempts=tuple(attempts),
            assessment=assessment,
            retrieval_resolution=retrieval_resolution,
        )


def _clean_evidence_ids(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(
        dict.fromkeys(
            cleaned
            for value in values
            if (cleaned := str(value).strip())
        )
    )


def _claim_evidence_ids(claims: Sequence[RequirementClaim]) -> tuple[str, ...]:
    return _clean_evidence_ids(
        tuple(
            evidence_id
            for claim in claims
            for evidence_id in claim.provenance.evidence_ids
        )
    )


def _is_validated(claim: RequirementClaim) -> bool:
    return claim.provenance.validation_status.strip().upper() in _VALIDATION_OK


def _require_nonblank_claim_value(claim: RequirementClaim, *, context: str) -> None:
    if not str(claim.value).strip():
        raise ValueError(f"{context} claim requires a nonblank value")


def _require_governed_evidence(claim: RequirementClaim, *, context: str) -> None:
    if not claim.provenance.source_reference or not claim.provenance.source_reference.strip():
        raise ValueError(f"{context} claim requires source_reference")
    if not _clean_evidence_ids(claim.provenance.evidence_ids):
        raise ValueError(f"{context} claim requires nonblank evidence_ids")


def _require_preloaded_entity_identity(
    *,
    node: RequirementNode,
    claim: RequirementClaim,
) -> None:
    target_entity = node.entity.strip() if node.entity and node.entity.strip() else None
    if target_entity is None:
        raise ValueError(
            "PRELOADED automatic claim requires a target entity before it can short-circuit"
        )
    if normalize_semantic_identifier(target_entity) != normalize_semantic_identifier(
        claim.subject
    ):
        raise ValueError("PRELOADED automatic claim entity does not match target entity")


def _validate_preloaded_usable_claims(
    *,
    node: RequirementNode,
    parameter: str,
    claims: Sequence[RequirementClaim],
) -> GapAssessment | None:
    """Revalidate initial usable claims before they can short-circuit the flow."""
    usable = tuple(
        claim
        for claim in claims
        if claim.predicate == parameter and claim.state in _AUTOMATIC_STATES
    )
    for claim in usable:
        if not claim.subject or not claim.subject.strip():
            raise ValueError("PRELOADED automatic claim requires a nonblank subject")
        _require_preloaded_entity_identity(node=node, claim=claim)
        _require_nonblank_claim_value(claim, context="PRELOADED")
        if not claim.provenance.source_reference or not claim.provenance.source_reference.strip():
            raise ValueError("PRELOADED automatic claim requires source_reference")
        if claim.requires_human_validation:
            raise ValueError(
                "PRELOADED automatic claim cannot short-circuit with a pending human gate"
            )

        if claim.state is RequirementState.DOCUMENTED:
            if claim.provenance.source_type is not RequirementSourceType.DOCUMENT:
                raise ValueError("PRELOADED DOCUMENTED claim requires DOCUMENT provenance")
            # Explicit document extraction is itself governed evidence and may
            # legitimately carry validation_status=EXTRACTED without a separate
            # evidence identifier; its source_reference remains mandatory.
            continue

        _require_governed_evidence(claim, context="PRELOADED")
        if not _is_validated(claim):
            raise ValueError(
                "PRELOADED automatic claim requires governed validation"
            )
        if claim.provenance.source_type is RequirementSourceType.LLM_INFERENCE:
            raise ValueError(
                "PRELOADED automatic claim cannot use LLM_INFERENCE provenance"
            )
        if (
            claim.state is RequirementState.CALCULATED
            and claim.provenance.source_type is not RequirementSourceType.CALCULATION
        ):
            raise ValueError(
                "PRELOADED CALCULATED claim requires CALCULATION provenance"
            )

    normalized_values = {
        normalize_semantic_value(claim.value)
        for claim in usable
        if str(claim.value).strip()
    }
    if len(normalized_values) > 1:
        return GapAssessment(
            requirement_id=node.requirement_id,
            parameter=parameter,
            state=RequirementState.CONFLICT,
            reasons=("preloaded governed claims disagree on the parameter value",),
            evidence_ids=_claim_evidence_ids(usable),
            confidence=ConfidenceBand.LOW,
            human_validation_required=True,
        )
    return None


def _validate_structured_entity(
    *,
    kind: ResolutionAttemptKind,
    node: RequirementNode,
    claim: RequirementClaim,
    entity_applicability_evidence: Mapping[str, Sequence[str]],
) -> tuple[str, ...]:
    explicit = _clean_evidence_ids(
        entity_applicability_evidence.get(claim.claim_id, ())
    )
    target_entity = node.entity.strip() if node.entity and node.entity.strip() else None
    if target_entity is not None:
        target_identity = normalize_semantic_identifier(target_entity)
        claim_identity = normalize_semantic_identifier(claim.subject)
        if target_identity == claim_identity:
            return ()
    if explicit:
        return explicit
    if target_entity is None:
        raise ValueError(
            f"{kind.value} claim requires explicit entity applicability because target entity is absent"
        )
    raise ValueError(
        f"{kind.value} claim entity does not match target entity and lacks explicit applicability evidence"
    )


def _validate_stage_claims(
    *,
    kind: ResolutionAttemptKind,
    node: RequirementNode,
    parameter: str,
    claims: Sequence[RequirementClaim],
    entity_applicability_evidence: Mapping[str, Sequence[str]],
) -> tuple[str, ...]:
    used_entity_evidence: list[str] = []
    for claim in claims:
        if claim.requirement_id != node.requirement_id:
            raise ValueError(
                f"{kind.value} claim belongs to another requirement: {claim.requirement_id}"
            )
        if claim.predicate != parameter:
            raise ValueError(
                f"{kind.value} claim predicate does not match target parameter: "
                f"{claim.predicate}"
            )
        if not claim.subject or not claim.subject.strip():
            raise ValueError(f"{kind.value} claim requires a nonblank subject")
        _require_nonblank_claim_value(claim, context=kind.value)
        _require_governed_evidence(claim, context=kind.value)
        used_entity_evidence.extend(
            _validate_structured_entity(
                kind=kind,
                node=node,
                claim=claim,
                entity_applicability_evidence=entity_applicability_evidence,
            )
        )

        if kind is ResolutionAttemptKind.RULE:
            if claim.provenance.source_type is not RequirementSourceType.RULE:
                raise ValueError("RULE provider claims require RULE provenance")
            if claim.state not in {
                RequirementState.KNOWN,
                RequirementState.INFERRED,
                RequirementState.ASSUMPTION_REQUIRED,
                RequirementState.CONFLICT,
            }:
                raise ValueError(f"RULE provider cannot emit state {claim.state.value}")
            if claim.state is RequirementState.KNOWN:
                if claim.requires_human_validation or not _is_validated(claim):
                    raise ValueError(
                        "RULE KNOWN claims require governed validation and no pending human gate"
                    )
            elif claim.state is RequirementState.INFERRED and not claim.requires_human_validation:
                raise ValueError("RULE INFERRED claims must require human validation")

        elif kind is ResolutionAttemptKind.CALCULATION:
            if claim.provenance.source_type is not RequirementSourceType.CALCULATION:
                raise ValueError(
                    "CALCULATION provider claims require CALCULATION provenance"
                )
            if claim.state not in {
                RequirementState.CALCULATED,
                RequirementState.CONFLICT,
            }:
                raise ValueError(
                    f"CALCULATION provider cannot emit state {claim.state.value}"
                )
            if claim.state is RequirementState.CALCULATED:
                if claim.requires_human_validation or not _is_validated(claim):
                    raise ValueError(
                        "CALCULATED claims require governed validation and no pending human gate"
                    )

        elif kind is ResolutionAttemptKind.INFERENCE:
            if claim.provenance.source_type not in {
                RequirementSourceType.LLM_INFERENCE,
                RequirementSourceType.EXPERIENCE,
            }:
                raise ValueError(
                    "INFERENCE provider claims require LLM_INFERENCE or EXPERIENCE provenance"
                )
            if claim.state not in {
                RequirementState.INFERRED,
                RequirementState.ASSUMPTION_REQUIRED,
                RequirementState.CONFLICT,
            }:
                raise ValueError(
                    f"INFERENCE provider cannot emit state {claim.state.value}"
                )
            if claim.state is RequirementState.INFERRED and not claim.requires_human_validation:
                raise ValueError("INFERENCE claims must require human validation")

        else:
            raise ValueError(f"structured claim validation is unsupported for {kind.value}")

    return _clean_evidence_ids(used_entity_evidence)


def _retrieval_attempt_outcome(
    *,
    step: ResolutionStepResult,
    resolution: SemanticResolution,
) -> tuple[ResolutionAttemptStatus, tuple[str, ...]]:
    evidence_ids = _clean_evidence_ids(
        (
            *step.evidence_ids,
            *(
                evidence_id
                for match in resolution.matches
                for evidence_id in match.candidate.provenance.evidence_ids
            ),
            *(
                evidence_id
                for match in resolution.matches
                for evidence_id in match.entity_applicability_evidence_ids
            ),
            *(
                evidence_id
                for match in resolution.matches
                for evidence_id in match.applicability_evidence_ids
            ),
        )
    )

    if resolution.state is SemanticResolutionState.RESOLVED:
        if resolution.retrieved_claim is None:
            raise ValueError("RESOLVED semantic retrieval requires retrieved_claim")
        resolved_evidence = _clean_evidence_ids(
            (*evidence_ids, *resolution.retrieved_claim.provenance.evidence_ids)
        )
        if not resolved_evidence:
            raise ValueError("resolved RETRIEVAL attempt requires governed evidence")
        return ResolutionAttemptStatus.RESOLVED, resolved_evidence
    if resolution.state is SemanticResolutionState.AMBIGUOUS:
        return ResolutionAttemptStatus.CONFLICT, evidence_ids
    if resolution.state in {
        SemanticResolutionState.VALIDATION_REQUIRED,
        SemanticResolutionState.CANDIDATE,
    }:
        return ResolutionAttemptStatus.NOT_APPLICABLE, evidence_ids
    return ResolutionAttemptStatus.NOT_FOUND, evidence_ids


def _structured_attempt_outcome(
    *,
    kind: ResolutionAttemptKind,
    step: ResolutionStepResult,
    entity_applicability_evidence_ids: Sequence[str],
) -> tuple[ResolutionAttemptStatus, tuple[str, ...]]:
    evidence_ids = _clean_evidence_ids(
        (
            *step.evidence_ids,
            *_claim_evidence_ids(step.claims),
            *entity_applicability_evidence_ids,
        )
    )
    if any(claim.state is RequirementState.CONFLICT for claim in step.claims):
        return ResolutionAttemptStatus.CONFLICT, evidence_ids

    normalized_values = {
        normalize_semantic_value(claim.value)
        for claim in step.claims
        if str(claim.value).strip()
    }
    if len(normalized_values) > 1:
        return ResolutionAttemptStatus.CONFLICT, evidence_ids

    if kind is ResolutionAttemptKind.RULE and any(
        claim.state is RequirementState.KNOWN for claim in step.claims
    ):
        if not evidence_ids:
            raise ValueError("resolved RULE attempt requires governed evidence")
        return ResolutionAttemptStatus.RESOLVED, evidence_ids

    if kind is ResolutionAttemptKind.CALCULATION and any(
        claim.state is RequirementState.CALCULATED for claim in step.claims
    ):
        if not evidence_ids:
            raise ValueError("resolved CALCULATION attempt requires governed evidence")
        return ResolutionAttemptStatus.RESOLVED, evidence_ids

    if step.claims:
        return ResolutionAttemptStatus.NOT_APPLICABLE, evidence_ids
    return ResolutionAttemptStatus.NOT_FOUND, evidence_ids


def _preserve_unresolved_retrieval(
    *,
    assessment: GapAssessment,
    retrieval_resolution: SemanticResolution | None,
    attempts: Sequence[ResolutionAttempt],
) -> GapAssessment:
    """Do not let missing or exhausted later paths erase retrieved uncertainty."""
    if retrieval_resolution is None:
        return assessment
    if assessment.state not in {
        RequirementState.GAP_CANDIDATE,
        RequirementState.GAP_CONFIRMED,
    }:
        return assessment

    retrieval_evidence = _clean_evidence_ids(
        (
            *assessment.evidence_ids,
            *(
                evidence_id
                for attempt in attempts
                if attempt.kind is ResolutionAttemptKind.RETRIEVAL
                for evidence_id in attempt.evidence_ids
            ),
        )
    )
    if retrieval_resolution.state is SemanticResolutionState.VALIDATION_REQUIRED:
        return GapAssessment(
            requirement_id=assessment.requirement_id,
            parameter=assessment.parameter,
            state=RequirementState.HUMAN_VALIDATION_REQUIRED,
            reasons=(
                "retrieval found strong semantic evidence whose applicability or governance still requires validation",
                "no later resolution path produced a governed fact",
            ),
            evidence_ids=retrieval_evidence,
            confidence=ConfidenceBand.UNVERIFIED,
            human_validation_required=True,
        )
    if retrieval_resolution.state is SemanticResolutionState.CANDIDATE:
        return GapAssessment(
            requirement_id=assessment.requirement_id,
            parameter=assessment.parameter,
            state=RequirementState.GAP_CANDIDATE,
            reasons=(
                "retrieval found only non-authoritative semantic candidates",
                "candidate evidence must be validated before the gap can be confirmed",
            ),
            evidence_ids=retrieval_evidence,
            confidence=ConfidenceBand.UNVERIFIED,
            human_validation_required=True,
        )
    return assessment


def _attempt_note(
    *,
    kind: ResolutionAttemptKind,
    status: ResolutionAttemptStatus,
) -> str:
    """Produce bounded audit-safe notes rather than forwarding provider prose."""
    return f"governed {kind.value.casefold()} attempt: {status.value.casefold()}"


def _audit_attempt(
    *,
    attempt: ResolutionAttempt,
    retrieval_resolution: SemanticResolution | None,
) -> Mapping[str, object]:
    payload: dict[str, object] = {
        "kind": attempt.kind.value,
        "status": attempt.status.value,
        "source_reference": attempt.source_reference,
        "evidence_ids": _clean_evidence_ids(attempt.evidence_ids),
    }
    if (
        attempt.kind is ResolutionAttemptKind.RETRIEVAL
        and retrieval_resolution is not None
    ):
        payload["semantic"] = audit_semantic_resolution(retrieval_resolution)
    return payload


def audit_requirement_resolution(
    result: RequirementResolutionResult,
) -> Mapping[str, object]:
    """Return an audit-safe trace for the requirement-resolution subflow."""
    return {
        "requirement_id": result.requirement_id,
        "parameter": result.parameter,
        "executed_order": tuple(kind.value for kind in result.executed_order),
        "attempts": tuple(
            _audit_attempt(
                attempt=attempt,
                retrieval_resolution=result.retrieval_resolution,
            )
            for attempt in result.attempts
        ),
        "final": {
            "state": result.assessment.state.value,
            "evidence_ids": _clean_evidence_ids(result.assessment.evidence_ids),
            "confidence": result.assessment.confidence.value,
            "human_validation_required": result.assessment.human_validation_required,
        },
    }
