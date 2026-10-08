from datetime import datetime, timezone

import pytest

from elo.core.decision_ledger import (
    DecisionLedgerContractError,
    DecisionLedgerEvent,
    project_lifecycle,
    transition_to_event,
)
from elo.core.decision_outcome_loop import DecisionLifecycle, DecisionState
from elo.core.systemic_primitives import DecisionRecord


def _lifecycle() -> DecisionLifecycle:
    return DecisionLifecycle(
        DecisionRecord(
            "d1",
            "replan",
            "capacity gap",
            expected_outcome="reduce delay",
        )
    )


def test_projection_reuses_existing_dol_transition_without_new_state():
    lifecycle = _lifecycle()
    transition = lifecycle.transition(DecisionState.APPROVED, actor="elo")

    event = transition_to_event(
        transition,
        event_id="evt-1",
        source_ref="github:issue:1",
        request_id="req-1",
        correlation_id="corr-1",
    )

    assert event.decision_id == "d1"
    assert event.state is DecisionState.APPROVED
    assert event.actor == "elo"
    assert event.source_ref == "github:issue:1"
    assert event.request_id == "req-1"
    assert event.correlation_id == "corr-1"


def test_project_lifecycle_is_read_only_and_preserves_order():
    lifecycle = _lifecycle()
    lifecycle.transition(DecisionState.APPROVED)
    lifecycle.transition(DecisionState.EXECUTED)
    lifecycle.transition(DecisionState.OBSERVING)

    events = project_lifecycle(
        lifecycle,
        event_id_factory=lambda transition: f"evt-{transition.to_state.value}",
    )

    assert [event.state for event in events] == [
        DecisionState.APPROVED,
        DecisionState.EXECUTED,
        DecisionState.OBSERVING,
    ]
    assert len(lifecycle.history) == 3


def test_terminal_evidence_requirement_is_preserved():
    with pytest.raises(DecisionLedgerContractError):
        DecisionLedgerEvent(
            event_id="evt-1",
            decision_id="d1",
            state=DecisionState.CLOSED,
            occurred_at=datetime.now(timezone.utc),
        )
