"""Lab wave for Hermes candidates currently waiting for governed evidence.

Reuses existing candidate evaluators. This test validates boundary integrity and
repeatability; it does not claim production evidence or promotion.
"""
from elo.agent_intake.hermes_context_plugin_evaluation import evaluate_context_plugin_candidate
from elo.agent_intake.hermes_worktree_evaluation import evaluate as evaluate_worktree
from elo.agent_intake.hermes_multiagent_evaluation import evaluate as evaluate_multiagent
from elo.agent_intake.hermes_cron_evaluation import evaluate as evaluate_cron


def test_waiting_candidates_wave_01_preserves_governance_boundaries():
    results = (
        evaluate_context_plugin_candidate(),
        evaluate_worktree(),
        evaluate_multiagent(),
        evaluate_cron(),
    )
    expected = {
        "EXT-CONTEXT-PLUGIN-HERMES",
        "EXT-WORKTREE-HERMES",
        "EXT-MULTIAGENT-HERMES",
        "EXT-CRON-HERMES",
    }
    assert {result.candidate_id if hasattr(result, "candidate_id") else (
        "EXT-WORKTREE-HERMES" if type(result).__name__ == "WorktreeEvaluation" else
        "EXT-MULTIAGENT-HERMES" if type(result).__name__ == "MultiagentEvaluation" else
        "EXT-CRON-HERMES"
    ) for result in results} == expected
    assert all(result.repeatable for result in results)
    assert all(result.boundary_integrity_rate == 1.0 for result in results)
    assert all(result.result in {"RETEST", "EVOLUTION_GATE_REQUIRED"} for result in results)


def test_waiting_candidates_wave_01_does_not_promote():
    results = (
        evaluate_context_plugin_candidate(),
        evaluate_worktree(),
        evaluate_multiagent(),
        evaluate_cron(),
    )
    assert all(result.result != "IMPLEMENTATION_AUTHORIZED" for result in results)
