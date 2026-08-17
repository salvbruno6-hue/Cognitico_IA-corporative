from pathlib import Path


def test_elo_023_execution_result_is_explicitly_conditional():
    text = Path('tests/elo_023_execution_result.md').read_text(encoding='utf-8')
    assert 'PASS for the cognitive contract at scenario-analysis level.' in text
    assert 'does not claim operational feasibility' in text
    assert 'Issue #137' in text
