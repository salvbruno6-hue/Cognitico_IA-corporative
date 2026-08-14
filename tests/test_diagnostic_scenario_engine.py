from elo.core.diagnostic_scenario_engine import (
    DiagnosticLens,
    DiagnosticObservation,
    DiagnosticScenarioEngine,
)


def obs(lens, finding, evidence=(), severity="INFO", confidence=0.8, dependencies=()):
    return DiagnosticObservation(
        lens=lens,
        finding=finding,
        evidence_ids=tuple(evidence),
        severity=severity,
        confidence=confidence,
        dependencies=tuple(dependencies),
    )


def test_same_problem_can_be_read_through_multiple_lenses():
    engine = DiagnosticScenarioEngine()
    scenario = engine.build(
        "delay-a",
        "pedido atrasado por restrição de produção",
        (
            obs(DiagnosticLens.FLOW, "fila aumentou", ["ev-flow"]),
            obs(DiagnosticLens.CAPACITY, "capacidade insuficiente", ["ev-cap"]),
            obs(DiagnosticLens.MATERIAL, "material crítico disponível", ["ev-mat"]),
        ),
    )
    assert set(scenario.lenses()) == {
        DiagnosticLens.FLOW,
        DiagnosticLens.CAPACITY,
        DiagnosticLens.MATERIAL,
    }
    assert scenario.evidence_ids() == ("ev-flow", "ev-cap", "ev-mat")


def test_comparison_blocks_conflicting_scenario():
    engine = DiagnosticScenarioEngine()
    first = engine.build(
        "capacity",
        "restrição de capacidade",
        (obs(DiagnosticLens.CAPACITY, "turno insuficiente", ["ev-1"], dependencies=["ev-2"]),),
    )
    second = engine.build(
        "material",
        "restrição de material",
        (obs(DiagnosticLens.MATERIAL, "insumo crítico", ["ev-1", "ev-3"]),),
    )
    result = engine.compare((first, second))
    assert result["status"] == "BLOCKED"
    assert result["shared_evidence"] == ("ev-1",)
    assert result["requires_human_decision"] is True


def test_empty_comparison_is_insufficient():
    result = DiagnosticScenarioEngine().compare(())
    assert result["status"] == "INSUFFICIENT"
