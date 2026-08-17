from pathlib import Path


def test_scenario_result_is_conditional():
    text = Path('tests/elo_023_scenario_result_test_2.md').read_text(encoding='utf-8')
    assert 'PASS for cognitive-contract behavior' in text
    assert 'operational feasibility remains conditional' in text
    assert 'Issue #137' in text
