from scripts.run_hermes_candidate_analysis_view import analyze_waiting_candidates, render_markdown

def test_pretest_view_analyzes_gain_evolution_relationship_and_risk():
    rows = analyze_waiting_candidates()
    assert {row['candidate'] for row in rows} == {
        'EXT-CONTEXT-PLUGIN-HERMES', 'EXT-WORKTREE-HERMES',
        'EXT-MULTIAGENT-HERMES', 'EXT-CRON-HERMES',
    }
    assert all('owner' in row and row['owner'] for row in rows)
    assert all('relationship' in row and row['relationship'] for row in rows)
    assert all(row['canonical_mutation'] is False for row in rows)
    assert all(row['risk'] in {'LOW', 'HIGH'} for row in rows)

def test_pretest_view_is_not_a_promotion_ranking():
    view = render_markdown(analyze_waiting_candidates())
    assert 'prioridade de intervenção' in view
    assert 'qualidade' in view
    assert 'canonicalização' in view