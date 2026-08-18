"""Compatibility facade for the canonical diagnostic scenario engine.

The canonical scenario/diagnostic owner is ``diagnostic_scenarios``.
This module preserves the historical API used by existing callers/tests while
routing comparison semantics through the canonical owner. New code should
import from ``elo.core.diagnostic_scenarios`` directly.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping

from .diagnostic_scenarios import (
    DiagnosticLens as CanonicalLens,
    DiagnosticObservation as CanonicalObservation,
    DiagnosticScenario as CanonicalScenario,
    DiagnosticScenarioEngine as CanonicalEngine,
    DiagnosticStatus,
)


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

    def lenses(self) -> tuple[DiagnosticLens, ...]:
        return tuple(dict.fromkeys(o.lens for o in self.observations))

    def evidence_ids(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(
            evidence_id
            for observation in self.observations
            for evidence_id in observation.evidence_ids
        ))

    def unknowns(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(
            unknown for observation in self.observations for unknown in observation.unknowns
        ))

    def conflicts(self) -> tuple[str, ...]:
        conflicts: list[str] = []
        for observation in self.observations:
            conflicts.extend(observation.dependencies)
        return tuple(dict.fromkeys(conflicts))

    def is_consistent(self) -> bool:
        return bool(self.observations and self.evidence_ids()) and not self.conflicts()


def _canonical_lens(lens: DiagnosticLens) -> CanonicalLens:
    mapping = {
        DiagnosticLens.FLOW: CanonicalLens.OPERATIONAL,
        DiagnosticLens.CAPACITY: CanonicalLens.CAPACITY,
        DiagnosticLens.MATERIAL: CanonicalLens.OPERATIONAL,
        DiagnosticLens.SCHEDULE: CanonicalLens.TEMPORAL,
        DiagnosticLens.QUALITY: CanonicalLens.EVIDENCE,
        DiagnosticLens.FINANCIAL_IMPACT: CanonicalLens.RISK,
        DiagnosticLens.CUSTOMER_IMPACT: CanonicalLens.OPERATIONAL,
        DiagnosticLens.SYSTEMIC: CanonicalLens.CAUSAL,
    }
    return mapping[lens]


class DiagnosticScenarioEngine:
    """Backward-compatible facade delegating scenario comparison to the canonical engine."""

    def __init__(self) -> None:
        self._canonical = CanonicalEngine()

    def build(
        self,
        scenario_id: str,
        hypothesis: str,
        observations: tuple[DiagnosticObservation, ...],
        assumptions: tuple[str, ...] = (),
        mode: object | None = None,
    ) -> DiagnosticScenario:
        del assumptions, mode
        return DiagnosticScenario(
            scenario_id=scenario_id,
            hypothesis=hypothesis,
            observations=observations,
        )

    def compare(
        self,
        scenarios: tuple[DiagnosticScenario, ...],
    ) -> Mapping[str, object]:
        canonical_scenarios: list[CanonicalScenario] = []
        for scenario in scenarios:
            observations: list[CanonicalObservation] = []
            for index, observation in enumerate(scenario.observations):
                evidence_id = observation.evidence_ids[0] if observation.evidence_ids else f"{scenario.scenario_id}:observation:{index}"
                status = DiagnosticStatus.CONFLICTING if observation.dependencies else DiagnosticStatus.SUPPORTED
                observations.append(
                    CanonicalObservation(
                        evidence_id=evidence_id,
                        dimension=observation.lens.value,
                        value=max(0.0, min(1.0, observation.confidence)),
                        statement=observation.finding,
                        confidence=max(0.0, min(1.0, observation.confidence)),
                        lens=_canonical_lens(observation.lens),
                        status=status,
                    )
                )
            canonical_scenarios.append(
                CanonicalScenario(
                    scenario_id=scenario.scenario_id,
                    question=scenario.hypothesis,
                    observations=tuple(observations),
                )
            )
        result = dict(self._canonical.compare(tuple(canonical_scenarios)))
        if any(scenario.unknowns() for scenario in scenarios):
            result["requires_human_decision"] = True
        return result
