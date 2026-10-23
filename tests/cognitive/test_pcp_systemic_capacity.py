from datetime import date, datetime, timezone

import pytest

from elo.cognitive.pcp_systemic_capacity import (
    DailyConstraintSnapshot,
    ELOperationalEvent,
    assess_el_event_balance,
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


def test_el_event_balance_uses_only_explicit_canonical_events():
    events = (
        ELOperationalEvent("ENTRADA_EL", 5, datetime(2026, 10, 23, 8, tzinfo=timezone.utc), "ev-1"),
        ELOperationalEvent("BLOQUEIO", 1, datetime(2026, 10, 23, 9, tzinfo=timezone.utc), "ev-2"),
        ELOperationalEvent("SAIDA_EL", 2, datetime(2026, 10, 23, 10, tzinfo=timezone.utc), "ev-3"),
        ELOperationalEvent("DESBLOQUEIO", 1, datetime(2026, 10, 23, 11, tzinfo=timezone.utc), "ev-4"),
    )

    result = assess_el_event_balance(events)

    assert result.available_quantity == 3
    assert result.blocked_quantity == 0
    assert result.entered_quantity == 5
    assert result.exited_quantity == 2
    assert result.blocked_total == 1
    assert result.unblocked_total == 1
    assert result.status == "SALDO_EL_POR_EVENTOS"
    assert result.evidence_refs == ("ev-1", "ev-2", "ev-3", "ev-4")


def test_el_event_balance_respects_as_of_cutoff():
    events = (
        ELOperationalEvent("ENTRADA_EL", 3, datetime(2026, 10, 23, 8, tzinfo=timezone.utc)),
        ELOperationalEvent("ENTRADA_EL", 2, datetime(2026, 10, 24, 8, tzinfo=timezone.utc)),
    )

    result = assess_el_event_balance(
        events,
        as_of=datetime(2026, 10, 23, 23, 59, tzinfo=timezone.utc),
    )

    assert result.available_quantity == 3
    assert result.event_count == 1


def test_structure_completion_is_not_an_el_event_type():
    with pytest.raises(ValueError, match="unsupported EL event type"):
        assess_el_event_balance(
            (
                ELOperationalEvent(
                    "ESTRUTURA_CONCLUIDA",
                    1,
                    datetime(2026, 10, 23, 8, tzinfo=timezone.utc),
                ),
            )
        )


def test_el_event_sequence_fails_closed_when_stock_is_impossible():
    with pytest.raises(ValueError, match="SAIDA_EL cannot exceed available EL"):
        assess_el_event_balance(
            (
                ELOperationalEvent(
                    "SAIDA_EL",
                    1,
                    datetime(2026, 10, 23, 8, tzinfo=timezone.utc),
                ),
            )
        )

    with pytest.raises(ValueError, match="DESBLOQUEIO cannot exceed blocked EL"):
        assess_el_event_balance(
            (
                ELOperationalEvent(
                    "DESBLOQUEIO",
                    1,
                    datetime(2026, 10, 23, 8, tzinfo=timezone.utc),
                ),
            )
        )


def test_el_event_balance_without_events_does_not_invent_initial_stock():
    result = assess_el_event_balance(())
    assert result.available_quantity == 0
    assert result.event_count == 0
    assert result.status == "SEM_EVENTOS_EL"


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
