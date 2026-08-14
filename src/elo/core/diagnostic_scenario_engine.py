"""Scenario-oriented diagnostic engine for ELO.

The engine does not guess a single cause. It evaluates the same operational
context through multiple diagnostic lenses and returns comparable findings.
It is intentionally deterministic and evidence-driven so a later GPT
specialist can critique or enrich the diagnosis without becoming the source
of truth.
"""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping


class DiagnosticLens(StrEnum):
    FLOW = "FLOW"
    CAPACITY = "CAPACITY"
    MATERIAL = "MATERIAL"
    SCHEDULE = "SCHEDULE"
    QUALITY = "QUALITY"
    FINANCIAL_IMPACT = "FINANCIAL_IMPACT"
    CUSTOMER_IMPACT = "CUSTOMER_IMPACT"
    SYSTEMIC = "SYSTEMIC"


@dataclass(frozen=True)
class DiagnosticObservation:
    lens: DiagnosticLens
    finding: str
    evidence_ids: tuple[str, ...] = ()
    severity: str = "INFO"
    confidence: float = 0.0
    unknowns: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()


@dataclass(frozen=True)
class DiagnosticScenario:
    scenario_id: str
    hypothesis: str
    observations: tuple[DiagnosticObservation, ...] = ()
    assumptions: tuple[str, ...] = ()

    def lenses(self) -> tuple[DiagnosticLens, ...]:
        return tuple(dict.fromkeys(o.lens for o in self.observations))

    def evidence_ids(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(
            evidence_id
            for observation in self.observations
            for evidence_id in observation.evidence_ids
        ))

    def conflicts(self) -> tuple[str, ...]:
        conflicts: list[str] = []
        for observation in self.observations:
            if observation.dependencies:
                conflicts.extend(observation.dependencies)
        return tuple(dict.fromkeys(conflicts))


class DiagnosticScenarioEngine:
    """Build and compare evidence-backed diagnostic scenarios."""

    DEFAULT_LENSES = (
        DiagnosticLens.FLOW,
        DiagnosticLens.CAPACITY,
        DiagnosticLens.MATERIAL,
        DiagnosticLens.SCHEDULE,
        DiagnosticLens.QUALITY,
        DiagnosticLens.CUSTOMER_IMPACT,
        DiagnosticLens.SYSTEMIC,
    )

    def build(
        self,
        scenario_id: str,
        hypothesis: str,
        observations: tuple[DiagnosticObservation, ...],
        assumptions: tuple[str, ...] = (),
    ) -> DiagnosticScenario:
        return DiagnosticScenario(
            scenario_id=scenario_id,
            hypothesis=hypothesis,
            observations=observations,
            assumptions=assumptions,
        )

    def compare(
        self,
        scenarios: tuple[DiagnosticScenario, ...],
    ) -> Mapping[str, object]:
        if not scenarios:
            return {"status": "INSUFFICIENT", "scenarios": (), "shared_evidence": ()}

        evidence_sets = [set(s.evidence_ids()) for s in scenarios]
        shared = set.intersection(*evidence_sets) if evidence_sets else set()
        covered_lenses = tuple(dict.fromkeys(
            lens for scenario in scenarios for lens in scenario.lenses()
        ))
        return {
            "status": "COMPARABLE",
            "scenarios": tuple(s.scenario_id for s in scenarios),
            "shared_evidence": tuple(sorted(shared)),
            "covered_lenses": covered_lenses,
            "requires_human_decision": any(s.conflicts() for s in scenarios),
        }
