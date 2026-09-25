from scripts.run_hermes_candidate_analysis_view import analyze_waiting_candidates, render_markdown


def test_pretest_view_analyzes_gain_evolution_relationship_and_risk():
    rows = analyze_waiting_candidates()
    assert {row["candidate"] for row in rows} == {
        "EXT-CONTEXT-PLUGIN-HERMES",
        "EXT-WORKTREE-HERMES",
        "EXT-MULTIAGENT-HERMES",
        "EXT-CRON-HERMES",
    }
    assert all(row["owner"] for row in rows)
    assert all(row["relationship"] == "EVOLVE_EXISTING_OWNER" for row in rows)
    assert all(row["functional_overlap"] == "BOUNDARDED_BY_EXISTING_OWNER" for row in rows)
    assert all(row["governance_classification"] == "DUPLICATE/SUPERSEDED" for row in rows)
    assert all(row["competition_allowed"] is False for row in rows)
    assert all(row["duplicate_risk"] == "CONTROLLED_BY_EXISTING_GATE" for row in rows)
    assert all(row["supersession_candidate"] is False for row in rows)
    assert all(row["canonical_mutation"] is False for row in rows)
    assert all(row["promotion_authorized"] is False for row in rows)
    assert all(row["risk"] in {"LOW", "HIGH"} for row in rows)


def test_pretest_view_is_not_a_promotion_ranking():
    view = render_markdown(analyze_waiting_candidates())
    assert "prioridade de intervenção" in view
    assert "qualidade" in view
    assert "Evolution Gate" in view
    assert "Concorrência" in view
    assert "canonicalização" in view
