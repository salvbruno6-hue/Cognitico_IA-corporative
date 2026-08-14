"""Governed scenario diagnostics for ELO.

This module does not predict a single future. It evaluates a scenario from
multiple diagnostic perspectives so ELO can compare consequences before a
decision: baseline, stress, failure, counterfactual and sensitivity.

The module is deliberately domain-neutral. Domain adapters provide the facts
and relationships; this layer provides the diagnostic contract and evidence
requirements.
"""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping


class ScenarioType(StrEnum):
    BASELINE = "BASELINE"
    STRESS = "STRESS"
    FAILURE = "FAILURE"
    COUNTERFACTUAL = "COUNTERFACTUAL"
    SENSITIVITY = "SENSITIVITY"


class DiagnosticStatus(StrEnum):
    READY = "READY"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    CONFLICT = "CONFLICT"


@dataclass(frozen=True)
class ScenarioVariable:
    name: str
    baseline: float
    scenario: float
    unit: str | None = None


@dataclass(frozen=True)
class ScenarioObservation:
    metric: str
    baseline: float | None
    scenario: float | None
    delta: float | None
    direction: str
    evidence_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class DiagnosticScenario:
    scenario_id: str
    scenario_type: ScenarioType
    description: str
    variables: tuple[ScenarioVariable, ...]
    evidence_ids: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def has_evidence(self) -> bool:
        return bool(self.evidence_ids)

    def validate(self) -> DiagnosticStatus:
        if not self.has_evidence():
            return DiagnosticStatus.INSUFFICIENT_EVIDENCE
        if not self.description.strip():
            return DiagnosticStatus.CONFLICT
        if any(not variable.name.strip() for variable in self.variables):
            return DiagnosticStatus.CONFLICT
        return DiagnosticStatus.READY


@dataclass(frozen=True)
class ScenarioDiagnostic:
    scenario: DiagnosticScenario
    observations: tuple[ScenarioObservation, ...]
    status: DiagnosticStatus
    risks: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()

    @property
    def decision_ready(self) -> bool:
        return self.status == DiagnosticStatus.READY and bool(self.observations)


def evaluate_scenario(scenario: DiagnosticScenario) -> ScenarioDiagnostic:
    status = scenario.validate()
    if status != DiagnosticStatus.READY:
        return ScenarioDiagnostic(scenario, (), status)

    observations: list[ScenarioObservation] = []
    risks: list[str] = []
    for variable in scenario.variables:
        delta = variable.scenario - variable.baseline
        direction = "UNCHANGED" if delta == 0 else ("UP" if delta > 0 else "DOWN")
        observations.append(
            ScenarioObservation(
                metric=variable.name,
                baseline=variable.baseline,
                scenario=variable.scenario,
                delta=delta,
                direction=direction,
                evidence_ids=scenario.evidence_ids,
            )
        )
        if delta != 0:
            risks.append(f"{variable.name}:{direction}")

    return ScenarioDiagnostic(
        scenario=scenario,
        observations=tuple(observations),
        status=status,
        risks=tuple(risks),
        unknowns=scenario.assumptions,
    )
