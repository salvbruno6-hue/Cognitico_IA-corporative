from __future__ import annotations

from elo.cognitive.objective_continuity import ObjectiveContinuityAdapter, ObjectiveLoopDecision
from elo.cognitive.response.elo_gpt_dialogue import AuthorizationState, PersistenceState
from elo.cognitive.response.elo_gpt_dialogue_bridge import compose_objective_cycle_reply
from elo.cognitive.symbiont_execution import SymbiontExecutionStore
from elo.contracts.okr import Objective


def test_two_wakeups_preserve_checkpoint_and_drive_gpt_reply(tmp_path) -> None:
    path = str(tmp_path / "elo-gpt-dialogue.sqlite")
    objective = Objective(
        tenant_id="tenant-dialogue",
        objective_id="obj-dialogue-real",
        title="Provar continuidade ELO para GPT entre wakeups",
        owner_ref="elo-cognitivo",
        evidence_refs=("evidence://objective/dialogue-real",),
    )

    # Wakeup 1: ELO advances and tells GPT it may continue without a new chat approval.
    store = SymbiontExecutionStore(path)
    adapter = ObjectiveContinuityAdapter(store)
    first_checkpoint = adapter.start_or_resume(
        objective,
        workstream_id="chatgpt-dialogue",
        initial_action="EXECUTE_BOUNDED_STEP",
        max_cycles=6,
    )
    first_result = adapter.record_cycle(
        objective,
        workstream_id="chatgpt-dialogue",
        expected_state_version=first_checkpoint.state_version,
        progress_token="wakeup:1:progress",
        evidence_refs=("evidence://dialogue/wakeup-1",),
        proposed_next_action="EXECUTE_SECOND_BOUNDED_STEP",
    )
    assert first_result.decision is ObjectiveLoopDecision.CONTINUE

    first_reply = compose_objective_cycle_reply(
        first_result,
        persistence_state=PersistenceState.PERSISTED,
        authorization_state=AuthorizationState.VALID,
        continuation_permitted=True,
    )
    assert first_reply.should_continue_automatically is True
    assert first_reply.progress_token == "wakeup:1:progress"
    assert "sem solicitar nova autorização conversacional" in first_reply.message
    first_execution_id = first_result.checkpoint.execution_id
    first_state_version = first_result.checkpoint.state_version
    store.close()

    # Wakeup 2: a new process reopens the same durable store and must recover wakeup 1.
    store = SymbiontExecutionStore(path)
    adapter = ObjectiveContinuityAdapter(store)
    resumed = adapter.start_or_resume(
        objective,
        workstream_id="chatgpt-dialogue",
        initial_action="SHOULD_NOT_REPLACE_PERSISTED_NEXT_ACTION",
        max_cycles=6,
    )
    assert resumed.execution_id == first_execution_id
    assert resumed.state_version == first_state_version
    assert resumed.last_progress_token == "wakeup:1:progress"
    assert resumed.next_action == "EXECUTE_SECOND_BOUNDED_STEP"

    second_result = adapter.record_cycle(
        objective,
        workstream_id="chatgpt-dialogue",
        expected_state_version=resumed.state_version,
        progress_token="wakeup:2:complete",
        evidence_refs=("evidence://dialogue/wakeup-2",),
        proposed_next_action="CLOSE_OBJECTIVE",
        objective_satisfied=True,
    )
    assert second_result.decision is ObjectiveLoopDecision.COMPLETE

    second_reply = compose_objective_cycle_reply(
        second_result,
        persistence_state=PersistenceState.PERSISTED,
        authorization_state=AuthorizationState.VALID,
        continuation_permitted=False,
    )
    assert second_reply.should_continue_automatically is False
    assert second_reply.decision == "COMPLETE"
    assert second_reply.progress_token == "wakeup:2:complete"
    assert "encerrar o ciclo do objetivo" in second_reply.message
    store.close()
