import pytest

from elo.cognitive.pcp_capacity_expansion import (
    assess_capacity_expansion,
    explode_mix_requirements,
)


def test_mix_explosion_respects_model_specific_components():
    result = explode_mix_requirements(
        {"M01": 10, "M02": 5},
        {
            "M01": {"PIR40": 14, "CUBA_P": 0},
            "M02": {"PIR40": 17, "CUBA_P": 1},
        },
        available_components={"PIR40": 100, "CUBA_P": 2},
    )
    by_component = {item.component: item for item in result}
    assert by_component["PIR40"].gross_required == 225
    assert by_component["PIR40"].net_required == 125
    assert by_component["CUBA_P"].gross_required == 5
    assert by_component["CUBA_P"].net_required == 3


def test_missing_bom_quantity_blocks_definitive_requirement():
    result = explode_mix_requirements(
        {"M01": 4},
        {"M01": {"TELHA_FIBRA": None}},
        available_components={"TELHA_FIBRA": 2},
    )
    assert result[0].status == "BOM_INCOMPLETA"
    assert result[0].gross_required is None
    assert result[0].net_required is None


def test_expansion_does_not_invent_headcount_without_marginal_productivity():
    result = assess_capacity_expansion(
        6,
        {"ESTRUTURA": 4, "MONTAGEM": 6, "FIBRA": 6},
        required_constraints=["ESTRUTURA", "MONTAGEM", "FIBRA"],
    )
    action = next(item for item in result.actions if item.target == "ESTRUTURA")
    assert action.action == "REVISAR_RECURSO_E_MEDIR_INCREMENTO"
    assert action.calculated_workers is None
    assert action.evidence_required == ("produtividade_marginal_por_colaborador",)


def test_expansion_can_calculate_workers_only_when_increment_is_explicit():
    result = assess_capacity_expansion(
        6,
        {"ESTRUTURA": 4, "MONTAGEM": 6, "FIBRA": 6},
        required_constraints=["ESTRUTURA", "MONTAGEM", "FIBRA"],
        worker_increment_capacity={"ESTRUTURA": 1},
    )
    action = next(item for item in result.actions if item.target == "ESTRUTURA")
    assert action.action == "AUMENTAR_CAPACIDADE_RECURSO"
    assert action.calculated_workers == 2


def test_material_shortage_generates_purchase_need_from_mix_and_stock():
    result = assess_capacity_expansion(
        4,
        {"ESTRUTURA": 4, "MONTAGEM": 4},
        demand_by_model={"M01": 4},
        bom_by_model={"M01": {"PIR40": 14}},
        available_components={"PIR40": 40},
    )
    purchase = next(item for item in result.actions if item.target == "PIR40")
    assert purchase.action == "EMITIR_NECESSIDADE_COMPRAS"
    assert purchase.required == 56
    assert purchase.gap == 16


def test_missing_required_capacity_blocks_expansion_instead_of_inferring():
    result = assess_capacity_expansion(
        6,
        {"ESTRUTURA": 6, "FIBRA": None},
        required_constraints=["ESTRUTURA", "FIBRA"],
    )
    assert result.status == "EXPANSAO_BLOQUEADA"
    assert any(item.target == "FIBRA" and item.action == "LOCALIZAR_CAPACIDADE" for item in result.actions)


def test_invalid_negative_mix_demand_is_rejected():
    with pytest.raises(ValueError):
        explode_mix_requirements({"M01": -1}, {"M01": {"PIR40": 14}})
