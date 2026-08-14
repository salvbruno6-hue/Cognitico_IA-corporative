from dataclasses import replace

from elo.core.diagnostic_scenarios import DiagnosticLens, DiagnosticObservation, DiagnosticScenarioEngine, DiagnosticStatus


def test_engine_exposes_multiple_lenses():
    lenses = DiagnosticScenarioEngine.required_lenses()
    assert set(lenses) == set(DiagnosticLens)


def test_scenario_is_not_ready_without_evidence():
    scenario = DiagnosticScenarioEngine().create("S-001", "Por que a produção atrasou?", entity="Multiteiner", scope="Duque de Caxias")
    assert not scenario.decision_ready()


def test_scenario_is_ready_with_core_supported_lenses():
    scenario = DiagnosticScenarioEngine().create("S-002", "Por que a produção atrasou?")
    scenario = replace(scenario, observations=(
        DiagnosticObservation(DiagnosticLens.OPERATIONAL, DiagnosticStatus.SUPPORTED, "Atraso confirmado", ("e1",), 0.9),
        DiagnosticObservation(DiagnosticLens.CAUSAL, DiagnosticStatus.SUPPORTED, "Material crítico atrasou", ("e2",), 0.85),
        DiagnosticObservation(DiagnosticLens.EVIDENCE, DiagnosticStatus.SUPPORTED, "Evidências consistentes", ("e1", "e2"), 0.9),
    ))
    assert scenario.decision_ready()


def test_conflicting_evidence_blocks_decision():
    scenario = DiagnosticScenarioEngine().create("S-003", "Qual é a causa do atraso?")
    scenario = replace(scenario, observations=(
        DiagnosticObservation(DiagnosticLens.OPERATIONAL, DiagnosticStatus.SUPPORTED, "Atraso", ("e1",), 0.9),
        DiagnosticObservation(DiagnosticLens.CAUSAL, DiagnosticStatus.CONFLICTING, "Causas incompatíveis", ("e2", "e3"), 0.8),
        DiagnosticObservation(DiagnosticLens.EVIDENCE, DiagnosticStatus.SUPPORTED, "Evidência parcial", ("e1",), 0.9),
    ))
    assert scenario.has_conflict()
    assert not scenario.decision_ready()
    assert "conflitantes" in scenario.human_summary()


def test_human_summary_uses_first_person():
    scenario = DiagnosticScenarioEngine().create("S-004", "Qual o estado da operação?")
    assert scenario.human_summary().startswith("Eu ")
