from datetime import date

import pytest

from elo.cognitive.pcp_systemic_capacity import (
    SystemicCapacityDay,
    assess_systemic_capacity,
    find_first_constraint_date,
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


def test_invalid_negative_capacity_is_rejected():
    with pytest.raises(ValueError):
        assess_systemic_capacity(4, {"FIBRA": -1})


def test_first_constraint_returns_earliest_confirmed_date():
    result = find_first_constraint_date(
        [
            SystemicCapacityDay(
                reference_date=date(2026, 10, 20),
                demand_modules=4,
                constraint_capacities={"ESTRUTURA": 4, "MONTAGEM": 4, "FIBRA": 4},
            ),
            SystemicCapacityDay(
                reference_date=date(2026, 10, 21),
                demand_modules=4,
                constraint_capacities={"ESTRUTURA": 4, "MONTAGEM": 4, "FIBRA": 2},
            ),
            SystemicCapacityDay(
                reference_date=date(2026, 10, 22),
                demand_modules=4,
                constraint_capacities={"ESTRUTURA": 1, "MONTAGEM": 4, "FIBRA": 4},
            ),
        ],
        required_constraints=["ESTRUTURA", "MONTAGEM", "FIBRA"],
    )

    assert result.status == "PRIMEIRA_RESTRICAO_CONFIRMADA"
    assert result.first_constraint_date == date(2026, 10, 21)
    assert result.limiting_constraints == ("FIBRA",)
    assert result.evidence_gap_date is None
    assert result.evaluated_dates == (date(2026, 10, 20), date(2026, 10, 21))


def test_earlier_missing_evidence_blocks_later_constraint_instead_of_skipping_gap():
    result = find_first_constraint_date(
        [
            SystemicCapacityDay(
                reference_date=date(2026, 10, 20),
                demand_modules=4,
                constraint_capacities={"ESTRUTURA": 4, "MONTAGEM": 4},
            ),
            SystemicCapacityDay(
                reference_date=date(2026, 10, 21),
                demand_modules=4,
                constraint_capacities={"ESTRUTURA": 4, "MONTAGEM": 4, "FIBRA": 2},
            ),
        ],
        required_constraints=["ESTRUTURA", "MONTAGEM", "FIBRA"],
    )

    assert result.status == "EVIDENCIA_INSUFICIENTE"
    assert result.first_constraint_date is None
    assert result.evidence_gap_date == date(2026, 10, 20)
    assert result.missing_constraints == ("FIBRA",)
    assert result.evaluated_dates == (date(2026, 10, 20),)


def test_empty_constraint_evidence_is_fail_closed_before_later_constraint():
    result = find_first_constraint_date(
        [
            SystemicCapacityDay(
                reference_date=date(2026, 10, 20),
                demand_modules=4,
                constraint_capacities={},
            ),
            SystemicCapacityDay(
                reference_date=date(2026, 10, 21),
                demand_modules=4,
                constraint_capacities={"EL": 1, "MONTAGEM": 4},
            ),
        ],
        required_constraints=["EL", "MONTAGEM"],
    )

    assert result.status == "EVIDENCIA_INSUFICIENTE"
    assert result.evidence_gap_date == date(2026, 10, 20)
    assert result.missing_constraints == ("EL", "MONTAGEM")


def test_first_constraint_preserves_multiple_tied_constraints_on_same_date():
    result = find_first_constraint_date(
        [
            SystemicCapacityDay(
                reference_date=date(2026, 10, 20),
                demand_modules=6,
                constraint_capacities={"EL": 3, "FIBRA": 3, "MONTAGEM": 6},
            )
        ],
        required_constraints=["EL", "FIBRA", "MONTAGEM"],
    )

    assert result.status == "PRIMEIRA_RESTRICAO_CONFIRMADA"
    assert result.first_constraint_date == date(2026, 10, 20)
    assert result.limiting_constraints == ("EL", "FIBRA")


def test_complete_series_without_bottleneck_returns_no_confirmed_constraint():
    result = find_first_constraint_date(
        [
            SystemicCapacityDay(
                reference_date=date(2026, 10, 20),
                demand_modules=4,
                constraint_capacities={"EL": 5, "MONTAGEM": 4},
            ),
            SystemicCapacityDay(
                reference_date=date(2026, 10, 21),
                demand_modules=3,
                constraint_capacities={"EL": 3, "MONTAGEM": 4},
            ),
        ],
        required_constraints=["EL", "MONTAGEM"],
    )

    assert result.status == "SEM_RESTRICAO_CONFIRMADA"
    assert result.first_constraint_date is None
    assert result.evidence_gap_date is None
    assert result.missing_constraints == ()
    assert result.evaluated_dates == (date(2026, 10, 20), date(2026, 10, 21))


def test_empty_daily_series_is_indeterminate_not_no_constraint():
    result = find_first_constraint_date(
        [],
        required_constraints=["EL", "MONTAGEM"],
    )

    assert result.status == "EVIDENCIA_INSUFICIENTE"
    assert result.first_constraint_date is None
    assert result.evidence_gap_date is None
    assert result.missing_constraints == ("EL", "MONTAGEM")


def test_first_constraint_requires_explicit_constraint_universe():
    with pytest.raises(ValueError):
        find_first_constraint_date([], required_constraints=[])


def test_first_constraint_rejects_duplicate_or_unsorted_dates():
    day = SystemicCapacityDay(
        reference_date=date(2026, 10, 20),
        demand_modules=4,
        constraint_capacities={"EL": 4},
    )
    with pytest.raises(ValueError):
        find_first_constraint_date(
            [day, day],
            required_constraints=["EL"],
        )
