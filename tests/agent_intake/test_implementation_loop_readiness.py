from elo.agent_intake.hermes_current_extensions import build_candidate
from elo.agent_intake.implementation_loop_readiness import assess_loop_readiness
from elo.agent_intake.symbiont_adaptation import refine_capability


def _adaptation():
    return refine_capability(
        "HERMES-CONTEXT",
        {"controlled_test": True, "outcome": {"verified": True}},
    )


def _complete_kwargs():
    return {
        "metric_directions": {"accuracy": "maximize"},
        "repeatable": True,
        "provenance_refs": ("controlled-test:628",),
        "boundary_integrity": True,
        "evolution_gate_approved": True,
        "elo_authorized": True,
    }


def test_loop_entry_requires_complete_evidence():
    result = assess_loop_readiness(
        build_candidate("EXT-CONTEXTREF-HERMES"),
        _adaptation(),
        {"accuracy": 0.8},
        {"accuracy": 0.9},
        **_complete_kwargs(),
    )
    assert result.ready_for_loop is True
    assert result.missing == ()
    assert result.canonical_mutation is False


def test_loop_entry_accepts_complete_evidence_without_gain():
    result = assess_loop_readiness(
        build_candidate("EXT-CONTEXTREF-HERMES"),
        _adaptation(),
        {"accuracy": 0.8},
        {"accuracy": 0.8},
        **_complete_kwargs(),
    )
    assert result.ready_for_loop is True
    assert result.missing == ()


def test_loop_entry_blocks_missing_direction():
    kwargs = _complete_kwargs()
    kwargs["metric_directions"] = {}
    result = assess_loop_readiness(
        build_candidate("EXT-CONTEXTREF-HERMES"),
        _adaptation(),
        {"accuracy": 0.8},
        {"accuracy": 0.9},
        **kwargs,
    )
    assert result.ready_for_loop is False
    assert "metric_direction:accuracy" in result.missing


def test_loop_entry_blocks_regression_and_nonrepeatability():
    kwargs = _complete_kwargs()
    kwargs.update(repeatable=False, regressions=("scope",))
    result = assess_loop_readiness(
        build_candidate("EXT-CONTEXTREF-HERMES"),
        _adaptation(),
        {"accuracy": 0.8},
        {"accuracy": 0.9},
        **kwargs,
    )
    assert result.ready_for_loop is False
    assert "regression_free" in result.missing
    assert "repeatability" in result.missing


def test_loop_entry_accepts_directional_minimize_gain():
    kwargs = _complete_kwargs()
    kwargs["metric_directions"] = {"latency": "minimize"}
    result = assess_loop_readiness(
        build_candidate("EXT-CONTEXTREF-HERMES"),
        _adaptation(),
        {"latency": 10.0},
        {"latency": 8.0},
        **kwargs,
    )
    assert result.ready_for_loop is True
    assert result.missing == ()


def test_loop_entry_does_not_require_downstream_governance_approval():
    kwargs = _complete_kwargs()
    kwargs.update(evolution_gate_approved=False, elo_authorized=False)
    result = assess_loop_readiness(
        build_candidate("EXT-CONTEXTREF-HERMES"),
        _adaptation(),
        {"accuracy": 0.8},
        {"accuracy": 0.9},
        **kwargs,
    )
    assert result.ready_for_loop is True
    assert result.missing == ()


def test_loop_entry_blocks_missing_provenance_and_boundary():
    kwargs = _complete_kwargs()
    kwargs.update(provenance_refs=(), boundary_integrity=False)
    result = assess_loop_readiness(
        build_candidate("EXT-CONTEXTREF-HERMES"),
        _adaptation(),
        {"accuracy": 0.8},
        {"accuracy": 0.9},
        **kwargs,
    )
    assert result.ready_for_loop is False
    assert "provenance" in result.missing
    assert "boundary_integrity" in result.missing
