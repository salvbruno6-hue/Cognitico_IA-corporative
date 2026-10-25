import pytest

from elo.cognitive.objective_continuity import (
    ObjectiveLoopCheckpoint,
    ObjectiveLoopCycleResult,
    ObjectiveLoopDecision,
)
from elo.cognitive.response.elo_gpt_dialogue import (
    AuthorizationState,
    PersistenceState,
)
from elo.cognitive.response.elo_gpt_dialogue_bridge import compose_objective_cycle_reply


def _result(**checkpoint_overrides):
    checkpoint_values = {
        "execution_id": "objective-loop:test",
        "tenant_id": "tenant-a",
        "objective_id": "objective-1",
        "objective_title": "Objetivo de teste",
        "workstream_id": "workstream-1",
        "status": "ACTIVE",
        "stage": "VALIDATE",
        "next_action": "executar próxima evidência",
        "iteration": 3,
        "state_version": 4,
        "last_progress_token": "progress-4",
        "no_progress_streak": 0,
        "last_decision": ObjectiveLoopDecision.CONTINUE,
        "evidence_refs": ("ev-1",),
    }
    checkpoint_values.update(checkpoint_overrides)
    checkpoint = ObjectiveLoopCheckpoint(**checkpoint_values)
    return ObjectiveLoopCycleResult(
        checkpoint=checkpoint,
        decision=checkpoint.last_decision or ObjectiveLoopDecision.CONTINUE,
        reason="progresso material confirmado",
        no_progress_streak=checkpoint.no_progress_streak,
    )


def test_real_cycle_result_becomes_gpt_reply_without_new_chat_authorization():
    reply = compose_objective_cycle_reply(
        _result(),
        persistence_state=PersistenceState.PERSISTED,
        authorization_state=AuthorizationState.VALID,
        continuation_permitted=True,
    )

    assert reply.decision == "CONTINUE"
    assert reply.should_continue_automatically is True
    assert reply.progress_token == "progress-4"
    assert "objective-1" in reply.message
    assert "sem solicitar nova autorização conversacional" in reply.message


def test_human_approval_checkpoint_is_rel_endpoint_not_auto_continue():
    result = _result(
        status="HUMAN_APPROVAL_REQUIRED",
        last_decision=ObjectiveLoopDecision.ESCALATE,
        next_action="aguardar aprovação humana",
    )

    reply = compose_objective_cycle_reply(
        result,
        persistence_state=PersistenceState.PERSISTED,
        authorization_state=AuthorizationState.VALID,
        continuation_permitted=False,
    )

    assert reply.decision == "ESCALATE"
    assert reply.human_required is True
    assert reply.should_continue_automatically is False


def test_bridge_rejects_invented_human_requirement():
    with pytest.raises(ValueError, match="does not match canonical checkpoint"):
        compose_objective_cycle_reply(
            _result(status="ACTIVE"),
            persistence_state=PersistenceState.PERSISTED,
            authorization_state=AuthorizationState.VALID,
            continuation_permitted=False,
            human_required=True,
        )


def test_bridge_rejects_cycle_without_real_progress_token():
    with pytest.raises(ValueError, match="persisted progress_token"):
        compose_objective_cycle_reply(
            _result(last_progress_token=None),
            persistence_state=PersistenceState.PERSISTED,
            authorization_state=AuthorizationState.VALID,
            continuation_permitted=False,
        )
