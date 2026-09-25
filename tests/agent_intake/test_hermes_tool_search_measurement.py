from elo.agent_intake.hermes_tool_search_measurement import measure_footprint


def test_progressive_disclosure_reduces_controlled_schema_footprint():
    result = measure_footprint(
        eager_schemas=("A" * 100, "B" * 100, "C" * 100),
        deferred_schemas=("A" * 100, "B" * 100),
        selected_tool_schema="C" * 100,
    )
    assert result.eager_chars == result.progressive_chars
    assert result.selected_tool_present is False


def test_progressive_disclosure_reduces_when_catalog_is_compact():
    result = measure_footprint(
        eager_schemas=("A" * 100, "B" * 100, "C" * 100),
        deferred_schemas=("A" * 10, "B" * 10),
        selected_tool_schema="C" * 10,
    )
    assert result.eager_chars == 300
    assert result.progressive_chars == 30
    assert result.reduction_chars == 270
    assert result.reduction_ratio == 0.9


def test_selected_tool_reachability_is_explicit():
    result = measure_footprint(
        eager_schemas=("A", "B"),
        deferred_schemas=("A", "B"),
        selected_tool_schema="B",
    )
    assert result.selected_tool_present is True
