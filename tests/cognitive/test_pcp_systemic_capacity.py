from datetime import date

import pytest

from elo.cognitive.pcp_systemic_capacity import (
    DailyConstraintSnapshot,
    assess_systemic_capacity,
    first_constraint_date,
    project_el,
)


def test_el_two_caps_planned_assembly_four_at_two():
    result = assess_systemic_capacity(4, {"EL": 2, "MONTAGEM": 4})
    assert result.executable_modules == 2
    assert result.limiting_constraints == ("EL",)


def test_recovery_six_cannot_consume_more_than_el_five_without_prior_release():
    projection = project_el(5, [0], [6])
    assert projection[0].realizable_assembly == 5
    assert projection[0].closing_el == 0


def test_systemic_capacity_is_limited_by_fiber_when_all_four_modules_require_telha():
    result = assess_systemic_capacity(
        4,
        {"ESTRUTURA": 4, "MONTAGEM": 4, "FIBRA": 2},
        required_constraints=["ESTRUTURA", "MONTAGEM", "FIBRA"],
    )
    assert result.executable_modules == 2
    assert result.limiting_constraints == ("FIBRA",)


def test_missing_required_constraint_blocks_instead_of_inventing_capacity():
    result = assess_systemic_capacity(
        4,
        {"ESTRUTURA": 4, "MONTAGEM": 4, "FIBRA": None},
        required_constraints=["ESTRUTURA", "MONTAGEM", "FIBRA"],
    )
    assert result.executable_modules is None
    assert result.status == "ANALISE_BLOQUEADA"
    assert result.missing_constraints == ("FIBRA",)


def test_el_projection_is_cumulative_across_days():
    projection = project_el(3, [4, 4, 0], [4, 4, 4])
    assert [day.opening_el for day in projection] == [3, 3, 3]
    assert [day.realizable_assembly for day in projection] == [4, 4, 3]
    assert [day.closing_el for day in projection] == [3, 3, 0]


def test_first_constraint_date_reuses_systemic_capacity_and_returns_first_break():
    d1 = date(2026, 10, 23)
    d2 = date(2026, 10, 24)
    result = first_constraint_date(
        requested_by_day={d1: 4, d2: 4},
        snapshots=(
            DailyConstraintSnapshot(
                d1,
                {"ESTRUTURA": 4, "FIBRA": 4},
                ("ESTRUTURA", "FIBRA"),
            ),
            DailyConstraintSnapshot(
                d2,
                {"ESTRUTURA": 4, "FIBRA": 2},
                ("ESTRUTURA", "FIBRA"),
            ),
        ),
    )

    assert result.day == d2
    assert result.resource_codes == ("FIBRA",)
    assert result.executable_quantity == 2
    assert result.status == "PRIMEIRA_RESTRICAO"


def test_first_constraint_date_fails_closed_when_snapshot_is_missing():
    d1 = date(2026, 10, 23)
    result = first_constraint_date(requested_by_day={d1: 4}, snapshots=())
    assert result.day == d1
    assert result.executable_quantity is None
    assert result.status == "EVIDENCIA_INSUFICIENTE"


def test_invalid_negative_capacity_is_rejected():
    with pytest.raises(ValueError):
        assess_systemic_capacity(4, {"FIBRA": -1})
