from elo.cognitive.pcp_deadline_quality import confront_deadlines, confront_quality


def test_deadline_keeps_dates_and_requires_explicit_status():
    result = confront_deadlines(({
        "id": "P1",
        "data_prometida": "2026-09-10",
        "data_entrega": "2026-09-12",
    },))
    assert result[0].planned == "2026-09-10"
    assert result[0].actual == "2026-09-12"
    assert result[0].variance is None


def test_deadline_uses_explicit_on_time_fact():
    result = confront_deadlines(({
        "id": "P1",
        "data_prometida": "2026-09-10",
        "data_entrega": "2026-09-12",
        "no_prazo": False,
    },))
    assert result[0].variance == 1


def test_quality_fpy_requires_both_counts():
    result = confront_quality(({
        "id": "Q1",
        "aprovado_sem_retrabalho": 90,
        "total_concluido": 100,
        "fpy_planejado": 0.95,
    },))
    assert result[0].actual == 0.9
    assert result[0].variance == -0.05
