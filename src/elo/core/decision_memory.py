"""Decision memory primitives for traceable organizational learning."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionRecord:
    id: str
    decision: str
    rationale: str
    evidence_ids: tuple[str, ...] = ()
    impact: str = "UNCLASSIFIED"
    outcome_id: str | None = None
