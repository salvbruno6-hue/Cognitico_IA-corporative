from elo.core.scenario_diagnostics import DiagnosticScenario, DiagnosticStatus, ScenarioType, ScenarioVariable, evaluate_scenario


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
