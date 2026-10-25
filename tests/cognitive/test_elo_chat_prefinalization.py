from __future__ import annotations

import pytest

from elo.cognitive.objective_continuity import ObjectiveContinuityAdapter
from elo.cognitive.response.elo_chat_prefinalization import (
    EloChatPreFinalizationLoop,
    EloPreFinalizationRequest,
)
from elo.cognitive.response.elo_gpt_dialogue import AuthorizationState, PersistenceState
from elo.cognitive.symbiont_execution import SymbiontExecutionStore
from elo.contracts.okr import Objective


def test_chat_prefinalization_uses_real_elo_cycle_and_derives_next_trigger(tmp_path) -> None:
    path = str(tmp_path / "chat-loop.sqlite")
    objective = Objective(
        tenant_id="tenant-chat",
        objective_id="objective-chat-loop",
        title="Validar dialogo autonomo ELO GPT",
        owner_ref="elo-cognitivo",
        evidence_refs=("evidence://chat/objective",),
    )

    store = SymbiontExecutionStore(path)
    adapter = ObjectiveContinuityAdapter(store)
    checkpoint = adapter.start_or_resume(
        objective,
        workstream_id="chat-prefinalization",
        initial_action="CHECK_ELO_BEFORE_FINAL",
        max_cycles=6,
    )
    calls = {"count": 0}

    def runner(request: EloPreFinalizationRequest):
        calls["count"] += 1
        assert request.expected_checkpoint_version == checkpoint.state_version
        return adapter.record_cycle(
            objective,
            workstream_id="chat-prefinalization",
            expected_state_version=request.expected_checkpoint_version,
            progress_token="chat-turn:1",
            evidence_refs=("evidence://chat/turn/1",),
            proposed_next_action="EXECUTE_NEXT_GOVERNED_ACTION",
        )

    result = EloChatPreFinalizationLoop(runner).run(
        EloPreFinalizationRequest(
            objective_id=objective.objective_id,
            workstream_id="chat-prefinalization",
            expected_checkpoint_version=checkpoint.state_version,
            chat_draft="rascunho do GPT antes de consultar o ELO",
        ),
        persistence_state=PersistenceState.PERSISTED,
        authorization_state=AuthorizationState.VALID,
        continuation_permitted=True,
    )

    assert calls["count"] == 1
    assert result.replay_count == 1
    assert result.elo_reply.decision == "CONTINUE"
    assert result.final_message == result.elo_reply.message
    assert result.next_trigger is not None
    assert result.next_trigger.trigger_type == "CONTINUE_OBJECTIVE"
    assert result.next_trigger.objective_id == objective.objective_id
    assert result.next_trigger.workstream_id == "chat-prefinalization"
    assert result.next_trigger.checkpoint_version > checkpoint.state_version
    assert result.next_trigger.next_action == "EXECUTE_NEXT_GOVERNED_ACTION"
    assert result.next_trigger.progress_token == "chat-turn:1"
    store.close()


def test_chat_prefinalization_complete_emits_no_next_trigger(tmp_path) -> None:
    store = SymbiontExecutionStore(str(tmp_path / "chat-complete.sqlite"))
    objective = Objective(
        tenant_id="tenant-chat",
        objective_id="objective-chat-complete",
        title="Concluir dialogo ELO GPT",
        owner_ref="elo-cognitivo",
        evidence_refs=("evidence://chat/complete",),
    )
    adapter = ObjectiveContinuityAdapter(store)
    checkpoint = adapter.start_or_resume(
        objective,
        workstream_id="chat-prefinalization",
        initial_action="CHECK_ELO_BEFORE_FINAL",
        max_cycles=4,
    )

    def runner(request: EloPreFinalizationRequest):
        return adapter.record_cycle(
            objective,
            workstream_id="chat-prefinalization",
            expected_state_version=request.expected_checkpoint_version,
            progress_token="chat-turn:complete",
            evidence_refs=("evidence://chat/complete/1",),
            proposed_next_action="OBJECTIVE_COMPLETE",
            objective_satisfied=True,
        )

    result = EloChatPreFinalizationLoop(runner).run(
        EloPreFinalizationRequest(
            objective_id=objective.objective_id,
            workstream_id="chat-prefinalization",
            expected_checkpoint_version=checkpoint.state_version,
            chat_draft="rascunho",
        ),
        persistence_state=PersistenceState.PERSISTED,
        authorization_state=AuthorizationState.VALID,
        continuation_permitted=False,
    )

    assert result.elo_reply.decision == "COMPLETE"
    assert result.next_trigger is None
    store.close()


def test_chat_prefinalization_rejects_stale_or_unadvanced_result(tmp_path) -> None:
    store = SymbiontExecutionStore(str(tmp_path / "chat-stale.sqlite"))
    objective = Objective(
        tenant_id="tenant-chat",
        objective_id="objective-chat-stale",
        title="Bloquear replay stale",
        owner_ref="elo-cognitivo",
        evidence_refs=("evidence://chat/stale",),
    )
    adapter = ObjectiveContinuityAdapter(store)
    checkpoint = adapter.start_or_resume(
        objective,
        workstream_id="chat-prefinalization",
        initial_action="CHECK_ELO_BEFORE_FINAL",
    )

    def runner(_request: EloPreFinalizationRequest):
        from elo.cognitive.objective_continuity import ObjectiveLoopCycleResult, ObjectiveLoopDecision
        return ObjectiveLoopCycleResult(
            checkpoint=checkpoint,
            decision=ObjectiveLoopDecision.CONTINUE,
            reason="no advance",
            no_progress_streak=0,
        )

    with pytest.raises(ValueError, match="did not advance"):
        EloChatPreFinalizationLoop(runner).run(
            EloPreFinalizationRequest(
                objective_id=objective.objective_id,
                workstream_id="chat-prefinalization",
                expected_checkpoint_version=checkpoint.state_version,
                chat_draft="rascunho",
            ),
            persistence_state=PersistenceState.PERSISTED,
            authorization_state=AuthorizationState.VALID,
            continuation_permitted=True,
        )
    store.close()


def test_chat_prefinalization_does_not_enter_runner_without_persisted_authorized_continuation() -> None:
    calls = {"count": 0}

    def runner(_request: EloPreFinalizationRequest):
        calls["count"] += 1
        raise AssertionError("runner must not execute")

    loop = EloChatPreFinalizationLoop(runner)
    request = EloPreFinalizationRequest(
        objective_id="objective-1",
        workstream_id="workstream-1",
        expected_checkpoint_version=1,
        chat_draft="rascunho",
    )

    with pytest.raises(ValueError, match="persisted checkpoint"):
        loop.run(
            request,
            persistence_state=PersistenceState.EPHEMERAL,
            authorization_state=AuthorizationState.VALID,
            continuation_permitted=True,
        )
    with pytest.raises(ValueError, match="valid canonical authorization"):
        loop.run(
            request,
            persistence_state=PersistenceState.PERSISTED,
            authorization_state=AuthorizationState.MISSING,
            continuation_permitted=True,
        )
    assert calls["count"] == 0
