from __future__ import annotations

from elo.cognitive.objective_continuity import (
    ObjectiveContinuityAdapter,
    ObjectiveLoopDecision,
    objective_execution_id,
)
from elo.cognitive.symbiont_execution import SymbiontExecutionStore
from elo.contracts.okr import Objective


def objective() -> Objective:
    return Objective(
        tenant_id="tenant-a",
        objective_id="obj-repeatable-flow",
        title="Persistir no objetivo até atingir o resultado",
        owner_ref="elo-cognitivo",
        evidence_refs=("evidence://objective/1",),
    )


def test_objective_checkpoint_survives_store_restart(tmp_path) -> None:
    path = str(tmp_path / "objective-loop.sqlite")
    obj = objective()

    store = SymbiontExecutionStore(path)
    adapter = ObjectiveContinuityAdapter(store)
    first = adapter.start_or_resume(obj, workstream_id="ws-a", initial_action="EXECUTE")
    cycle = adapter.record_cycle(
        obj,
        workstream_id="ws-a",
        expected_state_version=first.state_version,
        progress_token="processed:1",
        evidence_refs=("evidence://cycle/1",),
        proposed_next_action="EXECUTE",
    )
    execution_id = cycle.checkpoint.execution_id
    store.close()

    reopened = SymbiontExecutionStore(path)
    resumed = ObjectiveContinuityAdapter(reopened).start_or_resume(
        obj,
        workstream_id="ws-a",
        initial_action="EXECUTE",
    )
    assert resumed.execution_id == execution_id
    assert resumed.objective_id == obj.objective_id
    assert resumed.last_progress_token == "processed:1"
    assert resumed.iteration == 2
    reopened.close()


def test_no_progress_streak_survives_restart_and_triggers_replan(tmp_path) -> None:
    path = str(tmp_path / "stagnation.sqlite")
    obj = objective()
    store = SymbiontExecutionStore(path)
    adapter = ObjectiveContinuityAdapter(store)
    cp = adapter.start_or_resume(obj, workstream_id="ws-stall", initial_action="EXECUTE")

    first = adapter.record_cycle(
        obj,
        workstream_id="ws-stall",
        expected_state_version=cp.state_version,
        progress_token="same",
        evidence_refs=("evidence://stall/1",),
        proposed_next_action="EXECUTE",
    )
    second = adapter.record_cycle(
        obj,
        workstream_id="ws-stall",
        expected_state_version=first.checkpoint.state_version,
        progress_token="same",
        evidence_refs=("evidence://stall/2",),
        proposed_next_action="EXECUTE",
    )
    assert second.decision is ObjectiveLoopDecision.CORRECT
    assert second.no_progress_streak == 1
    store.close()

    reopened = SymbiontExecutionStore(path)
    resumed_adapter = ObjectiveContinuityAdapter(reopened)
    resumed = resumed_adapter.checkpoint(obj, workstream_id="ws-stall")
    third = resumed_adapter.record_cycle(
        obj,
        workstream_id="ws-stall",
        expected_state_version=resumed.state_version,
        progress_token="same",
        evidence_refs=("evidence://stall/3",),
        proposed_next_action="EXECUTE",
    )
    assert third.decision is ObjectiveLoopDecision.REPLAN
    assert third.no_progress_streak == 2
    reopened.close()


