from dataclasses import replace

from elo.core.diagnostic_scenarios import (
    DiagnosticLens,
    DiagnosticMode,
    DiagnosticObservation,
    DiagnosticScenarioEngine,
    DiagnosticStatus,
)


def obs(evidence_id, dimension, value, confidence=1.0):
    return DiagnosticObservation(evidence_id, dimension, value, f"evidência {evidence_id}", confidence)


def test_same_evidence_can_be_read_through_multiple_modes():
    report = DiagnosticScenarioEngine().diagnose(
        "production-delay",
        (
            obs("material-01", "materials", 0.95),
            obs("capacity-01", "capacity", 0.85),
        ),
        modes=(DiagnosticMode.BASELINE, DiagnosticMode.BOTTLENECK, DiagnosticMode.RISK),
    )
    assert report.by_mode(DiagnosticMode.BASELINE)
    assert report.by_mode(DiagnosticMode.BOTTLENECK)
    assert report.by_mode(DiagnosticMode.RISK)


def test_causal_mode_does_not_claim_causality_from_single_observation():
    report = DiagnosticScenarioEngine().diagnose(
        "single-signal",
        (obs("one", "materials", 0.95),),
        modes=(DiagnosticMode.CAUSAL,),
    )
    assert not report.by_mode(DiagnosticMode.CAUSAL)


def test_causal_mode_requires_multiple_signals_in_same_domain():
    report = DiagnosticScenarioEngine().diagnose(
        "multi-signal",
        (
            obs("one", "materials", 0.95),
            obs("two", "materials", 0.9),
        ),
        modes=(DiagnosticMode.CAUSAL,),
    )
    assert report.by_mode(DiagnosticMode.CAUSAL)[0].severity == "INVESTIGATE"


def test_low_confidence_is_preserved_as_uncertainty():
    report = DiagnosticScenarioEngine().diagnose(
        "uncertain",
        (obs("weak", "production", 0.9, 0.4),),
    )
    assert "weak: confiança abaixo de 0.6" in report.uncertainties


def test_engine_exposes_governed_multi_lenses():
    assert set(DiagnosticScenarioEngine.required_lenses()) == set(DiagnosticLens)


def test_scenario_is_not_ready_without_evidence():
    scenario = DiagnosticScenarioEngine().create(
        "S-001", "Por que a produção atrasou?", entity="Multiteiner", scope="Duque de Caxias"
    )
    assert not scenario.decision_ready()


def test_scenario_is_ready_with_core_supported_lenses():
    scenario = DiagnosticScenarioEngine().create("S-002", "Por que a produção atrasou?")
    scenario = replace(
        scenario,
        observations=(
            DiagnosticObservation("e1", "production", 0.9, "Atraso confirmado", 0.9, lens=DiagnosticLens.OPERATIONAL),
            DiagnosticObservation("e2", "materials", 0.9, "Material crítico atrasou", 0.85, lens=DiagnosticLens.CAUSAL),
            DiagnosticObservation("e1", "evidence", 0.9, "Evidências consistentes", 0.9, lens=DiagnosticLens.EVIDENCE),
        ),
    )
    assert scenario.decision_ready()


def test_conflicting_evidence_blocks_decision():
    scenario = DiagnosticScenarioEngine().create("S-003", "Qual é a causa do atraso?")
    scenario = replace(
        scenario,
        observations=(
            DiagnosticObservation("e1", "production", 0.9, "Atraso", 0.9, lens=DiagnosticLens.OPERATIONAL),
            DiagnosticObservation(
                "e2", "cause", 0.8, "Causa A", 0.8, lens=DiagnosticLens.CAUSAL,
                status=DiagnosticStatus.CONFLICTING,
            ),
            DiagnosticObservation("e3", "cause", 0.8, "Causa B", 0.8, lens=DiagnosticLens.CAUSAL),
            DiagnosticObservation("e1", "evidence", 0.9, "Evidência parcial", 0.9, lens=DiagnosticLens.EVIDENCE),
        ),
    )
    assert scenario.has_conflict()
    assert not scenario.decision_ready()
    assert "conflitantes" in scenario.human_summary()


def test_blocked_scenario_is_not_decision_ready():
    scenario = DiagnosticScenarioEngine().create("S-005", "Qual o estado da operação?")
    scenario = replace(
        scenario,
        observations=(
            DiagnosticObservation("e1", "governance", 0.9, "Bloqueio", 0.9, lens=DiagnosticLens.EVIDENCE, status=DiagnosticStatus.BLOCKED),
        ),
    )
    assert scenario.is_blocked()
    assert not scenario.decision_ready()


def test_human_summary_uses_first_person():
    scenario = DiagnosticScenarioEngine().create("S-004", "Qual o estado da operação?")
    assert scenario.human_summary().startswith("Eu ")
