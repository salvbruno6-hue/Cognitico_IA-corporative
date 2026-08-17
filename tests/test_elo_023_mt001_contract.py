from pathlib import Path

SCENARIO = Path('04-knowledge-handbook/MT001_COGNITIVE_CYCLE_TEST.md')
MATRIX = Path('tests/elo_023_mt001_cycle_contract.md')


def test_mt001_scenario_and_matrix_exist():
    assert SCENARIO.exists()
    assert MATRIX.exists()


def test_mt001_preserves_missing_data_as_gaps():
    text = SCENARIO.read_text(encoding='utf-8')
    assert 'M14 assembly time: not supplied' in text
    assert 'must NOT infer' in text
    assert 'exact available quantity among the 100 returns' in text
    assert 'exact CLT deficit' in text


def test_mt001_separates_committed_from_available():
    text = SCENARIO.read_text(encoding='utf-8')
    assert 'already committed' in text
    assert 'cannot be counted as seasonal availability' in text


def test_mt001_preserves_experience_and_promotion_boundary():
    text = SCENARIO.read_text(encoding='utf-8')
    assert 'remains a Forge/contextual experience' in text
    assert 'No case-specific number or conclusion is promoted to Core' in text


def test_mt001_follow_up_and_provenance_rules():
    text = SCENARIO.read_text(encoding='utf-8')
    assert 'WAITING_FEEDBACK' in text
    assert 'origin field must contain only the source excerpt or source reference' in text
    assert 'does not overwrite the original exercise' in text
