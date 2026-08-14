"""Domain helpers for automated learning from Análise de Solicitações conversations.

The module is intentionally small: it prepares a normalized, auditable learning
candidate and delegates admission/persistence to the existing ELO intake and
Evolution Memory mechanisms.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Mapping


DOMAIN = "ANALISE_SOLICITACOES"


@dataclass(frozen=True)
class SolicitationLearningCandidate:
    learning_id: str
    solicitation_id: str
    category: str
    statement: str
    evidence_refs: tuple[str, ...] = ()
    recurrence_count: int = 1
    distinct_clients: int = 1
    accepted_count: int = 0
    rejected_count: int = 0
    impact: str = "UNKNOWN"
    applicability: str | None = None
    exceptions: tuple[str, ...] = ()
    confidence: float = 0.0
    validation_status: str = "CAPTURED"
    provenance: Mapping[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


def _stable_id(solicitation_id: str, category: str, statement: str) -> str:
    payload = f"{DOMAIN}|{solicitation_id}|{category}|{statement.strip()}".encode("utf-8")
    return f"sol:{sha256(payload).hexdigest()[:24]}"


def build_learning_candidate(
    *,
    solicitation_id: str,
    category: str,
    statement: str,
    evidence_refs: list[str] | tuple[str, ...] = (),
    impact: str = "UNKNOWN",
    applicability: str | None = None,
    exceptions: list[str] | tuple[str, ...] = (),
    confidence: float = 0.0,
    provenance: Mapping[str, Any] | None = None,
) -> SolicitationLearningCandidate:
    """Normalize one learning observation; do not promote it to an ELO rule."""
    if not solicitation_id.strip():
        raise ValueError("solicitation_id is required")
    if not category.strip():
        raise ValueError("category is required")
    if not statement.strip():
        raise ValueError("statement is required")
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be between 0 and 1")

    return SolicitationLearningCandidate(
        learning_id=_stable_id(solicitation_id, category, statement),
        solicitation_id=solicitation_id.strip(),
        category=category.strip(),
        statement=statement.strip(),
        evidence_refs=tuple(evidence_refs),
        impact=impact,
        applicability=applicability,
        exceptions=tuple(exceptions),
        confidence=confidence,
        validation_status="CAPTURED",
        provenance=dict(provenance or {}),
    )


def classify_candidate(candidate: SolicitationLearningCandidate) -> str:
    """Return the governance class; one observation is a precedent, not a rule."""
    if candidate.recurrence_count <= 1:
        return "PRECEDENT"
    if candidate.validation_status in {"VALIDATED", "APPROVED"}:
        return "VALIDATED_LEARNING"
    return "LEARNING_CANDIDATE"
