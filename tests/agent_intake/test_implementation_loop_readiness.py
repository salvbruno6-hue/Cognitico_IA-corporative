from elo.agent_intake.hermes_current_extensions import build_candidate
from elo.agent_intake.implementation_loop_readiness import assess_loop_readiness
from elo.agent_intake.symbiont_adaptation import refine_capability


def _adaptation():
    return refine_capability(
        "HERMES-CONTEXT",
        {"controlled_test": True, "outcome": {"verified": True}},
    )


def test_loop_entry_requires_complete_evidence():
    result = assess_loop_readiness(
        build_candidate("EXT-CONTEXTREF-HERMES"),
        _adaptation(),
        {"accuracy": 0.8},
        {"accuracy": 0.9},
        metric_directions={"accuracy": "maximize"},
        repeatable=True,
    )
    assert result.ready_for_loop is True
    assert result.missing == ()
    assert result.canonical_mutation is False


def test_loop_entry_blocks_missing_gain():
    result = assess_loop_readiness(
        build_candidate("EXT-CONTEXTREF-HERMES"),
        _adaptation(),
        {"accuracy": 0.8},
        {"accuracy": 0.8},
        metric_directions={"accuracy": "maximize"},
        repeatable=True,
    )
    assert result.ready_for_loop is False
    assert "measured_gain" in result.missing


def test_loop_entry_blocks_missing_direction():
    result = assess_loop_readiness(
        build_candidate("EXT-CONTEXTREF-HERMES"),
        _adaptation(),
        {"accuracy": 0.8},
        {"accuracy": 0.9},
        metric_directions={},
        repeatable=True,
    )
    assert result.ready_for_loop is False
    assert "metric_direction:accuracy" in result.missing


def test_loop_entry_blocks_regression_and_nonrepeatability():
    result = assess_loop_readiness(
        build_candidate("EXT-CONTEXTREF-HERMES"),
        _adaptation(),
        {"accuracy": 0.8},
        {"accuracy": 0.9},
        metric_directions={"accuracy": "maximize"},
        repeatable=False,
        regressions=("scope",),
    )
    assert result.ready_for_loop is False
    assert "regression_free" in result.missing
    assert "repeatability" in result.missing


def test_loop_entry_accepts_directional_minimize_gain():
    result = assess_loop_readiness(
        build_candidate("EXT-CONTEXTREF-HERMES"),
        _adaptation(),
        {"latency": 10.0},
        {"latency": 8.0},
        metric_directions={"latency": "minimize"},
        repeatable=True,
    )
    assert result.ready_for_loop is True
    assert result.missing == ()
