from elo.core.proactive_manifestation import (
    ManifestationLevel,
    ProactiveContext,
    evaluate_proactive_manifestation,
)


def test_high_relevance_suggests_help():
    result = evaluate_proactive_manifestation(
        ProactiveContext(True, 0.90, 0.90, 0.30, novelty=0.80)
    )
    assert result.level == ManifestationLevel.SUGGEST


def test_missing_context_is_silent():
    result = evaluate_proactive_manifestation(
        ProactiveContext(True, 0.95, 0.95, 0.20, context_sufficient=False)
    )
    assert result.level == ManifestationLevel.SILENT


def test_missing_capability_is_silent():
    result = evaluate_proactive_manifestation(
        ProactiveContext(True, 0.95, 0.95, 0.20, capability_available=False)
    )
    assert result.level == ManifestationLevel.SILENT


def test_repeated_low_novelty_is_silent():
    result = evaluate_proactive_manifestation(
        ProactiveContext(True, 0.90, 0.90, 0.20, novelty=0.10, repeated=True)
    )
    assert result.level == ManifestationLevel.SILENT


def test_high_impact_requires_authorization():
    result = evaluate_proactive_manifestation(
        ProactiveContext(True, 0.90, 0.90, 0.90, novelty=0.80)
    )
    assert result.level == ManifestationLevel.AUTHORIZE


def test_invalid_signal_fails_closed_with_error():
    try:
        evaluate_proactive_manifestation(ProactiveContext(True, 1.1, 0.9, 0.2))
    except ValueError as exc:
        assert "between 0 and 1" in str(exc)
    else:
        raise AssertionError("invalid signal must be rejected")