def test_progress_resets_stagnation_and_repetitive_flow_can_complete() -> None:
    obj = objective()
    store = SymbiontExecutionStore()
    adapter = ObjectiveContinuityAdapter(store)
    cp = adapter.start_or_resume(obj, workstream_id="ws-repeat", initial_action="PROCESS_BATCH")

    one = adapter.record_cycle(
        obj,
        workstream_id="ws-repeat",
        expected_state_version=cp.state_version,
        progress_token="batch:1",
        evidence_refs=("evidence://batch/1",),
        proposed_next_action="PROCESS_BATCH",
    )
    stalled = adapter.record_cycle(
        obj,
        workstream_id="ws-repeat",
        expected_state_version=one.checkpoint.state_version,
        progress_token="batch:1",
        evidence_refs=("evidence://batch/stall",),
        proposed_next_action="PROCESS_BATCH",
    )
    assert stalled.decision is ObjectiveLoopDecision.CORRECT

    progressed = adapter.record_cycle(
        obj,
        workstream_id="ws-repeat",
        expected_state_version=stalled.checkpoint.state_version,
        progress_token="batch:2",
        evidence_refs=("evidence://batch/2",),
        proposed_next_action="PROCESS_BATCH",
    )
    assert progressed.decision is ObjectiveLoopDecision.CONTINUE
    assert progressed.no_progress_streak == 0

    completed = adapter.record_cycle(
        obj,
        workstream_id="ws-repeat",
        expected_state_version=progressed.checkpoint.state_version,
        progress_token="batch:3",
        evidence_refs=("evidence://batch/3",),
        proposed_next_action="PROCESS_BATCH",
        objective_satisfied=True,
    )
    assert completed.decision is ObjectiveLoopDecision.COMPLETE
    assert completed.checkpoint.status == "COMPLETED"
    assert completed.checkpoint.next_action == "COMPLETED"
    store.close()


def test_persistent_stagnation_escalates_instead_of_looping_forever() -> None:
    obj = objective()
    store = SymbiontExecutionStore()
    adapter = ObjectiveContinuityAdapter(store)
    cp = adapter.start_or_resume(obj, workstream_id="ws-escalate", initial_action="EXECUTE")

    result = None
    for index in range(5):
        result = adapter.record_cycle(
            obj,
            workstream_id="ws-escalate",
            expected_state_version=cp.state_version,
            progress_token="unchanged",
            evidence_refs=(f"evidence://unchanged/{index}",),
            proposed_next_action="EXECUTE",
        )
        cp = result.checkpoint

    assert result is not None
    assert result.decision is ObjectiveLoopDecision.ESCALATE
    assert result.no_progress_streak == 4
    assert result.checkpoint.status == "HUMAN_APPROVAL_REQUIRED"
    assert result.checkpoint.next_action == "HUMAN_APPROVAL_REQUIRED"
    store.close()


def test_stale_checkpoint_replay_is_blocked() -> None:
    obj = objective()
    store = SymbiontExecutionStore()
    adapter = ObjectiveContinuityAdapter(store)
    cp = adapter.start_or_resume(obj, workstream_id="ws-idempotent", initial_action="EXECUTE")

    adapter.record_cycle(
        obj,
        workstream_id="ws-idempotent",
        expected_state_version=cp.state_version,
        progress_token="progress:1",
        evidence_refs=("evidence://idempotent/1",),
        proposed_next_action="EXECUTE",
    )
    try:
        adapter.record_cycle(
            obj,
            workstream_id="ws-idempotent",
            expected_state_version=cp.state_version,
            progress_token="progress:1",
            evidence_refs=("evidence://idempotent/duplicate",),
            proposed_next_action="EXECUTE",
        )
    except ValueError as exc:
        assert "stale objective checkpoint replay blocked" in str(exc)
    else:
        raise AssertionError("stale checkpoint must not replay a completed logical cycle")
    store.close()


def test_workstreams_are_isolated_under_same_objective() -> None:
    obj = objective()
    store = SymbiontExecutionStore()
    adapter = ObjectiveContinuityAdapter(store)
    a = adapter.start_or_resume(obj, workstream_id="ws-a", initial_action="A")
    b = adapter.start_or_resume(obj, workstream_id="ws-b", initial_action="B")

    assert a.execution_id != b.execution_id
    assert a.execution_id == objective_execution_id(
        tenant_id=obj.tenant_id,
        objective_id=obj.objective_id,
        workstream_id="ws-a",
    )
    assert b.execution_id == objective_execution_id(
        tenant_id=obj.tenant_id,
        objective_id=obj.objective_id,
        workstream_id="ws-b",
    )
    store.close()
