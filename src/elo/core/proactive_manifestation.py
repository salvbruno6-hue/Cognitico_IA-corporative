"""Governed decision boundary for proactive ELO user guidance.

This module does not execute actions, own memory, or replace authorization.
It only decides whether a contextual opportunity is relevant enough to surface
and what level of assistance may be offered.
"""

from dataclasses import dataclass
from enum import StrEnum


class ManifestationLevel(StrEnum):
    SILENT = "SILENT"
    INFORM = "INFORM"
    SUGGEST = "SUGGEST"
    PREPARE = "PREPARE"
    AUTHORIZE = "AUTHORIZE"


@dataclass(frozen=True)
class ProactiveContext:
    opportunity: bool
    relevance: float
    confidence: float
    impact: float
    novelty: float = 0.0
    repeated: bool = False
    context_sufficient: bool = True
    capability_available: bool = True
    authorization_required: bool = False


@dataclass(frozen=True)
class ProactiveManifestation:
    level: ManifestationLevel
    reason: str

    @property
    def should_manifest(self) -> bool:
        return self.level != ManifestationLevel.SILENT


def evaluate_proactive_manifestation(context: ProactiveContext) -> ProactiveManifestation:
    """Return a fail-closed manifestation decision from bounded context signals."""
    values = (context.relevance, context.confidence, context.impact, context.novelty)
    if any(value < 0 or value > 1 for value in values):
        raise ValueError("proactive signals must be between 0 and 1")
    if not context.opportunity or not context.context_sufficient:
        return ProactiveManifestation(ManifestationLevel.SILENT, "no_actionable_opportunity")
    if not context.capability_available:
        return ProactiveManifestation(ManifestationLevel.SILENT, "capability_unavailable")
    if context.repeated and context.novelty < 0.25:
        return ProactiveManifestation(ManifestationLevel.SILENT, "repetition_cooldown")
    if context.relevance < 0.60 or context.confidence < 0.60:
        return ProactiveManifestation(ManifestationLevel.SILENT, "insufficient_relevance_or_confidence")
    if context.authorization_required or context.impact >= 0.80:
        return ProactiveManifestation(ManifestationLevel.AUTHORIZE, "high_impact_or_authorization_required")
    if context.impact >= 0.55:
        return ProactiveManifestation(ManifestationLevel.PREPARE, "material_decision_support")
    if context.relevance >= 0.80:
        return ProactiveManifestation(ManifestationLevel.SUGGEST, "highly_relevant_capability")
    return ProactiveManifestation(ManifestationLevel.INFORM, "relevant_contextual_capability")
