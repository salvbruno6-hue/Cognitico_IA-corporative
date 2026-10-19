"""Deterministic semantic matching for governed ELO requirements.

The matcher sits inside the canonical Reasoning owner and only relates a
requirement parameter to already-structured ``RequirementClaim`` evidence. It
never retrieves sources, calls an LLM, persists knowledge, invents aliases or
promotes similarity into canonical truth.

Automatic resolution is deliberately narrow: only exact predicate identity or
an explicitly supplied governed alias may bind validated, evidenced knowledge
to a requirement as a ``RETRIEVED`` claim. Token overlap is diagnostic only.
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping, Sequence

from .requirement_analysis import (
    ClaimProvenance,
    RequirementClaim,
    RequirementNode,
    RequirementSourceType,
    RequirementState,
)


class SemanticMatchKind(StrEnum):
    EXACT = "EXACT"
    GOVERNED_ALIAS = "GOVERNED_ALIAS"
    TOKEN_OVERLAP = "TOKEN_OVERLAP"


class SemanticResolutionState(StrEnum):
    RESOLVED = "RESOLVED"
    VALIDATION_REQUIRED = "VALIDATION_REQUIRED"
    AMBIGUOUS = "AMBIGUOUS"
    CANDIDATE = "CANDIDATE"
    NO_MATCH = "NO_MATCH"


@dataclass(frozen=True, slots=True)
class SemanticMatch:
    candidate: RequirementClaim
    kind: SemanticMatchKind
    score: float
    matched_terms: tuple[str, ...]

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("semantic match score must be between 0 and 1")
        if not self.matched_terms:
            raise ValueError("semantic match requires matched_terms")


@dataclass(frozen=True, slots=True)
class SemanticResolution:
    requirement_id: str
    parameter: str
    state: SemanticResolutionState
    matches: tuple[SemanticMatch, ...] = ()
    retrieved_claim: RequirementClaim | None = None
    reasons: tuple[str, ...] = ()
    human_validation_required: bool = False

    def __post_init__(self) -> None:
        if not self.requirement_id or not self.parameter:
            raise ValueError("semantic resolution requires requirement_id and parameter")
        if self.retrieved_claim is not None:
            if self.state is not SemanticResolutionState.RESOLVED:
                raise ValueError("retrieved_claim is only valid for RESOLVED semantic matching")
            if self.retrieved_claim.requirement_id != self.requirement_id:
                raise ValueError("retrieved_claim must belong to the resolved requirement")
            if self.retrieved_claim.predicate != self.parameter:
                raise ValueError("retrieved_claim must bind the resolved parameter")


_VALIDATION_OK = frozenset({"VALIDATED", "APPROVED", "CONFIRMED"})
_GOVERNED_STATES = frozenset(
    {
        RequirementState.KNOWN,
        RequirementState.DOCUMENTED,
        RequirementState.RETRIEVED,
        RequirementState.CALCULATED,
    }
)


def normalize_semantic_text(value: str) -> str:
    """Normalize text deterministically while preserving the original evidence.

    Unicode accents are removed for comparison, text is case-folded, punctuation
    becomes spaces and repeated whitespace is collapsed. The normalized value is
    never written back into the source claim.
    """
    if value is None:
        raise ValueError("semantic text is required")
    decomposed = unicodedata.normalize("NFKD", str(value))
    without_marks = "".join(char for char in decomposed if not unicodedata.combining(char))
    normalized = re.sub(r"[^a-z0-9]+", " ", without_marks.casefold()).strip()
    return re.sub(r"\s+", " ", normalized)


def _alias_index(aliases: Mapping[str, Sequence[str]]) -> Mapping[str, str]:
    index: dict[str, str] = {}
    for canonical, members in aliases.items():
        canonical_normalized = normalize_semantic_text(canonical)
        if not canonical_normalized:
            raise ValueError("alias canonical term cannot normalize to empty")
        group_terms = (canonical, *members)
        for term in group_terms:
            normalized = normalize_semantic_text(term)
            if not normalized:
                raise ValueError("alias term cannot normalize to empty")
            previous = index.get(normalized)
            if previous is not None and previous != canonical_normalized:
                raise ValueError(f"semantic alias collision for {normalized}")
            index[normalized] = canonical_normalized
    return index


def _token_overlap(left: str, right: str) -> tuple[float, tuple[str, ...]]:
    left_tokens = frozenset(left.split())
    right_tokens = frozenset(right.split())
    if not left_tokens or not right_tokens:
        return 0.0, ()
    common = tuple(sorted(left_tokens & right_tokens))
    union = left_tokens | right_tokens
    return len(common) / len(union), common


def match_parameter_to_claim(
    *,
    parameter: str,
    candidate: RequirementClaim,
    aliases: Mapping[str, Sequence[str]] = {},
) -> SemanticMatch | None:
    """Compare one required parameter with one structured evidence claim."""
    parameter_normalized = normalize_semantic_text(parameter)
    predicate_normalized = normalize_semantic_text(candidate.predicate)
    if not parameter_normalized or not predicate_normalized:
        return None

    if parameter_normalized == predicate_normalized:
        return SemanticMatch(
            candidate=candidate,
            kind=SemanticMatchKind.EXACT,
            score=1.0,
            matched_terms=(parameter_normalized,),
        )

    alias_index = _alias_index(aliases)
    parameter_group = alias_index.get(parameter_normalized)
    predicate_group = alias_index.get(predicate_normalized)
    if parameter_group is not None and parameter_group == predicate_group:
        return SemanticMatch(
            candidate=candidate,
            kind=SemanticMatchKind.GOVERNED_ALIAS,
            score=0.95,
            matched_terms=tuple(sorted({parameter_normalized, predicate_normalized})),
        )

    overlap, common = _token_overlap(parameter_normalized, predicate_normalized)
    if overlap >= 0.5 and common:
        # Lexical overlap is useful for ranking/investigation but is never strong
        # enough to become an automatic governed resolution.
        return SemanticMatch(
            candidate=candidate,
            kind=SemanticMatchKind.TOKEN_OVERLAP,
            score=min(overlap, 0.79),
            matched_terms=common,
        )
    return None


def _candidate_is_governed(candidate: RequirementClaim) -> bool:
    return (
        candidate.state in _GOVERNED_STATES
        and candidate.provenance.source_type is not RequirementSourceType.LLM_INFERENCE
        and bool(candidate.provenance.evidence_ids)
        and candidate.provenance.validation_status.upper() in _VALIDATION_OK
    )


def _stable_claim_id(*parts: str) -> str:
    material = "\x1f".join(part.strip() for part in parts)
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return f"claim:semantic:{digest[:20]}"


def _bind_retrieved_claim(
    *,
    node: RequirementNode,
    parameter: str,
    match: SemanticMatch,
) -> RequirementClaim:
    candidate = match.candidate
    provenance = ClaimProvenance(
        source_type=candidate.provenance.source_type,
        source_reference=candidate.provenance.source_reference,
        reasoning_method=f"semantic-match:{match.kind.value.casefold()}:v1",
        evidence_ids=candidate.provenance.evidence_ids,
        validation_status=candidate.provenance.validation_status,
    )
    return RequirementClaim(
        claim_id=_stable_claim_id(
            node.requirement_id,
            parameter,
            candidate.claim_id,
            candidate.value,
            candidate.provenance.source_reference,
        ),
        requirement_id=node.requirement_id,
        subject=node.entity or candidate.subject,
        predicate=parameter,
        value=candidate.value,
        state=RequirementState.RETRIEVED,
        provenance=provenance,
        dependencies=tuple(dict.fromkeys((*candidate.dependencies, candidate.claim_id))),
        requires_human_validation=False,
    )


def resolve_requirement_parameter(
    *,
    node: RequirementNode,
    parameter: str,
    candidates: Sequence[RequirementClaim],
    aliases: Mapping[str, Sequence[str]] = {},
) -> SemanticResolution:
    """Resolve a requirement parameter against already-governed evidence.

    Exact and explicitly aliased predicate matches are strong. A strong match
    still cannot resolve automatically when values conflict or the source claim
    lacks governed validation/evidence. Token overlap remains a non-authoritative
    candidate signal.
    """
    if not parameter or not parameter.strip():
        raise ValueError("parameter is required")

    matches = tuple(
        sorted(
            (
                match
                for candidate in candidates
                if (match := match_parameter_to_claim(
                    parameter=parameter,
                    candidate=candidate,
                    aliases=aliases,
                ))
                is not None
            ),
            key=lambda item: (
                -item.score,
                item.candidate.provenance.source_reference,
                item.candidate.claim_id,
            ),
        )
    )
    if not matches:
        return SemanticResolution(
            requirement_id=node.requirement_id,
            parameter=parameter,
            state=SemanticResolutionState.NO_MATCH,
            reasons=("no semantic evidence matched the required parameter",),
        )

    strong = tuple(
        match for match in matches
        if match.kind in {SemanticMatchKind.EXACT, SemanticMatchKind.GOVERNED_ALIAS}
    )
    if not strong:
        return SemanticResolution(
            requirement_id=node.requirement_id,
            parameter=parameter,
            state=SemanticResolutionState.CANDIDATE,
            matches=matches,
            reasons=("only lexical overlap was found; similarity is not evidence of equivalence",),
        )

    distinct_values = {
        normalize_semantic_text(match.candidate.value)
        for match in strong
    }
    if len(distinct_values) > 1:
        return SemanticResolution(
            requirement_id=node.requirement_id,
            parameter=parameter,
            state=SemanticResolutionState.AMBIGUOUS,
            matches=matches,
            reasons=("strong semantic matches disagree on the candidate value",),
            human_validation_required=True,
        )

    governed = tuple(match for match in strong if _candidate_is_governed(match.candidate))
    if not governed:
        return SemanticResolution(
            requirement_id=node.requirement_id,
            parameter=parameter,
            state=SemanticResolutionState.VALIDATION_REQUIRED,
            matches=matches,
            reasons=("semantic equivalence exists, but no matched claim has governed validation and evidence",),
            human_validation_required=True,
        )

    selected = governed[0]
    retrieved = _bind_retrieved_claim(node=node, parameter=parameter, match=selected)
    return SemanticResolution(
        requirement_id=node.requirement_id,
        parameter=parameter,
        state=SemanticResolutionState.RESOLVED,
        matches=matches,
        retrieved_claim=retrieved,
        reasons=("parameter resolved from validated governed evidence through deterministic semantic matching",),
        human_validation_required=False,
    )


def audit_semantic_resolution(resolution: SemanticResolution) -> Mapping[str, object]:
    """Expose an audit-safe semantic decision trace without private reasoning."""
    return {
        "requirement_id": resolution.requirement_id,
        "parameter": resolution.parameter,
        "state": resolution.state.value,
        "human_validation_required": resolution.human_validation_required,
        "reasons": resolution.reasons,
        "matches": tuple(
            {
                "candidate_claim_id": match.candidate.claim_id,
                "kind": match.kind.value,
                "score": match.score,
                "matched_terms": match.matched_terms,
                "source_type": match.candidate.provenance.source_type.value,
                "source_reference": match.candidate.provenance.source_reference,
                "evidence_ids": match.candidate.provenance.evidence_ids,
                "validation_status": match.candidate.provenance.validation_status,
            }
            for match in resolution.matches
        ),
        "retrieved_claim_id": (
            resolution.retrieved_claim.claim_id
            if resolution.retrieved_claim is not None
            else None
        ),
    }
