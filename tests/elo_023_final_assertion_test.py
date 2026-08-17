from pathlib import Path


def test_final_assertion():
    text = Path('tests/elo_023_final_assertion.md').read_text(encoding='utf-8')
    assert 'preserve uncertainty' in text
    assert 'request missing specialist evidence' in text
    assert 'never promote company-specific facts to Core' in text
