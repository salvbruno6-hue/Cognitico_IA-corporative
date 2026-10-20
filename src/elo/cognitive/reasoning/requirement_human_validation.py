"""Governed human validation for semantic requirement claims.

This module applies an explicit human decision to a canonical
``RequirementResolutionResult`` without mutating the source hypothesis,
retrieval candidate, assumption or conflict. Approval/revision creates a new
``KNOWN`` claim with HUMAN provenance that must still pass the ordinary
``RequirementResolutionFlow`` preloaded-claim trust checks on replay.

The gate is not an execution, authorization, learning-promotion or persistence
boundary. It records only bounded decision/provenance data and never stores
private chain-of-thought.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
from typing import Mapping, Sequence

from .requirement_analysis import (
    ClaimProvenance,
    RequirementClaim,
    RequirementNode,
    RequirementSourceType,
    RequirementState,
)
from .requirement_resolution import RequirementResolutionResult


class HumanValidationAction(StrEnum):
    APPROVE = "APPROVE"
    REVISE = "REVISE"
    REJECT = "REJECT"


class HumanValidationStatus(StrEnum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


_MAX_HUMAN_VALUE_CHARS = 4096
_HUMAN_METHOD_PREFIX = "human-validation"


@dataclass(frozen=True, slots=True)
class HumanValidationDecision:
    decision_id: str
    reviewer_id: str
    requirement_id: str
    parameter: str
    action: HumanValidationAction
    target_claim_id: str | None = None
    value: str | None = None
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.action, HumanValidationAction):
            raise ValueError("human validation action must use HumanValidationAction")
        for name, value in (
            ("decision_id", self.decision_id),
            ("reviewer_id", self.reviewer_id),
            ("requirement_id", self.requirement_id),
            ("parameter", self.parameter),
        ):
            _require_canonical_id(value, field=name)

        if self.target_claim_id is not None:
            _require_canonical_id(self.target_claim_id, field="target_claim_id")
        _require_canonical_evidence_ids(self.evidence_ids)

        if self.action is HumanValidationAction.APPROVE:
            if self.target_claim_id is None:
                raise ValueError("APPROVE requires target_claim_id")
            if self.value is not None:
                raise ValueError("APPROVE uses candidate value and cannot supply value")
        elif self.action is HumanValidationAction.REVISE:
            if not isinstance(self.value, str) or not self.value.strip():
                raise ValueError("REVISE requires a nonblank human value")
            if self.value != self.value.strip():
                raise ValueError("REVISE value must be canonical without surrounding whitespace")
            if len(self.value) > _MAX_HUMAN_VALUE_CHARS:
                raise ValueError("REVISE value exceeds bounded size")
        elif self.action is HumanValidationAction.REJECT:
            if self.value is not None:
                raise ValueError("REJECT cannot supply value")


@dataclass(frozen=True, slots=True)
class HumanValidationResult:
    decision_id: str
    reviewer_id: str
    requirement_id: str
    parameter: str
    action: HumanValidationAction
    status: HumanValidationStatus
    source_claim_id: str | None
    evidence_ids: tuple[str, ...]
    validated_claim: RequirementClaim | None = None

    def __post_init__(self) -> None:
        if self.status is HumanValidationStatus.APPROVED and self.validated_claim is None:
            raise ValueError("approved human validation requires validated_claim")
        if self.status is HumanValidationStatus.REJECTED and self.validated_claim is not None:
            raise ValueError("rejected human validation cannot produce a claim")

    @property
    def can_execute(self) -> bool:
        return False


def apply_human_validation(
    *,
    node: RequirementNode,
    resolution: RequirementResolutionResult,
    decision: HumanValidationDecision,
) -> HumanValidationResult:
    """Apply one explicit human decision to an unresolved governed requirement."""
    _validate_target_alignment(node=node, resolution=resolution, decision=decision)
    if not resolution.assessment.human_validation_required:
        raise ValueError("requirement result does not require human validation")

    candidate: RequirementClaim | None = None
    if decision.target_claim_id is not None:
        candidate = _select_candidate(
            resolution=resolution,
            target_claim_id=decision.target_claim_id,
        )

    decision_evidence_id = _decision_evidence_id(decision)
    source_evidence = candidate.provenance.evidence_ids if candidate is not None else ()
    evidence_ids = _canonical_ids(
        (*decision.evidence_ids, *source_evidence, decision_evidence_id)
    )

    if decision.action is HumanValidationAction.REJECT:
        return HumanValidationResult(
            decision_id=decision.decision_id,
            reviewer_id=decision.reviewer_id,
            requirement_id=decision.requirement_id,
            parameter=decision.parameter,
            action=decision.action,
            status=HumanValidationStatus.REJECTED,
            source_claim_id=candidate.claim_id if candidate is not None else None,
            evidence_ids=evidence_ids,
            validated_claim=None,
        )

    _require_canonical_target_entity(node)

    if decision.action is HumanValidationAction.APPROVE:
        assert candidate is not None
        if candidate.state is RequirementState.CONFLICT:
            raise ValueError("CONFLICT candidate cannot be approved as a fact; use REVISE")
        if not isinstance(candidate.value, str) or not candidate.value.strip():
            raise ValueError("approved candidate requires a nonblank string value")
        if candidate.value != candidate.value.strip():
            raise ValueError("approved candidate value must be canonical without surrounding whitespace")
        value = candidate.value
    elif decision.action is HumanValidationAction.REVISE:
        assert isinstance(decision.value, str)
        value = decision.value
    else:  # pragma: no cover - enum exhaustiveness guard
        raise ValueError(f"unsupported human validation action: {decision.action}")

    source_claim_id = candidate.claim_id if candidate is not None else None
    dependencies = _canonical_ids(
        (
            *(candidate.dependencies if candidate is not None else ()),
            *((source_claim_id,) if source_claim_id is not None else ()),
        )
    )
    assert node.entity is not None
    claim = RequirementClaim(
        claim_id=_validated_claim_id(
            decision=decision,
            entity=node.entity,
            value=value,
            evidence_ids=evidence_ids,
        ),
        requirement_id=node.requirement_id,
        subject=node.entity,
        predicate=resolution.parameter,
        value=value,
        state=RequirementState.KNOWN,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.HUMAN,
            source_reference=f"human-validation:{decision.decision_id}",
            reasoning_method=f"{_HUMAN_METHOD_PREFIX}:{decision.action.value.casefold()}:v1",
            evidence_ids=evidence_ids,
            validation_status="APPROVED",
        ),
        dependencies=dependencies,
        requires_human_validation=False,
    )
    return HumanValidationResult(
        decision_id=decision.decision_id,
        reviewer_id=decision.reviewer_id,
        requirement_id=decision.requirement_id,
        parameter=decision.parameter,
        action=decision.action,
        status=HumanValidationStatus.APPROVED,
        source_claim_id=source_claim_id,
        evidence_ids=evidence_ids,
        validated_claim=claim,
    )


def audit_human_validation(result: HumanValidationResult) -> Mapping[str, object]:
    """Return bounded decision evidence without arbitrary notes or private reasoning."""
    return {
        "decision_id": result.decision_id,
        "reviewer_id": result.reviewer_id,
        "requirement_id": result.requirement_id,
        "parameter": result.parameter,
        "action": result.action.value,
        "status": result.status.value,
        "source_claim_id": result.source_claim_id,
        "evidence_ids": result.evidence_ids,
        "validated_claim_id": (
            result.validated_claim.claim_id if result.validated_claim is not None else None
        ),
        "validated_value": (
            result.validated_claim.value if result.validated_claim is not None else None
        ),
        "can_execute": result.can_execute,
    }


def _validate_target_alignment(
    *,
    node: RequirementNode,
    resolution: RequirementResolutionResult,
    decision: HumanValidationDecision,
) -> None:
    if resolution.requirement_id != node.requirement_id:
        raise ValueError("resolution does not belong to target requirement node")
    if decision.requirement_id != node.requirement_id:
        raise ValueError("human decision requirement_id mismatch")
    if decision.parameter != resolution.parameter:
        raise ValueError("human decision parameter mismatch")
    if resolution.assessment.requirement_id != node.requirement_id:
        raise ValueError("assessment does not belong to target requirement")
    if resolution.assessment.parameter != resolution.parameter:
        raise ValueError("assessment parameter mismatch")


def _require_canonical_target_entity(node: RequirementNode) -> None:
    if not node.entity or not node.entity.strip():
        raise ValueError("human validation requires an explicit target entity")
    if node.entity != node.entity.strip():
        raise ValueError("human validation target entity must be canonical without surrounding whitespace")


def _candidate_pool(resolution: RequirementResolutionResult) -> tuple[RequirementClaim, ...]:
    claims = [
        claim
        for claim in resolution.claims
        if claim.predicate == resolution.parameter and str(claim.value).strip()
    ]
    semantic = resolution.retrieval_resolution
    if semantic is not None:
        claims.extend(
            match.candidate
            for match in semantic.matches
            if str(match.candidate.value).strip()
        )
    # The same candidate may legitimately be exposed through more than one
    # result surface. Collapse structurally identical objects, but keep distinct
    # claims sharing an ID so _select_candidate can fail closed on ambiguity.
    return tuple(dict.fromkeys(claims))


def _select_candidate(
    *,
    resolution: RequirementResolutionResult,
    target_claim_id: str,
) -> RequirementClaim:
    matches = tuple(
        claim
        for claim in _candidate_pool(resolution)
        if claim.claim_id == target_claim_id
    )
    if not matches:
        raise ValueError("human validation target claim was not found")
    if len(matches) != 1:
        raise ValueError("human validation target claim identity is ambiguous")
    candidate = matches[0]
    _require_canonical_id(candidate.claim_id, field="candidate claim_id")
    return candidate


def _require_canonical_id(value: str, *, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be nonblank")
    if value != value.strip():
        raise ValueError(f"{field} must be canonical without surrounding whitespace")


def _require_canonical_evidence_ids(values: Sequence[str]) -> None:
    seen: set[str] = set()
    for value in values:
        _require_canonical_id(value, field="evidence_id")
        if value in seen:
            raise ValueError("human decision evidence_ids must be unique")
        seen.add(value)


def _canonical_ids(values: Sequence[str]) -> tuple[str, ...]:
    materialized = tuple(str(value) for value in values)
    for value in materialized:
        _require_canonical_id(value, field="reference_id")
    return tuple(sorted(set(materialized)))


def _decision_evidence_id(decision: HumanValidationDecision) -> str:
    material = "\x1f".join(
        (
            decision.decision_id,
            decision.reviewer_id,
            decision.requirement_id,
            decision.parameter,
            decision.action.value,
            decision.target_claim_id or "",
            decision.value if isinstance(decision.value, str) else "",
            *sorted(decision.evidence_ids),
        )
    )
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return f"evidence:human-validation:{digest[:24]}"


def _validated_claim_id(
    *,
    decision: HumanValidationDecision,
    entity: str,
    value: str,
    evidence_ids: Sequence[str],
) -> str:
    material = "\x1f".join(
        (
            decision.decision_id,
            decision.requirement_id,
            decision.parameter,
            entity,
            value,
            *sorted(evidence_ids),
        )
    )
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return f"claim:human-validation:{digest[:24]}"
