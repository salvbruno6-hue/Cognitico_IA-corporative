from elo.core.diagnostic_scenarios import DiagnosticLens, DiagnosticObservation, DiagnosticScenario
from elo.core.scenario_gates import MultiScenarioGate


def scenario(kind: str, value: str, evidence: str = "e1") -> DiagnosticScenario:
    observation = DiagnosticObservation(
        evidence_id=evidence,
        dimension="capacity",
        value=0.9,
        statement=f"{kind} observation",
        confidence=0.9,
        lens=DiagnosticLens.CAPACITY,
    )
    return DiagnosticScenario(
        scenario_id=kind.lower(),
        question="compare capacity",
        observations=(observation,),
        metadata={
            "scenario_type": kind,
            "metrics": "capacity,cost,lead_time",
            "metric:capacity": value,
            "metric:cost": value,
            "metric:lead_time": value,
        },
    )


def test_multi_scenario_gate_requires_complete_set_and_common_evidence():
    scenarios = tuple(scenario(kind, "100") for kind in ("BASELINE", "STRESS", "FAILURE", "COUNTERFACTUAL", "SENSITIVITY"))
    result = MultiScenarioGate().evaluate(scenarios)
    assert result.status == "READY"
    assert result.ready_for_reasoning is True
    assert result.shared_evidence == ("e1",)
    assert result.common_metrics == ("capacity", "cost", "lead_time")
    assert result.changed_metrics == ()


def test_multi_scenario_gate_blocks_missing_scenario_type():
    scenarios = tuple(scenario(kind, "100") for kind in ("BASELINE", "STRESS", "FAILURE"))
    result = MultiScenarioGate().evaluate(scenarios)
    assert result.status == "BLOCKED"
    assert result.ready_for_reasoning is False
    assert any("missing scenario types" in gap for gap in result.gaps)


def test_multi_scenario_gate_blocks_without_shared_evidence():
    scenarios = (
        scenario("BASELINE", "100", "e1"),
        scenario("STRESS", "110", "e2"),
        scenario("FAILURE", "80", "e3"),
        scenario("COUNTERFACTUAL", "105", "e4"),
        scenario("SENSITIVITY", "95", "e5"),
    )
    result = MultiScenarioGate().evaluate(scenarios)
    assert result.status == "BLOCKED"
    assert "no shared evidence across scenarios" in result.gaps


def test_multi_scenario_gate_detects_changed_metrics_without_mutating_scenarios():
    scenarios = tuple(
        scenario(kind, value)
        for kind, value in (
            ("BASELINE", "100"),
            ("STRESS", "120"),
            ("FAILURE", "70"),
            ("COUNTERFACTUAL", "105"),
            ("SENSITIVITY", "95"),
        )
    )
    before = tuple(item.metadata for item in scenarios)
    result = MultiScenarioGate().evaluate(scenarios)
    assert result.changed_metrics == ("capacity", "cost", "lead_time")
    assert tuple(item.metadata for item in scenarios) == before
