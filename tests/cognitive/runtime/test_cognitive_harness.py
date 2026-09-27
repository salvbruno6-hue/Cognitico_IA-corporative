from __future__ import annotations

from elo.cognitive.runtime.cognitive_harness import (
    CognitiveHarness,
    CognitiveHarnessFixture,
    STAGE_ORDER,
)


def test_cognitive_harness_runs_all_ten_stages_and_reports_audit():
    report = CognitiveHarness().run(CognitiveHarnessFixture())

    assert report.stage_order == (
        "observe",
        "contextualize",
        "analyze",
        "formulate",
        "decide",
        "execute",
        "monitor",
        "learn",
        "follow_up",
        "reassess",
    )
    assert STAGE_ORDER == report.stage_order
    assert len(report.audit) == 10
    assert all(item["status"] == "ok" for item in report.audit)
    assert report.metrics["completed_stage_count"] == 10
    assert report.metrics["skipped_stage_count"] == 0
    assert report.metrics["error_stage_count"] == 0


def test_cognitive_harness_produces_delta_directives_and_human_response():
    fixture = CognitiveHarnessFixture(
        external_analysis="A análise contempla segurança.",
    )
    report = CognitiveHarness().run(fixture)

    assert report.delta["so_id"] == "FIXTURE-SO"
    assert report.delta["aligned"]
    assert report.delta["improvements"]
    assert report.directives
    assert report.human_response


def test_cognitive_harness_isolated_and_measurement_only():
    report = CognitiveHarness().run(CognitiveHarnessFixture())

    assert report.isolated is True
    assert report.metrics["network_access"] is False
    assert report.metrics["supabase_access"] is False
    assert report.metrics["mcp_access"] is False
    assert report.metrics["canonical_memory_write"] is False
    assert report.promotion_attempted is False
    assert report.metrics["promotion_attempted"] is False
    assert report.governance_decision == "MEASUREMENT_ONLY"
    assert report.stage_results["learning"]["promotion"] == "promotion_not_attempted"


def test_cognitive_harness_is_deterministic_for_same_fixture():
    fixture = CognitiveHarnessFixture()
    first = CognitiveHarness().run(fixture)
    second = CognitiveHarness().run(fixture)

    assert first.stage_order == second.stage_order
    assert first.audit == second.audit
    assert first.delta == second.delta
    assert first.directives == second.directives
    assert first.human_response == second.human_response
    assert first.metrics == second.metrics
