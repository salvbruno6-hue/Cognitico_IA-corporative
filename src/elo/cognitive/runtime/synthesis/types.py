"""Tipos do delta de síntese.

Refs: ADR-0014.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DeltaItem:
    """Um item do delta estruturado."""
    category: str           # aligned | improvements | corrections | conflicts
    summary: str
    evidence: list[str] = field(default_factory=list)
    source: str | None = None  # so_learning | handbook | precedent
    confidence: float = 0.0


@dataclass
class SynthesisDelta:
    """Resultado da síntese entre análise externa e contexto ELO."""
    so_id: str | None
    aligned: list[DeltaItem] = field(default_factory=list)
    improvements: list[DeltaItem] = field(default_factory=list)
    corrections: list[DeltaItem] = field(default_factory=list)
    conflicts: list[DeltaItem] = field(default_factory=list)
    precedents_used: list[str] = field(default_factory=list)
    handbook_used: list[str] = field(default_factory=list)
    learning_used: str | None = None
    overall_confidence: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "so_id": self.so_id,
            "aligned": [i.__dict__ for i in self.aligned],
            "improvements": [i.__dict__ for i in self.improvements],
            "corrections": [i.__dict__ for i in self.corrections],
            "conflicts": [i.__dict__ for i in self.conflicts],
            "precedents_used": self.precedents_used,
            "handbook_used": self.handbook_used,
            "learning_used": self.learning_used,
            "overall_confidence": self.overall_confidence,
        }
