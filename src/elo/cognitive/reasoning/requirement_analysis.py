"""Governed semantic requirement representation and gap analysis for ELO.

This module extends the canonical reasoning owner with deterministic contracts.
It does not retrieve data, call an LLM, persist knowledge, or create a second
reasoning authority. It classifies evidence supplied by existing ELO owners and
prevents the conceptual error ``not present in the document == ELO gap``.

The module stores auditable justification (evidence, rules, decisions and
pending validation), never private model chain-of-thought.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping, Sequence


class RequirementState(StrEnum):
    KNOWN = "KNOWN"
    DOCUMENTED = "DOCUMENTED"
    RETRIEVED = "RETRIEVED"
    CALCULATED = "CALCULATED"
    INFERRED = "INFERRED"
    ASSUMPTION_REQUIRED = "ASSUMPTION_REQUIRED"
    CONFLICT = "CONFLICT"
    BLOCKED = "BLOCKED"
    MISSING = "MISSING"
    GAP_CANDIDATE = "GAP_CANDIDATE"
    GAP_CONFIRMED = "GAP_CONFIRMED"
    HUMAN_VALIDATION_REQUIRED = "HUMAN_VALIDATION_REQUIRED"


class RequirementSourceType(StrEnum):
    DOCUMENT = "DOCUMENT"
    ELO = "ELO"
    RULE = "RULE"
    CALCULATION = "CALCULATION"
    EXPERIENCE = "EXPERIENCE"
    LLM_INFERENCE = "LLM_INFERENCE"
    HUMAN = "HUMAN"


class ResolutionAttemptKind(StrEnum):
    RETRIEVAL = "RETRIEVAL"
    RULE = "RULE"
    CALCULATION = "CALCULATION"
    INFERENCE = "INFERENCE"


class ResolutionAttemptStatus(StrEnum):
    RESOLVED = "RESOLVED"
    NOT_FOUND = "NOT_FOUND"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    CONFLICT = "CONFLICT"


class ConfidenceBand(StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNVERIFIED = "UNVERIFIED"


@dataclass(frozen=True, slots=True)
class ClaimProvenance:
    source_type: RequirementSourceType
    source_reference: str
    reasoning_method: str
    evidence_ids: tuple[str, ...] = ()
    validation_status: str = "UNVERIFIED"

    def __post_init__(self) -> None:
        if not self.source_reference:
            raise ValueError("source_reference is required")
        if not self.reasoning_method:
            raise ValueError("reasoning_method is required")


@dataclass(frozen=True, slots=True)
class RequirementClaim:
    claim_id: str
    requirement_id: str
    subject: str
    predicate: str
    value: str
    state: RequirementState
    provenance: ClaimProvenance
    dependencies: tuple[str, ...] = ()
    requires_human_validation: bool = False

    def __post_init__(self) -> None:
        required = (self.claim_id, self.requirement_id, self.subject, self.predicate)
        if not all(required):
            raise ValueError("claim identity, requirement, subject and predicate are required")
        if self.state == RequirementState.DOCUMENTED and self.provenance.source_type != RequirementSourceType.DOCUMENT:
            raise ValueError("DOCUMENTED claims require DOCUMENT provenance")
        if self.state == RequirementState.CALCULATED and self.provenance.source_type != RequirementSourceType.CALCULATION:
            raise ValueError("CALCULATED claims require CALCULATION provenance")
        if self.state == RequirementState.INFERRED and self.provenance.source_type not in {
            RequirementSourceType.LLM_INFERENCE,
            RequirementSourceType.RULE,
            RequirementSourceType.EXPERIENCE,
        }:
            raise ValueError("INFERRED claims require inference/rule/experience provenance")


@dataclass(frozen=True, slots=True)
class ResolutionAttempt:
    kind: ResolutionAttemptKind
    status: ResolutionAttemptStatus
    source_reference: str
    evidence_ids: tuple[str, ...] = ()
    note: str = ""

    def __post_init__(self) -> None:
        if not self.source_reference:
            raise ValueError("resolution attempt requires source_reference")
        if self.status == ResolutionAttemptStatus.RESOLVED and not self.evidence_ids:
            raise ValueError("resolved attempt requires evidence")


@dataclass(frozen=True, slots=True)
class RequirementNode:
    requirement_id: str
    text: str
    entity: str | None = None
    claims: tuple[RequirementClaim, ...] = ()
    dependencies: tuple[str, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)
    requirement_dependencies: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.requirement_id or not self.text:
            raise ValueError("requirement_id and text are required")
        if any(claim.requirement_id != self.requirement_id for claim in self.claims):
            raise ValueError("all claims must belong to the requirement node")


@dataclass(frozen=True, slots=True)
class GapAssessment:
    requirement_id: str
    parameter: str
    state: RequirementState
    reasons: tuple[str, ...]
    evidence_ids: tuple[str, ...] = ()
    confidence: ConfidenceBand = ConfidenceBand.UNVERIFIED
    human_validation_required: bool = False


_USABLE_STATES = {
    RequirementState.DOCUMENTED,
    RequirementState.RETRIEVED,
    RequirementState.CALCULATED,
    RequirementState.KNOWN,
}

_REQUIRED_GAP_ATTEMPTS = {
    ResolutionAttemptKind.RETRIEVAL,
    ResolutionAttemptKind.RULE,
    ResolutionAttemptKind.CALCULATION,
    ResolutionAttemptKind.INFERENCE,
}

# Metadata is an extensibility surface and therefore cannot be copied wholesale
# into audit output. Only fields with an explicit audit purpose are allowed.
_AUDIT_SAFE_METADATA_KEYS = frozenset(
    {
        "source_reference",
        "locator",
        "origin_hash",
        "extraction_mode",
        "retrieval.record_id",
        "retrieval.reported_source_type",
        "retrieval.conversation_id",
        "retrieval.classification",
        "retrieval.uri",
        "retrieval.tenant_id",
        "retrieval.domain",
        "retrieval.principal_id",
        "retrieval.session_id",
        "retrieval.request_id",
        "retrieval.correlation_id",
        "retrieval.source_id",
        "retrieval.source_kind",
        "retrieval.required_capability",
        "retrieval.authorization_scope",
    }
)


def confidence_for_claims(claims: Sequence[RequirementClaim]) -> ConfidenceBand:
    """Return an evidence-derived confidence band without trusting model self-score."""
    if not claims:
        return ConfidenceBand.UNVERIFIED
    if any(claim.state == RequirementState.CONFLICT for claim in claims):
        return ConfidenceBand.LOW

    evidenced = [claim for claim in claims if claim.provenance.evidence_ids]
    if not evidenced:
        return ConfidenceBand.UNVERIFIED

    authoritative = {
        RequirementSourceType.DOCUMENT,
        RequirementSourceType.RULE,
        RequirementSourceType.CALCULATION,
        RequirementSourceType.HUMAN,
    }
    source_types = {claim.provenance.source_type for claim in evidenced}
    validated = any(claim.provenance.validation_status.upper() in {"VALIDATED", "APPROVED", "CONFIRMED"} for claim in evidenced)

    if source_types & authoritative and validated:
        return ConfidenceBand.HIGH
    if source_types & authoritative or len({evidence for claim in evidenced for evidence in claim.provenance.evidence_ids}) >= 2:
        return ConfidenceBand.MEDIUM
    return ConfidenceBand.LOW


def assess_parameter_gap(
    *,
    requirement_id: str,
    parameter: str,
    claims: Sequence[RequirementClaim],
    attempts: Sequence[ResolutionAttempt] = (),
) -> GapAssessment:
    """Classify one required parameter after governed resolution attempts.

    A confirmed gap is only possible after retrieval, rule, calculation and
    controlled inference have each been attempted without resolving the value.
    """
    relevant = tuple(claim for claim in claims if claim.predicate == parameter)
    evidence_ids = tuple(dict.fromkeys(
        evidence
        for claim in relevant
        for evidence in claim.provenance.evidence_ids
    ))

    if any(claim.state == RequirementState.CONFLICT for claim in relevant) or any(
        attempt.status == ResolutionAttemptStatus.CONFLICT for attempt in attempts
    ):
        return GapAssessment(
            requirement_id=requirement_id,
            parameter=parameter,
            state=RequirementState.CONFLICT,
            reasons=("conflicting evidence requires investigation",),
            evidence_ids=evidence_ids,
            confidence=ConfidenceBand.LOW,
            human_validation_required=True,
        )

    usable = tuple(claim for claim in relevant if claim.state in _USABLE_STATES)
    if usable:
        selected_state = usable[0].state
        return GapAssessment(
            requirement_id=requirement_id,
            parameter=parameter,
            state=selected_state,
            reasons=("parameter resolved by governed evidence",),
            evidence_ids=evidence_ids,
            confidence=confidence_for_claims(usable),
            human_validation_required=False,
        )

    inferred = tuple(claim for claim in relevant if claim.state == RequirementState.INFERRED)
    if inferred:
        return GapAssessment(
            requirement_id=requirement_id,
            parameter=parameter,
            state=RequirementState.HUMAN_VALIDATION_REQUIRED,
            reasons=("only an inference/hypothesis is available; it is not a contractual fact",),
            evidence_ids=evidence_ids,
            confidence=confidence_for_claims(inferred),
            human_validation_required=True,
        )

    assumption = tuple(claim for claim in relevant if claim.state == RequirementState.ASSUMPTION_REQUIRED)
    if assumption:
        return GapAssessment(
            requirement_id=requirement_id,
            parameter=parameter,
            state=RequirementState.ASSUMPTION_REQUIRED,
            reasons=("parameter requires an explicit governed assumption",),
            evidence_ids=evidence_ids,
            confidence=confidence_for_claims(assumption),
            human_validation_required=True,
        )

    attempted_kinds = {attempt.kind for attempt in attempts}
    unresolved_attempts = all(attempt.status != ResolutionAttemptStatus.RESOLVED for attempt in attempts)
    if _REQUIRED_GAP_ATTEMPTS.issubset(attempted_kinds) and unresolved_attempts:
        attempt_evidence = tuple(dict.fromkeys(
            evidence for attempt in attempts for evidence in attempt.evidence_ids
        ))
        return GapAssessment(
            requirement_id=requirement_id,
            parameter=parameter,
            state=RequirementState.GAP_CONFIRMED,
            reasons=(
                "document/current claims do not resolve the parameter",
                "retrieval, rule, calculation and controlled inference were attempted without resolution",
            ),
            evidence_ids=tuple(dict.fromkeys((*evidence_ids, *attempt_evidence))),
            confidence=ConfidenceBand.UNVERIFIED,
            human_validation_required=True,
        )

    return GapAssessment(
        requirement_id=requirement_id,
        parameter=parameter,
        state=RequirementState.GAP_CANDIDATE,
        reasons=("parameter is unresolved but governed resolution has not been exhausted",),
        evidence_ids=evidence_ids,
        confidence=ConfidenceBand.UNVERIFIED,
        human_validation_required=False,
    )


def audit_requirement(node: RequirementNode) -> Mapping[str, object]:
    """Return a compact auditable trace without private reasoning content."""
    evidence_ids = tuple(dict.fromkeys(
        evidence for claim in node.claims for evidence in claim.provenance.evidence_ids
    ))
    audit_metadata = {
        key: value
        for key, value in node.metadata.items()
        if key in _AUDIT_SAFE_METADATA_KEYS
    }
    return {
        "requirement_id": node.requirement_id,
        "source_claims": tuple(
            {
                "claim_id": claim.claim_id,
                "state": claim.state.value,
                "source_type": claim.provenance.source_type.value,
                "source_reference": claim.provenance.source_reference,
                "evidence_ids": claim.provenance.evidence_ids,
                "dependencies": claim.dependencies,
                "validation_status": claim.provenance.validation_status,
            }
            for claim in node.claims
        ),
        "evidence_ids": evidence_ids,
        "dependencies": node.dependencies,
        "requirement_dependencies": node.requirement_dependencies,
        "metadata": audit_metadata,
    }