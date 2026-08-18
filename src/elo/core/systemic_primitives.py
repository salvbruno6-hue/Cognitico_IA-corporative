"""Provider-neutral systemic intelligence value objects for the ELO Core.

These primitives describe evidence-backed reasoning state. They do not execute
operations, persist memory, select providers, or authorize changes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Tuple


@dataclass(frozen=True)
class SystemicRelation:
    source: str
    relation: str
    target: str
    evidence_ids: Tuple[str, ...] = ()
    confidence: float = 0.0

    def __post_init__(self) -> None:
        if not self.source or not self.relation or not self.target:
            raise ValueError("source, relation and target are required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class SystemicModel:
    entities: Tuple[str, ...] = ()
    relations: Tuple[SystemicRelation, ...] = ()
    evidence_ids: Tuple[str, ...] = ()


@dataclass(frozen=True)
class CausalAssessment:
    cause: str
    effect: str
    confidence: float
    evidence_ids: Tuple[str, ...] = ()
    assumptions: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.cause or not self.effect:
            raise ValueError("cause and effect are required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class DecisionRecord:
    decision_id: str
    decision: str
    rationale: str
    impact: Tuple[str, ...] = ()
    evidence_ids: Tuple[str, ...] = ()
    authority: Optional[str] = None
    expected_outcome: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.decision_id or not self.decision or not self.rationale:
            raise ValueError("decision_id, decision and rationale are required")


@dataclass(frozen=True)
class OutcomeFeedback:
    decision_id: str
    expected: str
    observed: str
    variance: Optional[str] = None
    evidence_ids: Tuple[str, ...] = ()
    observed_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if not self.decision_id or not self.expected or not self.observed:
            raise ValueError("decision_id, expected and observed are required")


@dataclass(frozen=True)
class TemporalValidity:
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    last_confirmed_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.valid_from and self.valid_until and self.valid_until < self.valid_from:
            raise ValueError("valid_until cannot precede valid_from")


@dataclass(frozen=True)
class UncertaintyAssessment:
    confidence: float
    uncertainty_level: str
    evidence_ids: Tuple[str, ...] = ()
    limitations: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not self.uncertainty_level:
            raise ValueError("uncertainty_level is required")


@dataclass(frozen=True)
class Scenario:
    name: str
    assumptions: Tuple[str, ...] = ()
    expected_effects: Tuple[str, ...] = ()
    evidence_ids: Tuple[str, ...] = ()
    uncertainty: Optional[UncertaintyAssessment] = None

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("scenario name is required")
