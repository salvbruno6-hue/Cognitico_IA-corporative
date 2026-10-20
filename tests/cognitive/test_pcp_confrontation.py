from elo.cognitive.pcp_confrontation import (
    confront, confront_batch, summarize_status,
)


def test_confront_planned_actual():
    result = confront(
        dimension="CAPACIDADE",
        key="CT-001",
        planned=100,
        actual=90,
        variance=-10,
        evidence_ids=["E1"],
        impact="10h abaixo do planejado",
    )
    assert result.status == "CONFRONTADO"
    assert result.variance == -10
    assert result.evidence_ids == ("E1",)


def test_confront_does_not_infer_cause():
    result = confront(
        dimension="PRAZO",
        key="OP-001",
        planned=10,
        actual=13,
        variance=3,
    )
    assert result.status == "CONFRONTADO"
    assert result.cause_evidence_ids == ()


def test_missing_actual_is_explicit():
    result = confront(
        dimension="PRODUCAO",
        key="OP-001",
        planned=10,
        actual=None,
    )
    assert result.status == "NAO_LOCALIZADO"
    assert result.variance is None


def test_batch_and_summary():
    results = confront_batch([
        {"dimension": "DEMANDA", "key": "D1",
         "planned": 100, "actual": 110, "variance": 10},
        {"dimension": "MATERIAL", "key": "M1",
         "planned": 50, "actual": None},
    ])
    assert len(results) == 2
    assert summarize_status(results) == {
        "CONFRONTADO": 1,
        "NAO_LOCALIZADO": 1,
    }
