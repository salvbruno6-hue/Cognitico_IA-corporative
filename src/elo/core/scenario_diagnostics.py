"""Scenario diagnostics for ELO's systemic decision loop.

The diagnostic layer evaluates the same operational situation through multiple
lenses without creating multiple reasoning engines. It produces comparable,
auditable observations for the ELO to reconcile.
"""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping


class DiagnosticLens(StrEnum):
    OPERATIONAL = "OPERATIONAL"
    CAPACITY = "CAPACITY"
    MATERIAL = "MATERIAL"
    FINANCIAL = "FINANCIAL"
    CUSTOMER = "CUSTOMER"
    RISK = "RISK"
    TEMPORAL = "TEMPORAL"
    SYSTEMIC = "SYSTEMIC"


@dataclass(frozen=True)
class ScenarioObservation:
    lens: DiagnosticLens
    finding: str
    severity: str = "INFO"
    confidence: float = 0.0
    evidence_ids: tuple[str, ...] = ()
    impacts: tuple[str, ...] = ()
    uncertainties: tuple[str, ...] = ()


@dataclass(frozen=True)
class ScenarioDiagnostic:
    scenario_id: str
    question: str
    observations: tuple[ScenarioObservation, ...] = ()
    assumptions: tuple[str, ...] = ()
    decision_required: bool = False
    recommended_action: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)

    def observations_by_lens(self, lens: DiagnosticLens) -> tuple[ScenarioObservation, ...]:
        return tuple(item for item in self.observations if item.lens == lens)

    def conflicts(self) -> tuple[tuple[ScenarioObservation, ScenarioObservation], ...]:
        pairs = []
        for index, left in enumerate(self.observations):
            for right in self.observations[index + 1 :]:
                if left.lens != right.lens and left.finding != right.finding:
                    shared_evidence = set(left.evidence_ids) & set(right.evidence_ids)
                    if shared_evidence:
                        pairs.append((left, right))
        return tuple(pairs)

    def confidence(self) -> float:
        if not self.observations:
            return 0.0
        return sum(item.confidence for item in self.observations) / len(self.observations)

    def requires_escalation(self, threshold: float = 0.6) -> bool:
        return self.decision_required or self.conflicts() or self.confidence() < threshold
