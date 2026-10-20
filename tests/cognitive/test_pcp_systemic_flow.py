from datetime import date, datetime

from elo.cognitive.pcp_systemic_flow import (
    DailyConstraintSnapshot,
    ELDayInput,
    MaterialRequirement,
    assess_assembly_realizability,
    assess_el_availability,
    assess_mix_component_requirement,
    assess_systemic_capacity,
    consolidate_material_aliases,
    find_first_constraint_date,
    project_el_cumulative,
)


def test_el_2_caps_planned_assembly_4_at_2():
    result = assess_assembly_realizability(
        4,
        el_before_consumption=2,
        nominal_capacity=4,
    )
    assert result.realizable_quantity == 2
    assert result.status == "LIMITADA"


def test_el_5_caps_recovery_plan_6_at_5_without_prior_release():
    result = assess_assembly_realizability(
        6,
        el_before_consumption=5,
        nominal_capacity=4,
        recovery=True,
        recovery_capacity=6,
    )
    assert result.realizable_quantity == 5


def test_recovery_with_el_6_still_respects_other_confirmed_constraints():
    result = assess_assembly_realizability(
        6,
        el_before_consumption=6,
        nominal_capacity=4,
        recovery=True,
        recovery_capacity=6,
        other_constraints={"fibra": 4, "qualidade": 5},
    )
    assert result.realizable_quantity == 4


def test_systemic_capacity_is_limited_by_fiber_when_all_four_require_roof():
    result = assess_systemic_capacity(
        4,
        {
            "estrutura": 4,
            "el": 4,
            "montagem": 4,
            "fibra": 2,
            "qualidade": 4,
        },
    )
    assert result.systemic_capacity == 2
    assert result.executable_quantity == 2
    assert result.limiting_constraints == ("fibra",)


def test_mix_uses_component_only_for_models_that_explicitly_require_it():
    result = assess_mix_component_requirement(
        "CUBA-P",
        {"M01": 10, "M02": 5, "M05": 5},
        {"M01": 0, "M02": 1, "M05": 0},
    )
    assert result.total_requirement == 5
    assert result.status == "CALCULADO"


def test_explicit_aliases_consolidate_without_double_counting():
    result = consolidate_material_aliases(
        [
            MaterialRequirement("PIR40", 10, "UN"),
            MaterialRequirement("MAT-PIR-40", 5, "UN"),
        ],
        {"PIR40": "MAT-PIR-40"},
    )
    assert len(result) == 1
    assert result[0].canonical_code == "MAT-PIR-40"
    assert result[0].quantity == 15
    assert set(result[0].source_codes) == {"PIR40", "MAT-PIR-40"}


def test_different_door_concepts_are_not_consolidated_without_explicit_alias():
    result = consolidate_material_aliases(
        [
            MaterialRequirement("COMP-KIT-PORTA-ALUMINIO", 1, "KIT"),
            MaterialRequirement("PORTA-SOCIAL-COMPLETA", 1, "UN"),
        ],
        {},
    )
    assert len(result) == 2


def test_structure_completed_today_but_released_tomorrow_is_not_el_today():
    result = assess_el_availability(
        completed_at=datetime(2026, 10, 20, 10, 0),
        released_at=datetime(2026, 10, 21, 8, 0),
        reference_at=datetime(2026, 10, 20, 17, 0),
    )
    assert result.available_in_el is False
    assert result.status == "AGUARDANDO_LIBERACAO"


def test_el_projection_is_cumulative_and_cannot_consume_more_than_available():
    result = project_el_cumulative(
        3,
        [
            ELDayInput(date(2026, 10, 20), 0, 4),
            ELDayInput(date(2026, 10, 21), 4, 4),
        ],
        minimum=3,
        target=4,
        maximum=5,
    )
    assert result[0].realizable_consumption == 3
    assert result[0].closing_balance == 0
    assert result[1].opening_balance == 0
    assert result[1].available_before_consumption == 4


def test_missing_consumption_for_a_demanded_model_blocks_definitive_requirement():
    result = assess_mix_component_requirement(
        "TELHA-FIBRA",
        {"M01": 10, "M02": 5},
        {"M01": 1, "M02": None},
    )
    assert result.total_requirement is None
    assert result.missing_models == ("M02",)
    assert result.status == "EVIDENCIA_INSUFICIENTE"


def test_first_constraint_date_returns_earliest_confirmed_shortage():
    result = find_first_constraint_date(
        [
            DailyConstraintSnapshot(
                date(2026, 10, 20), 4, {"estrutura": 4, "el": 4, "fibra": 4}
            ),
            DailyConstraintSnapshot(
                date(2026, 10, 21), 4, {"estrutura": 4, "el": 4, "fibra": 2}
            ),
            DailyConstraintSnapshot(
                date(2026, 10, 22), 4, {"estrutura": 3, "el": 4, "fibra": 4}
            ),
        ]
    )
    assert result.day == date(2026, 10, 21)
    assert result.resource == "fibra"
    assert result.deficit == 2
    assert result.status == "FIRST_CONSTRAINT_DATE"


def test_first_constraint_date_fails_closed_on_earlier_missing_evidence():
    result = find_first_constraint_date(
        [
            DailyConstraintSnapshot(
                date(2026, 10, 20), 4, {"estrutura": 4, "fibra": None}
            ),
            DailyConstraintSnapshot(
                date(2026, 10, 21), 4, {"estrutura": 4, "fibra": 2}
            ),
        ]
    )
    assert result.day == date(2026, 10, 20)
    assert result.status == "EVIDENCIA_INSUFICIENTE"
    assert result.missing_constraints == ("fibra",)
