"""Deterministic semantic matching for governed ELO requirements.

The matcher sits inside the canonical Reasoning owner and only relates a
requirement parameter to already-structured ``RequirementClaim`` evidence. It
never retrieves sources, calls an LLM, persists knowledge, invents aliases or
promotes similarity into canonical truth.

Automatic resolution is deliberately narrow: only exact predicate identity or
an explicitly supplied governed alias may bind validated, evidenced knowledge
to a requirement as a ``RETRIEVED`` claim. Entity and requirement-context
applicability are independent gates. Cross-context reuse requires explicit
applicability evidence. A target with no entity identity also requires explicit
entity-applicability evidence. Token overlap is diagnostic only.
"""
from __future__ import annotations

import hashlib
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
    entity_compatible: bool = True
    entity_match_kind: SemanticMatchKind | None = None
    entity_applicability_evidence_ids: tuple[str, ...] = ()
    context_compatible: bool = True
    applicability_evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("semantic match score must be between 0 and 1")
        if not self.matched_terms:
            raise ValueError("semantic match requires matched_terms")
        if not self.entity_compatible and self.entity_match_kind is not None:
            raise ValueError("incompatible entity cannot declare an entity match kind")


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
        if not self.requirement_id.strip() or not self.parameter.strip():
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


def _clean_evidence_ids(values: Sequence[str]) -> tuple[str, ...]:
    """Return stable, nonblank evidence identifiers without duplication."""
    return tuple(
        dict.fromkeys(
            cleaned
            for value in values
            if (cleaned := str(value).strip())
        )
    )


