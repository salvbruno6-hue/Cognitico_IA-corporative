from datetime import date

import pytest

from elo.cognitive.pcp_systemic_planning import (
    ConstraintEvidence,
    DailyConstraintSnapshot,
    assess_systemic_capacity,
    explode_mix_requirements,
    first_constraint_date,
    plan_cross_domain_handoffs,
    project_el,
)


def test_el_limits_assembly_when_stock_is_two_and_plan_is_four():
    day = date(2026, 10, 23)
    result = project_el(
        initial_el=2,
        releases_by_day={day: 0},
        planned_consumption_by_day={day: 4},
        min_level=3,
        target_level=4,
        max_level=5,
    )

    assert result.days[0].realizable_consumption == 2
    assert result.days[0].el_final == 0
    assert result.status == "RISCO_RUPTURA"


def test_el_five_caps_recovery_plan_six_without_prior_release():
    day = date(2026, 10, 23)
    result = project_el(
        initial_el=5,
        releases_by_day={day: 0},
        planned_consumption_by_day={day: 6},
        min_level=3,
        target_level=4,
        max_level=5,
    )

    assert result.days[0].realizable_consumption == 5
    assert result.days[0].el_final == 0


def test_systemic_capacity_checks_other_constraints_even_with_el_six():
    result = assess_systemic_capacity(
        6,
        (
            ConstraintEvidence("EL", 6, 6, "modulos", "ev-el"),
            ConstraintEvidence("MONTAGEM", 6, 6, "modulos", "ev-montagem"),
            ConstraintEvidence("FIBRA", 6, 4, "telhas", "ev-fibra"),
        ),
    )

    assert result.status == "LIMITADO"
    assert result.executable_quantity == 4
    assert result.limiting_constraints == ("FIBRA",)


def test_fiber_limits_complete_capacity_to_two_when_all_models_need_roof():
    result = assess_systemic_capacity(
        4,
        (
            ConstraintEvidence("ESTRUTURA", 4, 4, "modulos", "ev-estrutura"),
            ConstraintEvidence("EL", 4, 4, "modulos", "ev-el"),
            ConstraintEvidence("MONTAGEM", 4, 4, "modulos", "ev-montagem"),
            ConstraintEvidence("TELHA_FIBRA", 4, 2, "telhas", "ev-fibra"),
        ),
    )

    assert result.executable_quantity == 2
    assert result.limiting_constraints == ("TELHA_FIBRA",)


def test_mix_does_not_apply_basin_to_models_without_basin():
    result = explode_mix_requirements(
        {"M01": 15, "M02": 5},
        {
            "M01": {"PIR40": 14},
            "M02": {"PIR40": 17, "CUBA_P": 1},
        },
    )

    assert result.requirements["CUBA_P"] == 5
    assert result.requirements["PIR40"] == 295
    assert result.status == "COMPLETO"


def test_aliases_are_not_merged_without_explicit_normalization():
    result = explode_mix_requirements(
        {"M01": 1},
        {"M01": {"PIR40": 14, "MAT-PIR-40": 1}},
    )

    assert result.requirements["PIR40"] == 14
    assert result.requirements["MAT-PIR-40"] == 1
    assert len(result.requirements) == 2


def test_porta_aluminio_kit_and_social_door_remain_distinct():
    result = explode_mix_requirements(
        {"M02": 1},
        {"M02": {"COMP-KIT-PORTA-ALUMINIO": 1, "PORTA_SOCIAL_COMPLETA": 1}},
    )

    assert result.requirements["COMP-KIT-PORTA-ALUMINIO"] == 1
    assert result.requirements["PORTA_SOCIAL_COMPLETA"] == 1


def test_same_day_structure_completion_does_not_enter_el_without_release_event():
    day = date(2026, 10, 23)
    result = project_el(
        initial_el=0,
        releases_by_day={day: 0},
        planned_consumption_by_day={day: 4},
        min_level=3,
        target_level=4,
        max_level=5,
    )

    assert result.days[0].realizable_consumption == 0


def test_missing_material_consumption_keeps_systemic_capacity_inconclusive():
    result = assess_systemic_capacity(
        4,
        (
            ConstraintEvidence("ESTRUTURA", 4, 4, "modulos", "ev-estrutura"),
            ConstraintEvidence("MATERIAL_X", None, None, "kg", "ev-material"),
        ),
    )

    assert result.status == "EVIDENCIA_INSUFICIENTE"
    assert result.executable_quantity is None
    assert result.missing_constraints == ("MATERIAL_X",)


def test_missing_bom_model_produces_partial_requirement_not_invention():
    result = explode_mix_requirements(
        {"M01": 10, "M99": 3},
        {"M01": {"PIR40": 14}},
    )

    assert result.requirements == {"PIR40": 140}
    assert result.missing_models == ("M99",)
    assert result.status == "PARCIAL"


def test_first_constraint_date_returns_first_future_break():
    d1 = date(2026, 10, 23)
    d2 = date(2026, 10, 24)
    result = first_constraint_date(
        requested_by_day={d1: 4, d2: 4},
        snapshots=(
            DailyConstraintSnapshot(
                d1,
                (
                    ConstraintEvidence("ESTRUTURA", 4, 4, "modulos", "ev-e1"),
                    ConstraintEvidence("FIBRA", 4, 4, "telhas", "ev-f1"),
                ),
            ),
            DailyConstraintSnapshot(
                d2,
                (
                    ConstraintEvidence("ESTRUTURA", 4, 4, "modulos", "ev-e2"),
                    ConstraintEvidence("FIBRA", 4, 2, "telhas", "ev-f2"),
                ),
            ),
        ),
    )

    assert result.day == d2
    assert result.resource_codes == ("FIBRA",)
    assert result.executable_quantity == 2
    assert result.status == "PRIMEIRA_RESTRICAO"


def test_handoff_does_not_authorize_purchase_or_hiring():
    handoffs = plan_cross_domain_handoffs(
        demand_increased=True,
        material_shortage=True,
        capacity_shortage=True,
        labor_capacity_evidence=True,
        parallel_flow_shortage=True,
        evidence_refs=("ev-demand", "ev-capacity"),
    )

    assert {item.domain for item in handoffs} == {
        "PCP",
        "COMPRAS_ALMOXARIFADO",
        "PRODUCAO_RH",
        "FLUXOS_PARALELOS",
    }
    assert all(item.authorized is False for item in handoffs)
    assert any(item.action == "EVALUATE_LABOR_AND_RESOURCE_SCENARIOS" for item in handoffs)


def test_unknown_shortages_request_evidence_instead_of_inventing_action_values():
    handoffs = plan_cross_domain_handoffs(
        demand_increased=True,
        material_shortage=None,
        capacity_shortage=None,
        labor_capacity_evidence=False,
        parallel_flow_shortage=None,
        evidence_refs=("ev-demand",),
    )

    actions = {item.action for item in handoffs}
    assert "COLLECT_STOCK_RESERVATION_OPEN_ORDER_AND_LEAD_TIME_EVIDENCE" in actions
    assert "COLLECT_CAPACITY_EVIDENCE" in actions
    assert "COLLECT_COMPONENT_AVAILABILITY_EVIDENCE" in actions


def test_negative_values_are_rejected():
    with pytest.raises(ValueError):
        assess_systemic_capacity(
            4,
            (ConstraintEvidence("EL", 4, -1, "modulos", "ev"),),
        )
