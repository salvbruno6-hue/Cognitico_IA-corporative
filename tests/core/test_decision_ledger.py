import pytest

from elo.core.decision_outcome_loop import DecisionLifecycle, DecisionState
from elo.core.decision_ledger import DecisionLedger
from elo.core.systemic_primitives import DecisionRecord


def _lifecycle() -> DecisionLifecycle:
    return DecisionLifecycle(
        DecisionRecord("d-ledger-1", "replan", "capacity gap", expected_outcome="reduce delay")
    )


def test_ledger_projects_real_lifecycle_transitions_only() -> None:
    lifecycle = _lifecycle()
    lifecycle.transition(DecisionState.APPROVED, evidence_ids=("e1",), actor="elo")
    lifecycle.transition(DecisionState.EXECUTED, evidence_ids=("e2",), actor="executor")

    ledger = DecisionLedger()
    records = ledger.append_lifecycle(lifecycle, correlation_id="c1", request_id="r1")

    assert [(r.from_state, r.to_state) for r in records] == [
        ("proposed", "approved"),
        ("approved", "executed"),
    ]
    assert all(r.decision_id == "d-ledger-1" for r in records)
    assert all(r.correlation_id == "c1" and r.request_id == "r1" for r in records)
    ledger.assert_matches_lifecycle(lifecycle)


def test_ledger_is_idempotent_for_same_lifecycle_history() -> None:
    lifecycle = _lifecycle()
    lifecycle.transition(DecisionState.APPROVED, evidence_ids=("e1",))
    ledger = DecisionLedger()

    first = ledger.append_lifecycle(lifecycle)
    second = ledger.append_lifecycle(lifecycle)

    assert len(first) == 1
    assert second == ()
    assert len(ledger.records) == 1


def test_ledger_does_not_authorize_or_change_lifecycle() -> None:
    lifecycle = _lifecycle()
    ledger = DecisionLedger()

    with pytest.raises(ValueError):
        ledger.assert_matches_lifecycle(lifecycle)

    assert lifecycle.state is DecisionState.PROPOSED
    assert ledger.records == ()
