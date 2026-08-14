"""Scenario-based diagnostic gates for the ELO Core Loop.

The diagnostic layer evaluates the same operational question through multiple
lenses before a decision is considered mature: operational, causal, temporal,
risk, capacity and evidence quality. It reports explainable findings without
turning hypotheses into facts or exposing private chain-of-thought.
"""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping


class DiagnosticLens(StrEnum):
    OPERATIONAL = "OPERATIONAL"
    CAUSAL = "CAUSAL"
    TEMPORAL = "TEMPORAL"
    CAPACITY = "CAPACITY"
    RISK = "RISK"
    EVIDENCE = "EVIDENCE"


class DiagnosticStatus(StrEnum):
    SUPPORTED = "SUPPORTED"
    INCONCLUSIVE = "INCONCLUSIVE"
    CONFLICTING = "CONFLICTING"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class DiagnosticObservation:
    lens: DiagnosticLens
    status: DiagnosticStatus
    finding: str
    evidence_ids: tuple[str, ...] = ()
    confidence: float = 0.0
    impact: str | None = None
    recommendation: str | None = None


@dataclass(frozen=True)
class DiagnosticScenario:
    scenario_id: str
    question: str
    entity: str | None = None
    scope: str | None = None
    observations: tuple[DiagnosticObservation, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def by_lens(self, lens: DiagnosticLens) -> tuple[DiagnosticObservation, ...]:
        return tuple(item for item in self.observations if item.lens == lens)

    def has_conflict(self) -> bool:
        return any(item.status == DiagnosticStatus.CONFLICTING for item in self.observations)

    def is_blocked(self) -> bool:
        return any(item.status == DiagnosticStatus.BLOCKED for item in self.observations)

    def evidence_quality(self) -> float:
        evidence = self.by_lens(DiagnosticLens.EVIDENCE)
        if not evidence:
            return 0.0
        return sum(item.confidence for item in evidence) / len(evidence)

    def decision_ready(self, minimum_confidence: float = 0.7) -> bool:
        if self.is_blocked() or self.has_conflict():
            return False
        required = {DiagnosticLens.OPERATIONAL, DiagnosticLens.CAUSAL, DiagnosticLens.EVIDENCE}
        present = {item.lens for item in self.observations}
        return required.issubset(present) and self.evidence_quality() >= minimum_confidence

    def human_summary(self) -> str:
        if self.is_blocked():
            return "Eu não considero este cenário pronto para decisão porque há um bloqueio de evidência ou governança."
        if self.has_conflict():
            return "Eu encontrei leituras conflitantes entre as evidências e não considero seguro consolidar uma decisão ainda."
        if self.decision_ready():
            return "Eu considero o cenário suficientemente sustentado para uma decisão, com base nas evidências operacionais, causais e de qualidade disponíveis."
        return "Eu encontrei sinais relevantes, mas ainda não tenho evidência suficiente para tratar a conclusão como decisão madura."


class DiagnosticScenarioEngine:
    """Build a scenario matrix without assuming that one lens explains everything."""

    LENSES = tuple(DiagnosticLens)

    def create(self, scenario_id: str, question: str, *, entity: str | None = None, scope: str | None = None) -> DiagnosticScenario:
        if not question.strip():
            raise ValueError("question is required")
        return DiagnosticScenario(scenario_id=scenario_id, question=question, entity=entity, scope=scope)

    @classmethod
    def required_lenses(cls) -> tuple[DiagnosticLens, ...]:
        return cls.LENSES
