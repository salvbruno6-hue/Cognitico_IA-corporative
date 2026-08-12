"""Application boundary for evidence-grounded reasoning."""
from __future__ import annotations

from typing import Iterable

from . import EvidenceItem, ReasoningResult
from .engine import ReasoningEngine
from .policy import validate_reasoning_result


class ReasoningService:
    """Coordinates reasoning and critique without executing business actions."""

    def __init__(self, engine: ReasoningEngine | None = None) -> None:
        self.engine = engine or ReasoningEngine()

    def evaluate(self, query: str, evidence: Iterable[EvidenceItem], *, provenance: dict | None = None) -> ReasoningResult:
        result = self.engine.reason(query, evidence=list(evidence), provenance=provenance)
        validate_reasoning_result(result)
        return result
