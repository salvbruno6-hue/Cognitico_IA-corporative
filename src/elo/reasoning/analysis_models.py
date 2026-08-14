"""Governed reasoning, decision and consulting models for ELO stages 4-6."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping


class ClaimType(StrEnum):
    FACT = "FACT"
    OBSERVATION = "OBSERVATION"
    INFERENCE = "INFERENCE"
    HYPOTHESIS = "HYPOTHESIS"
    RECOMMENDATION = "RECOMMENDATION"
    DECISION = "DECISION"
    UNKNOWN = "UNKNOWN"


class EvidencePolarity(StrEnum):
    SUPPORTS = "SUPPORTS"
    CONTRADICTS = "CONTRADICTS"
    NEUTRAL = "NEUTRAL"


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


@dataclass(frozen=True, slots=True)
class EvidenceEvaluation:
    evidence_id: str
    claim_id: str
    polarity: EvidencePolarity
    quality: str
    relevance: float
    rationale: str
    provenance: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "relevance", _bounded(self.relevance))


@dataclass(frozen=True, slots=True)
class Hypothesis:
    hypothesis_id: str
    statement: str
    confidence: float = 0.0
    evidence_refs: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", _bounded(self.confidence))


@dataclass(frozen=True, slots=True)
class CritiqueResult:
    target_claim_id: str
    contradictions: tuple[str, ...] = ()
    alternatives: tuple[str, ...] = ()
    missing_information: tuple[str, ...] = ()
    revised_confidence: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(self, "revised_confidence", _bounded(self.revised_confidence))


@dataclass(frozen=True, slots=True)
class Scenario:
    scenario_id: str
    name: str
    description: str
    expected_impacts: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    confidence: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", _bounded(self.confidence))


@dataclass(frozen=True, slots=True)
class DecisionSupport:
    decision_id: str
    problem: str
    alternatives: tuple[Scenario, ...]
    recommended_option: str | None = None
    rationale: str = ""
    decision_owner: str | None = None
    evidence_refs: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class InformationGap:
    gap_id: str
    question: str
    reason: str
    priority: str = "MEDIUM"
    impact_if_unknown: str = ""


@dataclass(frozen=True, slots=True)
class ConsultingAssessment:
    assessment_id: str
    problem: str
    known: tuple[str, ...] = ()
    unknown: tuple[str, ...] = ()
    hypotheses: tuple[Hypothesis, ...] = ()
    information_gaps: tuple[InformationGap, ...] = ()
    recommendations: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
