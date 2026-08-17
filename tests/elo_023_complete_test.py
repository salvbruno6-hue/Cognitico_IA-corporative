from pathlib import Path


def test_complete_package():
    assert Path('04-knowledge-handbook/MT001_COGNITIVE_CYCLE_TEST.md').exists()
    assert Path('04-knowledge-handbook/MT001_POST_CYCLE_REPORT.md').exists()
    assert Path('tests/elo_023_mt001_cycle_contract.md').exists()
    assert Path('tests/test_elo_023_mt001_contract.py').exists()
