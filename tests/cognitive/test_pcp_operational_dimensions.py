from elo.cognitive.pcp_operational_dimensions import (
    confront_capacity, confront_flow, confront_stock,
)


def test_capacity_mapping():
    result = confront_capacity(({
        "id": "C1", "quantidade_padrao": 100,
        "quantidade_disponivel": 80,
    },))
    assert result[0].dimension == "CAPACIDADE"
    assert result[0].variance == -20


def test_stock_mapping():
    result = confront_stock(({
        "id": "S1", "quantidade_reservada": 40,
        "quantidade_disponivel": 50,
    },))
    assert result[0].dimension == "ESTOQUE"
    assert result[0].variance == 10


def test_flow_requires_explicit_durations():
    result = confront_flow(({
        "id": "F1",
        "inicio": "2026-09-01",
        "fim": "2026-09-02",
    },))
    assert result[0].status == "NAO_LOCALIZADO"
    assert result[0].variance is None


def test_flow_uses_explicit_durations():
    result = confront_flow(({
        "id": "F1",
        "duracao_planejada": 8,
        "duracao_real": 10,
    },))
    assert result[0].variance == 2
