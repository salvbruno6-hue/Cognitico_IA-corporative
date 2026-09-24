from src.elo.agent_intake.hermes_current_extensions import (
    CANDIDATES,
    build_candidate,
    evaluate_candidate,
)


def test_all_current_hermes_candidates_have_existing_elo_owners():
    assert len(CANDIDATES) == 15
    assert all(owner for _, _, owner, _ in CANDIDATES)
    assert len({candidate_id for candidate_id, *_ in CANDIDATES}) == len(CANDIDATES)


def test_candidates_are_candidate_only_and_non_mutating():
    for candidate_id, *_ in CANDIDATES:
        candidate = build_candidate(candidate_id)
        assert candidate.promotion_state == "candidate_only"
        assert candidate.canonical_mutation is False


def test_new_candidates_are_registered():
    expected = {
        "EXT-LEARN-HERMES",
        "EXT-LEARNING-GRAPH-HERMES",
        "EXT-CONTEXT-PLUGIN-HERMES",
        "EXT-WORKTREE-HERMES",
        "EXT-MULTIAGENT-HERMES",
        "EXT-CRON-HERMES",
        "EXT-MCP-HERMES",
    }
    assert expected.issubset({candidate_id for candidate_id, *_ in CANDIDATES})


def test_positive_repeatable_measurement_stops_at_evolution_gate():
    candidate = build_candidate("EXT-CONTEXTREF-HERMES")
    result = evaluate_candidate(candidate, {"precision": 0.70}, {"precision": 0.82}, repeatable=True, metric_directions={"precision": "maximize"})
    assert result.result == "EVOLUTION_GATE_REQUIRED"


def test_regression_is_rejected():
    candidate = build_candidate("EXT-CHECKPOINT-HERMES")
    result = evaluate_candidate(
        candidate,
        {"recovery": 0.90},
        {"recovery": 0.95},
        regressions=("mutation_boundary",),
        repeatable=True,
        metric_directions={"recovery": "maximize"},
    )
    assert result.result == "REJECT"


def test_non_repeatable_gain_requires_retest():
    candidate = build_candidate("EXT-BATCH-HERMES")
    result = evaluate_candidate(candidate, {"recall": 0.60}, {"recall": 0.70}, repeatable=False, metric_directions={"recall": "maximize"})
    assert result.result == "RETEST"
