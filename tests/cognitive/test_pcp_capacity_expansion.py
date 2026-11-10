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


def test_aliases_are_not_merged_without_explicit_canonical_normalization():
    result = explode_mix_requirements(
        {"M01": 1},
        {"M01": {"PIR40": 14, "MAT-PIR-40": 1}},
        available_components={"PIR40": 0, "MAT-PIR-40": 0},
    )
    by_component = {item.component: item for item in result}
    assert by_component["PIR40"].gross_required == 14
    assert by_component["MAT-PIR-40"].gross_required == 1
    assert len(result) == 2


def test_aluminum_door_kit_and_complete_social_door_remain_distinct():
    result = explode_mix_requirements(
        {"M02": 1},
        {"M02": {"COMP-KIT-PORTA-ALUMINIO": 1, "PORTA_SOCIAL_COMPLETA": 1}},
        available_components={"COMP-KIT-PORTA-ALUMINIO": 0, "PORTA_SOCIAL_COMPLETA": 0},
    )
    by_component = {item.component: item for item in result}
    assert by_component["COMP-KIT-PORTA-ALUMINIO"].gross_required == 1
    assert by_component["PORTA_SOCIAL_COMPLETA"].gross_required == 1


def test_missing_bom_quantity_blocks_definitive_requirement():
    result = explode_mix_requirements(
        {"M01": 4},
        {"M01": {"TELHA_FIBRA": None}},
        available_components={"TELHA_FIBRA": 2},
    )
    assert result[0].status == "BOM_INCOMPLETA"
    assert result[0].gross_required is None
    assert result[0].net_required is None


def test_sufficient_stock_yields_zero_net_requirement():
    result = explode_mix_requirements(
        {"M01": 4},
        {"M01": {"PIR40": 14}},
        available_components={"PIR40": 56},
    )
    assert result[0].gross_required == 56
    assert result[0].net_required == 0
    assert result[0].status == "COBERTO"


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
        labor_constrained_resources=["ESTRUTURA"],
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


def test_missing_model_bom_blocks_full_expansion_even_if_other_model_has_bom():
    result = assess_capacity_expansion(
        5,
        {"ESTRUTURA": 5, "MONTAGEM": 5},
        demand_by_model={"M01": 3, "M02": 2},
        bom_by_model={"M01": {"PIR40": 14}},
        available_components={"PIR40": 42},
    )
    assert result.status == "EXPANSAO_BLOQUEADA"
    assert result.missing_model_boms == ("M02",)
    assert any(a.target == "M02" and a.action == "LOCALIZAR_BOM_MODELO" for a in result.actions)


def test_measured_increment_without_labor_causality_does_not_calculate_hiring():
    result = assess_capacity_expansion(
        6,
        {"ESTRUTURA": 4, "MONTAGEM": 6},
        worker_increment_capacity={"ESTRUTURA": 1},
    )
    action = next(a for a in result.actions if a.target == "ESTRUTURA")
    assert action.action == "VALIDAR_CAUSA_MAO_DE_OBRA"
    assert action.calculated_workers is None


def test_evidenced_labor_cause_and_marginal_gain_allow_conditional_headcount():
    result = assess_capacity_expansion(
        6,
        {"ESTRUTURA": 4, "MONTAGEM": 6},
        labor_constrained_resources=["ESTRUTURA"],
        worker_increment_capacity={"ESTRUTURA": 1},
    )
    action = next(a for a in result.actions if a.target == "ESTRUTURA")
    assert action.calculated_workers == 2
    assert result.canonical_mutation is False


def test_missing_component_stock_blocks_executable_expansion():
    result = assess_capacity_expansion(
        4,
        {"ESTRUTURA": 4, "MONTAGEM": 4},
        demand_by_model={"M01": 4},
        bom_by_model={"M01": {"PIR40": 14}},
    )
    assert result.status == "EXPANSAO_BLOQUEADA"
    assert any(
        action.target == "PIR40" and action.action == "CONSULTAR_ESTOQUE"
        for action in result.actions
    )
    assert result.canonical_mutation is False


def test_unverified_bom_consumption_blocks_executable_expansion():
    result = assess_capacity_expansion(
        4,
        {"ESTRUTURA": 4, "MONTAGEM": 4},
        demand_by_model={"M01": 4},
        bom_by_model={"M01": {"TELHA_FIBRA": None}},
        available_components={"TELHA_FIBRA": 10},
    )
    assert result.status == "EXPANSAO_BLOQUEADA"
    assert any(
        action.target == "TELHA_FIBRA"
        and action.action == "BLOQUEAR_QUANTIDADE_E_VALIDAR_BOM"
        for action in result.actions
    )
    assert result.canonical_mutation is False


def test_confirmed_material_coverage_does_not_block_plan():
    result = assess_capacity_expansion(
        4,
        {"ESTRUTURA": 4, "MONTAGEM": 4},
        demand_by_model={"M01": 4},
        bom_by_model={"M01": {"PIR40": 14}},
        available_components={"PIR40": 56},
    )
    assert result.status == "SEM_EXPANSAO_NECESSARIA"
