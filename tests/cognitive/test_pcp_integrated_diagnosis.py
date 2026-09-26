from elo.cognitive.pcp_confrontation import confront
from elo.cognitive.pcp_integrated_diagnosis import diagnose_confrontations


def test_integrated_diagnosis_aggregates_without_inference():
    items = (
        confront(
            dimension="CAPACIDADE", key="CT-001",
            planned=100, actual=90, variance=-10,
            evidence_ids=("E1",), impact="capacidade abaixo do plano",
        ),
        confront(
            dimension="MATERIAL", key="MAT-001",
            planned=50, actual=40, variance=-10,
            evidence_ids=("E2",),
        ),
    )
    result = diagnose_confrontations(items)
    assert result.status == "DIAGNOSTICO_CONFRONTADO"
    assert result.total == 2
    assert result.confronted == 2
    assert result.not_located == 0
    assert result.dimensions == ("CAPACIDADE", "MATERIAL")
    assert result.evidence_ids == ("E1", "E2")


def test_integrated_diagnosis_preserves_missing_data():
    result = diagnose_confrontations((
        confront(
            dimension="PRAZO", key="OP-001",
            planned=10, actual=None,
        ),
    ))
    assert result.status == "DADOS_INCOMPLETOS"
    assert result.not_located == 1
    assert result.evidence_ids == ()


def test_empty_diagnosis():
    result = diagnose_confrontations(())
    assert result.status == "SEM_DADOS"
