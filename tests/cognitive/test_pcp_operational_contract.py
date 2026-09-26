from elo.cognitive.pcp_operational_contract import (
    confront_materials,
    confront_operations,
    confront_plan_lines,
)


def test_plan_line_maps_planned_and_actual():
    result = confront_plan_lines(({
        "id": "L1",
        "quantidade_planejada": 100,
        "quantidade_produzida": 90,
    },))
    assert result[0].dimension == "PRODUCAO"
    assert result[0].variance == -10
    assert result[0].status == "CONFRONTADO"


def test_operation_missing_actual_stays_unlocated():
    result = confront_operations(({
        "id": "O1",
        "quantidade_planejada": 10,
        "quantidade_concluida": None,
    },))
    assert result[0].status == "NAO_LOCALIZADO"


def test_material_does_not_sum_allocated_and_purchased():
    result = confront_materials(({
        "id": "M1",
        "quantidade_bruta": 10,
        "quantidade_alocada": 6,
        "quantidade_comprada": 8,
    },))
    assert len(result) == 2
    assert {item.dimension for item in result} == {
        "MATERIAL_ALOCADO", "MATERIAL_COMPRADO",
    }
    assert all(item.variance in (-4, -2) for item in result)
