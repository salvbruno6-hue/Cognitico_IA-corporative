from elo.agent_intake.hermes_tool_search_quality import (
    ToolSearchQualityCase,
    evaluate_task_quality,
)
from elo.agent_intake.hermes_tool_search_repeatability import (
    evaluate_repeatability,
)


def _quality_result(adapted="mcp_tool"):
    cases = (
        ToolSearchQualityCase("case-01", "session_search", "session_search", "session_search"),
        ToolSearchQualityCase("case-02", "computer_use", "computer_use", "computer_use"),
        ToolSearchQualityCase("case-03", "mcp_tool", "mcp_tool", adapted),
        ToolSearchQualityCase("case-04", "session_search", "session_search", "session_search"),
        ToolSearchQualityCase("case-05", "mcp_tool", "mcp_tool", "mcp_tool"),
    )
    return evaluate_task_quality(cases)


def test_repeatability_requires_stable_quality_across_three_runs():
    result = evaluate_repeatability(
        (_quality_result(), _quality_result(), _quality_result())
    )

    assert result.run_count == 3
    assert result.expected_run_count == 3
    assert result.stable_metrics is True
    assert result.all_runs_quality_equivalent is True
    assert result.repeatable is True
    assert result.candidate_only is True
    assert result.canonical_mutation is False


def test_repeatability_rejects_a_regressed_run():
    result = evaluate_repeatability(
        (_quality_result(), _quality_result("computer_use"), _quality_result())
    )

    assert result.stable_metrics is False
    assert result.all_runs_quality_equivalent is False
    assert result.repeatable is False


def test_repeatability_requires_minimum_number_of_runs():
    try:
        evaluate_repeatability((_quality_result(),))
    except ValueError as exc:
        assert "at least 3 results" in str(exc)
    else:
        raise AssertionError("expected ValueError")
