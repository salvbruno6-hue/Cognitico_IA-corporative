"""Governed multi-scenario diagnostics for ELO.

The layer compares the same evidence through different scenario lenses without
promoting assumptions to facts. Domain adapters provide variables and evidence;
this layer provides repeatable reading, comparison and decision-readiness.
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


@dataclass(frozen=True)
class ScenarioComparison:
    diagnostics: tuple[ScenarioDiagnostic, ...]
    common_metrics: tuple[str, ...] = ()
    changed_metrics: tuple[str, ...] = ()
    blocked: bool = False
    reason: str | None = None

    @property
    decision_ready(self) -> bool:
        return bool(self.diagnostics) and not self.blocked and all(
            diagnostic.decision_ready for diagnostic in self.diagnostics
        )


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


def compare_scenarios(scenarios: tuple[DiagnosticScenario, ...]) -> ScenarioComparison:
    diagnostics = tuple(evaluate_scenario(scenario) for scenario in scenarios)
    if not diagnostics:
        return ScenarioComparison((), blocked=True, reason="no scenarios")
    if any(item.status == DiagnosticStatus.INSUFFICIENT_EVIDENCE for item in diagnostics):
        return ScenarioComparison(diagnostics, blocked=True, reason="insufficient evidence")
    if any(item.status == DiagnosticStatus.CONFLICT for item in diagnostics):
        return ScenarioComparison(diagnostics, blocked=True, reason="scenario contract conflict")

    metric_sets = [
        {observation.metric for observation in diagnostic.observations}
        for diagnostic in diagnostics
    ]
    common = set.intersection(*metric_sets) if metric_sets else set()
    changed = {
        observation.metric
        for diagnostic in diagnostics
        for observation in diagnostic.observations
        if observation.delta not in (None, 0)
    }
    return ScenarioComparison(
        diagnostics=diagnostics,
        common_metrics=tuple(sorted(common)),
        changed_metrics=tuple(sorted(changed)),
    )