def _strip_diacritics(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", str(value))
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def normalize_semantic_text(value: str) -> str:
    """Normalize labels deterministically without rewriting source evidence.

    Accents and case are normalized, punctuation becomes spaces and repeated
    whitespace is collapsed. Unicode alphanumeric characters outside ASCII stay
    comparable. This function is for semantic labels/predicates, not identifiers
    or technical values.
    """
    if value is None:
        raise ValueError("semantic text is required")
    folded = _strip_diacritics(value).casefold()
    normalized = "".join(char if char.isalnum() else " " for char in folded)
    return " ".join(normalized.split())


def normalize_semantic_identifier(value: str) -> str:
    """Normalize identifier case/spacing while preserving punctuation identity.

    Technical identifiers use punctuation as part of identity. Consequently
    ``MLT/C08`` and ``MLT-C08`` remain distinct unless an explicit entity alias
    relates them.
    """
    if value is None:
        raise ValueError("semantic identifier is required")
    folded = unicodedata.normalize("NFKC", _strip_diacritics(value)).casefold()
    return " ".join(folded.split())


def normalize_semantic_value(value: str) -> str:
    """Normalize a candidate value while preserving technical punctuation.

    Case, accents and whitespace are normalized, but punctuation and symbols are
    retained so semantically different technical values such as ``1.2 mm`` and
    ``1/2 mm`` cannot collapse into the same comparison key.
    """
    if value is None:
        raise ValueError("semantic value is required")
    folded = unicodedata.normalize("NFKC", _strip_diacritics(value)).casefold()
    return " ".join(folded.split())


def _alias_index(
    aliases: Mapping[str, Sequence[str]] | None,
    *,
    normalizer=normalize_semantic_text,
) -> Mapping[str, str]:
    index: dict[str, str] = {}
    for canonical, members in (aliases or {}).items():
        canonical_normalized = normalizer(canonical)
        if not canonical_normalized:
            raise ValueError("alias canonical term cannot normalize to empty")
        group_terms = (canonical, *members)
        for term in group_terms:
            normalized = normalizer(term)
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


def _strong_term_equivalence(
    left: str,
    right: str,
    aliases: Mapping[str, Sequence[str]] | None,
    *,
    normalizer=normalize_semantic_text,
) -> SemanticMatchKind | None:
    left_normalized = normalizer(left)
    right_normalized = normalizer(right)
    if not left_normalized or not right_normalized:
        return None
    if left_normalized == right_normalized:
        return SemanticMatchKind.EXACT
    alias_index = _alias_index(aliases, normalizer=normalizer)
    left_group = alias_index.get(left_normalized)
    right_group = alias_index.get(right_normalized)
    if left_group is not None and left_group == right_group:
        return SemanticMatchKind.GOVERNED_ALIAS
    return None


def _requirement_context_id(requirement_id: str) -> str:
    """Return the stable request/SO context for requirement-node identifiers."""
    head, separator, tail = requirement_id.rpartition(":")
    tail_upper = tail.upper()
    requirement_suffix = (
        tail_upper == "R"
        or tail_upper.startswith("R-")
        or (tail_upper.startswith("R") and tail_upper[1:].isdigit())
    )
    if separator and head and requirement_suffix:
        return head
    return requirement_id


def _context_is_compatible(
    *,
    required_requirement_id: str | None,
    candidate_requirement_id: str,
    applicability_evidence_ids: Sequence[str],
) -> bool:
    if required_requirement_id is None or not required_requirement_id.strip():
        return True
    if _requirement_context_id(required_requirement_id) == _requirement_context_id(candidate_requirement_id):
        return True
    return bool(_clean_evidence_ids(applicability_evidence_ids))


def match_parameter_to_claim(
    *,
    parameter: str,
    candidate: RequirementClaim,
    aliases: Mapping[str, Sequence[str]] | None = None,
    required_entity: str | None = None,
    entity_aliases: Mapping[str, Sequence[str]] | None = None,
    required_requirement_id: str | None = None,
    applicability_evidence_ids: Sequence[str] = (),
    entity_applicability_evidence_ids: Sequence[str] = (),
) -> SemanticMatch | None:
    """Compare one required parameter with one structured evidence claim.

    Predicate equivalence, entity identity and request-context applicability are
    independent. Cross-context candidates remain consultative unless the caller
    supplies explicit governed evidence that the candidate applies here. When a
    target entity is absent, explicit entity-applicability evidence is mandatory
    before the candidate subject can be rebound to the target requirement.
    """
    parameter_normalized = normalize_semantic_text(parameter)
    predicate_normalized = normalize_semantic_text(candidate.predicate)
    if not parameter_normalized or not predicate_normalized:
        return None

    parameter_kind = _strong_term_equivalence(parameter, candidate.predicate, aliases)
    if parameter_kind is SemanticMatchKind.EXACT:
        score = 1.0
        matched_terms = (parameter_normalized,)
    elif parameter_kind is SemanticMatchKind.GOVERNED_ALIAS:
        score = 0.95
        matched_terms = tuple(sorted({parameter_normalized, predicate_normalized}))
    else:
        overlap, common = _token_overlap(parameter_normalized, predicate_normalized)
        if overlap < 0.5 or not common:
            return None
        parameter_kind = SemanticMatchKind.TOKEN_OVERLAP
        score = min(overlap, 0.79)
        matched_terms = common

    explicit_entity_applicability = _clean_evidence_ids(
        entity_applicability_evidence_ids
    )
    entity_match_kind: SemanticMatchKind | None = None
    if required_entity is not None and required_entity.strip():
        entity_match_kind = _strong_term_equivalence(
            required_entity,
            candidate.subject,
            entity_aliases,
            normalizer=normalize_semantic_identifier,
        )
        entity_compatible = entity_match_kind in {
            SemanticMatchKind.EXACT,
            SemanticMatchKind.GOVERNED_ALIAS,
        }
        if not entity_compatible:
            entity_match_kind = None
    else:
        # A candidate's subject cannot silently become the target subject when
        # the target requirement did not establish entity identity.
        entity_compatible = bool(explicit_entity_applicability)

    explicit_applicability = _clean_evidence_ids(applicability_evidence_ids)
    context_compatible = _context_is_compatible(
        required_requirement_id=required_requirement_id,
        candidate_requirement_id=candidate.requirement_id,
        applicability_evidence_ids=explicit_applicability,
    )

    return SemanticMatch(
        candidate=candidate,
        kind=parameter_kind,
        score=score,
        matched_terms=matched_terms,
        entity_compatible=entity_compatible,
        entity_match_kind=entity_match_kind,
        entity_applicability_evidence_ids=explicit_entity_applicability,
        context_compatible=context_compatible,
        applicability_evidence_ids=explicit_applicability,
    )


def _candidate_is_governed(candidate: RequirementClaim) -> bool:
    return (
        candidate.state in _GOVERNED_STATES
        and candidate.provenance.source_type is not RequirementSourceType.LLM_INFERENCE
        and not candidate.requires_human_validation
        and bool(candidate.requirement_id.strip())
        and bool(candidate.subject.strip())
        and bool(str(candidate.value).strip())
        and bool(candidate.provenance.source_reference.strip())
        and bool(_clean_evidence_ids(candidate.provenance.evidence_ids))
        and candidate.provenance.validation_status.strip().upper() in _VALIDATION_OK
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
    candidate_evidence = _clean_evidence_ids(candidate.provenance.evidence_ids)
    combined_evidence = _clean_evidence_ids(
        (
            *candidate_evidence,
            *match.entity_applicability_evidence_ids,
            *match.applicability_evidence_ids,
        )
    )
    provenance = ClaimProvenance(
        source_type=candidate.provenance.source_type,
        source_reference=candidate.provenance.source_reference.strip(),
        reasoning_method=f"semantic-match:{match.kind.value.casefold()}:v1",
        evidence_ids=combined_evidence,
        validation_status=candidate.provenance.validation_status.strip(),
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
        subject=node.entity.strip() if node.entity and node.entity.strip() else candidate.subject,
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
    aliases: Mapping[str, Sequence[str]] | None = None,
    entity_aliases: Mapping[str, Sequence[str]] | None = None,
    applicability_evidence: Mapping[str, Sequence[str]] | None = None,
    entity_applicability_evidence: Mapping[str, Sequence[str]] | None = None,
) -> SemanticResolution:
    """Resolve a requirement parameter against already-governed evidence.

    Exact and explicitly aliased predicate matches are strong. A strong match
    still cannot resolve automatically when entity or request-context
    applicability is unproven, any applicable evidence is conflicting/pending
    human validation, candidate values conflict, or source claims lack governed
    validation/evidence. A missing target entity fails closed unless explicit
    entity-applicability evidence is supplied. Token overlap remains
    non-authoritative.
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
                    required_entity=node.entity,
                    entity_aliases=entity_aliases,
                    required_requirement_id=node.requirement_id,
                    applicability_evidence_ids=(applicability_evidence or {}).get(
                        candidate.claim_id,
                        (),
                    ),
                    entity_applicability_evidence_ids=(
                        entity_applicability_evidence or {}
                    ).get(candidate.claim_id, ()),
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

    entity_applicable = tuple(match for match in strong if match.entity_compatible)
    if not entity_applicable:
        return SemanticResolution(
            requirement_id=node.requirement_id,
            parameter=parameter,
            state=SemanticResolutionState.VALIDATION_REQUIRED,
            matches=matches,
            reasons=("parameter equivalence exists, but applicability to the requirement entity is not established",),
            human_validation_required=True,
        )

    applicable = tuple(match for match in entity_applicable if match.context_compatible)
    if not applicable:
        return SemanticResolution(
            requirement_id=node.requirement_id,
            parameter=parameter,
            state=SemanticResolutionState.VALIDATION_REQUIRED,
            matches=matches,
            reasons=("entity equivalence exists, but applicability to the current requirement context is not evidenced",),
            human_validation_required=True,
        )

    if any(match.candidate.state is RequirementState.CONFLICT for match in applicable):
        return SemanticResolution(
            requirement_id=node.requirement_id,
            parameter=parameter,
            state=SemanticResolutionState.AMBIGUOUS,
            matches=matches,
            reasons=("applicable semantic evidence contains an explicit conflict state",),
            human_validation_required=True,
        )

    if any(match.candidate.requires_human_validation for match in applicable):
        return SemanticResolution(
            requirement_id=node.requirement_id,
            parameter=parameter,
            state=SemanticResolutionState.VALIDATION_REQUIRED,
            matches=matches,
            reasons=("applicable semantic evidence still carries an explicit human-validation gate",),
            human_validation_required=True,
        )

    distinct_values = {
        normalized
        for match in applicable
        if (normalized := normalize_semantic_value(match.candidate.value))
    }
    if len(distinct_values) > 1:
        return SemanticResolution(
            requirement_id=node.requirement_id,
            parameter=parameter,
            state=SemanticResolutionState.AMBIGUOUS,
            matches=matches,
            reasons=("strong applicable semantic matches disagree on the candidate value",),
            human_validation_required=True,
        )

    governed = tuple(match for match in applicable if _candidate_is_governed(match.candidate))
    if not governed:
        return SemanticResolution(
            requirement_id=node.requirement_id,
            parameter=parameter,
            state=SemanticResolutionState.VALIDATION_REQUIRED,
            matches=matches,
            reasons=("semantic equivalence exists, but no applicable matched claim has governed validation, value, evidence and cleared human-validation state",),
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
                "candidate_requirement_id": match.candidate.requirement_id,
                "candidate_subject": match.candidate.subject,
                "recovered_value": match.candidate.value,
                "candidate_state": match.candidate.state.value,
                "candidate_requires_human_validation": match.candidate.requires_human_validation,
                "kind": match.kind.value,
                "score": match.score,
                "matched_terms": match.matched_terms,
                "entity_compatible": match.entity_compatible,
                "entity_match_kind": (
                    match.entity_match_kind.value
                    if match.entity_match_kind is not None
                    else None
                ),
                "entity_applicability_evidence_ids": (
                    match.entity_applicability_evidence_ids
                ),
                "context_compatible": match.context_compatible,
                "applicability_evidence_ids": match.applicability_evidence_ids,
                "source_type": match.candidate.provenance.source_type.value,
                "source_reference": match.candidate.provenance.source_reference.strip(),
                "evidence_ids": _clean_evidence_ids(match.candidate.provenance.evidence_ids),
                "validation_status": match.candidate.provenance.validation_status.strip(),
            }
            for match in resolution.matches
        ),
        "retrieved_claim_id": (
            resolution.retrieved_claim.claim_id
            if resolution.retrieved_claim is not None
            else None
        ),
    }
