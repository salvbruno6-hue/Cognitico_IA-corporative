from elo.agent_intake.hermes_tool_search_quality import (
    ToolSearchQualityCase,
    evaluate_task_quality,
    result_as_metrics,
)


def _cases():
    return (
        ToolSearchQualityCase("case-01", "session_search", "session_search", "session_search"),
        ToolSearchQualityCase("case-02", "computer_use", "computer_use", "computer_use"),
        ToolSearchQualityCase("case-03", "mcp_tool", "mcp_tool", "mcp_tool"),
        ToolSearchQualityCase("case-04", "session_search", "session_search", "session_search"),
        ToolSearchQualityCase("case-05", "mcp_tool", "mcp_tool", "mcp_tool"),
    )


def test_task_quality_equivalence_without_regression():
    result = evaluate_task_quality(_cases())

    assert result.case_count == 5
    assert result.baseline_accuracy == 1.0
    assert result.adapted_accuracy == 1.0
    assert result.accuracy_delta == 0.0
    assert result.regressions == ()
    assert result.unreachable_cases == ()
    assert result.task_quality_equivalent is True
    assert result.candidate_only is True
    assert result.canonical_mutation is False


def test_quality_failure_when_adapted_selection_regresses():
    cases = list(_cases())
    cases[2] = ToolSearchQualityCase(
        "case-03", "mcp_tool", "mcp_tool", "computer_use"
    )

    result = evaluate_task_quality(cases)

    assert result.baseline_accuracy == 1.0
    assert result.adapted_accuracy == 0.8
    assert result.regressions == ("case-03",)
    assert result.task_quality_equivalent is False


def test_quality_failure_when_selected_tool_is_unreachable():
    cases = list(_cases())
    cases[1] = ToolSearchQualityCase(
        "case-02", "computer_use", "computer_use", "computer_use",
        adapted_reachable=False,
    )

    result = evaluate_task_quality(cases)

    assert result.unreachable_cases == ("case-02",)
    assert result.task_quality_equivalent is False


def test_metrics_can_feed_existing_candidate_measurement():
    result = evaluate_task_quality(_cases())

    assert result_as_metrics(result) == {
        "selection_accuracy": 1.0,
        "baseline_selection_accuracy": 1.0,
        "accuracy_delta": 0.0,
    }
