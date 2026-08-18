"""Executable multi-scenario consistency gate for the canonical diagnostic engine.

The gate validates a set of scenarios before downstream reasoning. It does not
perform diagnosis itself and therefore does not create a second scenario
authority.
"""

from dataclasses import dataclass
from typing import Mapping

from .diagnostic_scenarios import DiagnosticScenario, DiagnosticScenarioEngine


DEFAULT_SCENARIO_TYPES = ("BASELINE", "STRESS", "FAILURE", "COUNTERFACTUAL", "SENSITIVITY")


@dataclass(frozen=True)
class ScenarioGateResult:
    status: str
    scenario_ids: tuple[str, ...]
    scenario_types: tuple[str, ...]
    shared_evidence: tuple[str, ...]
    common_metrics: tuple[str, ...]
    changed_metrics: tuple[str, ...]
    gaps: tuple[str, ...] = ()
    ready_for_reasoning: bool = False


class MultiScenarioGate:
    """Validate scenario-set completeness and consistency without mutation."""

    def __init__(self, engine: DiagnosticScenarioEngine | None = None) -> None:
        self._engine = engine or DiagnosticScenarioEngine()

    def evaluate(
        self,
        scenarios: tuple[DiagnosticScenario, ...],
        *,
        required_types: tuple[str, ...] = DEFAULT_SCENARIO_TYPES,
    ) -> ScenarioGateResult:
        scenario_ids = tuple(item.scenario_id for item in scenarios)
        scenario_types = tuple(dict.fromkeys(
            item.metadata.get("scenario_type", "UNKNOWN").upper() for item in scenarios
        ))
        gaps: list[str] = []

        if not scenarios:
            return ScenarioGateResult("BLOCKED", (), (), (), (), (), ("no scenarios supplied",), False)

        missing_types = tuple(kind for kind in required_types if kind not in scenario_types)
        if missing_types:
            gaps.append(f"missing scenario types: {', '.join(missing_types)}")

        for scenario in scenarios:
            if not scenario.observations:
                gaps.append(f"{scenario.scenario_id}: no evidence observations")
            if scenario.has_conflict():
                gaps.append(f"{scenario.scenario_id}: conflicting evidence")
            if scenario.is_blocked():
                gaps.append(f"{scenario.scenario_id}: blocked evidence/governance")

        comparison = self._engine.compare(scenarios)
        shared_evidence = tuple(comparison.get("shared_evidence", ()))
        if not shared_evidence:
            gaps.append("no shared evidence across scenarios")

        common_metrics, changed_metrics = self._compare_metrics(scenarios)
        if not common_metrics:
            gaps.append("no common metrics declared")

        gaps_tuple = tuple(dict.fromkeys(gaps))
        ready = not gaps_tuple and comparison.get("requires_human_decision") is False
        return ScenarioGateResult(
            status="READY" if ready else "BLOCKED",
            scenario_ids=scenario_ids,
            scenario_types=scenario_types,
            shared_evidence=shared_evidence,
            common_metrics=common_metrics,
            changed_metrics=changed_metrics,
            gaps=gaps_tuple,
            ready_for_reasoning=ready,
        )

    @staticmethod
    def _compare_metrics(
        scenarios: tuple[DiagnosticScenario, ...],
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        metric_sets = []
        values: dict[str, set[str]] = {}
        for scenario in scenarios:
            metrics = tuple(filter(None, scenario.metadata.get("metrics", "").split(",")))
            metric_sets.append(set(metrics))
            for metric in metrics:
                values.setdefault(metric, set()).add(scenario.metadata.get(f"metric:{metric}", ""))
        if not metric_sets:
            return (), ()
        common = set.intersection(*metric_sets)
        changed = {metric for metric, metric_values in values.items() if len(metric_values) > 1}
        return tuple(sorted(common)), tuple(sorted(changed))
