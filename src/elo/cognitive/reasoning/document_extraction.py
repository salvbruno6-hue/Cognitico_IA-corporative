"""Deterministic document-to-requirement extraction for ELO.

This module only structures explicit textual material already obtained by an
existing authorized source adapter. It does not read files, retrieve sources,
call an LLM, persist records, infer missing facts, or promote learning.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Iterable, Sequence

from .requirement_analysis import (
    ClaimProvenance,
    RequirementClaim,
    RequirementNode,
    RequirementSourceType,
    RequirementState,
)


@dataclass(frozen=True, slots=True)
class DocumentSegment:
    source_reference: str
    text: str
    locator: str
    ordinal: int

    def __post_init__(self) -> None:
        if not self.source_reference or not self.locator:
            raise ValueError("source_reference and locator are required")
        if self.ordinal < 0:
            raise ValueError("ordinal must be non-negative")
        if not self.text.strip():
            raise ValueError("segment text is required")


@dataclass(frozen=True, slots=True)
class ExplicitRequirement:
    key: str
    value: str
    raw_text: str
    segment: DocumentSegment


_KEY_VALUE = re.compile(r"^\s*([^:;]{2,120}?)\s*:\s*(.+?)\s*$")
_BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+(.+?)\s*$")


def _stable_digest(*parts: str) -> str:
    material = "\x1f".join(part.strip() for part in parts)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def normalize_key(text: str) -> str:
    """Normalize only the claim key; factual values remain textual."""
    normalized = re.sub(r"[^a-z0-9]+", ".", text.casefold()).strip(".")
    if not normalized:
        raise ValueError("requirement key cannot normalize to empty")
    return normalized


def split_text_segments(*, source_reference: str, text: str) -> tuple[DocumentSegment, ...]:
    """Split already-retrieved text into stable non-empty line segments."""
    if not source_reference:
        raise ValueError("source_reference is required")
    segments: list[DocumentSegment] = []
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip():
            continue
        segments.append(
            DocumentSegment(
                source_reference=source_reference,
                text=raw_line,
                locator=f"line:{line_number}",
                ordinal=line_number,
            )
        )
    return tuple(segments)


def parse_explicit_requirement(segment: DocumentSegment) -> ExplicitRequirement | None:
    """Parse only explicit key/value statements; ambiguous prose remains unclassified."""
    raw = segment.text
    bullet = _BULLET.match(raw)
    candidate = bullet.group(1) if bullet else raw.strip()
    match = _KEY_VALUE.match(candidate)
    if not match:
        return None
    key_text, value = match.groups()
    if not value.strip():
        return None
    return ExplicitRequirement(
        key=normalize_key(key_text),
        value=value,
        raw_text=raw,
        segment=segment,
    )


def extract_documented_requirements(
    *,
    source_reference: str,
    text: str,
    requirement_prefix: str,
    subject: str,
    evidence_ids: Sequence[str] = (),
) -> tuple[RequirementNode, ...]:
    """Create DOCUMENTED claims only from explicit source statements.

    Identical source/locator/content triples are idempotently deduplicated. No
    value interpretation or technical inference occurs in this phase.
    """
    if not requirement_prefix or not subject:
        raise ValueError("requirement_prefix and subject are required")

    seen: set[str] = set()
    nodes: list[RequirementNode] = []
    index = 0
    for segment in split_text_segments(source_reference=source_reference, text=text):
        parsed = parse_explicit_requirement(segment)
        if parsed is None:
            continue
        digest = _stable_digest(source_reference, segment.locator, parsed.raw_text)
        if digest in seen:
            continue
        seen.add(digest)
        index += 1
        requirement_id = f"{requirement_prefix}:R{index}"
        claim_id = f"claim:{digest[:20]}"
        source_ref = f"{source_reference}#{segment.locator}"
        claim = RequirementClaim(
            claim_id=claim_id,
            requirement_id=requirement_id,
            subject=subject,
            predicate=parsed.key,
            value=parsed.value,
            state=RequirementState.DOCUMENTED,
            provenance=ClaimProvenance(
                source_type=RequirementSourceType.DOCUMENT,
                source_reference=source_ref,
                reasoning_method="explicit-key-value-extraction:v1",
                evidence_ids=tuple(evidence_ids),
                validation_status="EXTRACTED",
            ),
        )
        nodes.append(
            RequirementNode(
                requirement_id=requirement_id,
                text=parsed.raw_text,
                entity=subject,
                claims=(claim,),
                metadata={
                    "source_reference": source_reference,
                    "locator": segment.locator,
                    "origin_hash": digest,
                    "extraction_mode": "explicit-only",
                },
            )
        )
    return tuple(nodes)


def iter_claims(nodes: Iterable[RequirementNode]) -> tuple[RequirementClaim, ...]:
    """Flatten extraction output without introducing a second claim model."""
    return tuple(claim for node in nodes for claim in node.claims)
