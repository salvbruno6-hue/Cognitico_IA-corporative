from elo.core.diagnostic_scenario_engine import DiagnosticLens, DiagnosticObservation, DiagnosticScenarioEngine, ScenarioMode


def test_all_scenario_modes_are_supported_and_require_evidence():
    engine = DiagnosticScenarioEngine()
    for index, mode in enumerate(ScenarioMode):
        scenario = engine.build(
            f"scenario-{index}",
            "same production hypothesis",
            (DiagnosticObservation(DiagnosticLens.SYSTEMIC, "observed", (f"ev-{index}",), confidence=0.8),),
            mode=mode,
        )
        assert scenario.mode is mode
        assert scenario.is_consistent()


def test_conflict_blocks_scenario_comparison():
    engine = DiagnosticScenarioEngine()
    scenario = engine.build(
        "conflict",
        "conflicting causes",
        (DiagnosticObservation(
            DiagnosticLens.CAPACITY,
            "capacity issue",
            ("ev-1",),
            confidence=0.7,
            dependencies=("material-evidence-conflict",),
        ),),
        mode=ScenarioMode.STRESS,
    )
    result = engine.compare((scenario,))
    assert result["status"] == "BLOCKED"
    assert result["requires_human_decision"] is True


def test_unknowns_block_automatic_consistency():
    scenario = DiagnosticScenarioEngine().build(
        "unknown",
        "insufficient data",
        (DiagnosticObservation(
            DiagnosticLens.FLOW,
            "data missing",
            ("ev-1",),
            confidence=0.5,
            unknowns=("capacity baseline unavailable",),
        ),),
        mode=ScenarioMode.SENSITIVITY,
    )
    result = DiagnosticScenarioEngine().compare((scenario,))
    assert result["status"] == "COMPARABLE"
    assert result["requires_human_decision"] is True
