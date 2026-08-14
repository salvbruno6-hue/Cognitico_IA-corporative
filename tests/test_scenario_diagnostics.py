from elo.core.scenario_diagnostics import (
    DiagnosticScenario,
    DiagnosticStatus,
    ScenarioType,
    ScenarioVariable,
    compare_scenarios,
    evaluate_scenario,
)


def make_scenario(**overrides):
    values = {
        "scenario_id": "SC-001",
        "scenario_type": ScenarioType.BASELINE,
        "description": "production capacity review",
        "variables": (ScenarioVariable("capacity", 100, 90, "units"),),
        "evidence_ids": ("EV-001",),
    }
    values.update(overrides)
    return DiagnosticScenario(**values)


def test_baseline_produces_observable_delta():
    result = evaluate_scenario(make_scenario())
    assert result.status is DiagnosticStatus.READY
    assert result.decision_ready
    assert result.observations[0].delta == -10
    assert "capacity:DOWN" in result.risks


def test_missing_evidence_blocks_diagnosis():
    result = evaluate_scenario(make_scenario(evidence_ids=()))
    assert result.status is DiagnosticStatus.INSUFFICIENT_EVIDENCE
    assert not result.decision_ready


def test_all_scenario_types_use_one_contract():
    for scenario_type in ScenarioType:
        result = evaluate_scenario(make_scenario(scenario_type=scenario_type))
        assert result.status is DiagnosticStatus.READY


def test_assumptions_remain_unknowns():
    result = evaluate_scenario(make_scenario(assumptions=("supplier lead time is stable",)))
    assert result.unknowns == ("supplier lead time is stable",)


def test_multiple_scenarios_are_comparable_without_mutating_inputs():
    baseline = make_scenario(scenario_id="BASE")
    stress = make_scenario(
        scenario_id="STRESS",
        scenario_type=ScenarioType.STRESS,
        variables=(ScenarioVariable("capacity", 100, 70, "units"),),
    )
    comparison = compare_scenarios((baseline, stress))
    assert comparison.decision_ready
    assert comparison.common_metrics == ("capacity",)
    assert comparison.changed_metrics == ("capacity",)
    assert baseline.variables[0].scenario == 90
    assert stress.variables[0].scenario == 70


def test_comparison_blocks_when_one_scenario_lacks_evidence():
    comparison = compare_scenarios((make_scenario(), make_scenario(evidence_ids=())))
    assert comparison.blocked
    assert comparison.reason == "insufficient evidence"
    assert not comparison.decision_ready
