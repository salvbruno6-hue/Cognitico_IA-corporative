from elo.core.diagnostic_scenarios import (
    DiagnosticMode,
    DiagnosticObservation,
    DiagnosticScenarioEngine,
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
