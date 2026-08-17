from pathlib import Path

REPORT = Path('04-knowledge-handbook/MT001_POST_CYCLE_REPORT.md')


def test_mt001_post_cycle_report_preserves_conditional_state():
    text = REPORT.read_text(encoding='utf-8')
    assert 'INITIAL_CYCLE_COMPLETED_WITH_OPEN_FOLLOW_UP' in text
    assert '`CONDITIONAL`' in text
    assert 'Original exercise: preserved.' in text


def test_mt001_report_does_not_promote_case_specific_rules():
    text = REPORT.read_text(encoding='utf-8')
    assert 'not promoted to Core as company-specific rules' in text


def test_mt001_report_links_follow_up():
    text = REPORT.read_text(encoding='utf-8')
    assert 'Issue #137' in text
    assert 'Commercial, PCP, Assembly, Rental/Yard/Repair, HR and Logistics' in text
