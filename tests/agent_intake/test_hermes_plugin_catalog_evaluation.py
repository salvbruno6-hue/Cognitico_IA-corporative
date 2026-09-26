from elo.agent_intake.hermes_plugin_catalog_evaluation import (
    FIXTURES,
    baseline_activate,
    governed_activate,
    evaluate,
)


def test_governed_catalog_requires_discovery_allowlist_and_provenance():
    assert governed_activate(FIXTURES[0])
    assert not governed_activate(FIXTURES[1])
    assert not governed_activate(FIXTURES[2])
    assert not governed_activate(FIXTURES[4])


def test_controlled_measurement_has_repeatable_gain_without_regression():
    result = evaluate()
    assert result.baseline_rate == 0.4
    assert result.adapted_rate == 1.0
    assert result.adapted_rate > result.baseline_rate
    assert result.repeatable
    assert result.regressions == ()


def test_baseline_is_measurable_and_distinct_from_adapted_policy():
    baseline = tuple(baseline_activate(item) for item in FIXTURES)
    adapted = tuple(governed_activate(item) for item in FIXTURES)
    assert baseline != adapted
