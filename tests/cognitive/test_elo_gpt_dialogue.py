import pytest

from elo.cognitive.response.elo_gpt_dialogue import (
    AuthorizationState,
    EloDialogueFacts,
    EloDialogueResponsePolicy,
    EvidenceState,
    ExecutionState,
    PersistenceState,
)


def _facts(**overrides):
    values = {
        "objective_id": "objective-1",
        "workstream_id": "workstream-1",
        "checkpoint_version": 3,
        "state": "ACTIVE",
        "decision": "CONTINUE",
        "next_action": "executar próxima etapa governada",
        "progress_token": "progress-3",
        "justification": "houve progresso material comprovado",
        "evidence_refs": ("ev-1", "ev-2"),
        "persistence_state": PersistenceState.PERSISTED,
        "authorization_state": AuthorizationState.VALID,
        "execution_state": ExecutionState.EXECUTED,
        "evidence_state": EvidenceState.OBSERVED,
        "continuation_permitted": True,
        "human_required": False,
    }
    values.update(overrides)
    return EloDialogueFacts(**values)


def test_policy_exposes_more_than_one_hundred_structured_scenarios():
    assert EloDialogueResponsePolicy.scenario_capacity() == 720


def test_continue_relays_elo_and_allows_next_cycle_without_new_chat_authorization():
    reply = EloDialogueResponsePolicy().compose(_facts())

    assert reply.decision == "CONTINUE"
    assert reply.should_continue_automatically is True
    assert reply.human_required is False
    assert reply.scenario_code == "CONTINUE.PERSISTED.VALID.EXECUTED.OBSERVED"
    assert "sem solicitar nova autorização conversacional" in reply.message


@pytest.mark.parametrize("decision", ["CORRECT", "REPLAN"])
def test_correction_and_replan_can_continue_when_canonical_runtime_permits(decision):
    reply = EloDialogueResponsePolicy().compose(_facts(decision=decision))

    assert reply.decision == decision
    assert reply.should_continue_automatically is True
    assert "Próxima ação:" in reply.message


def test_escalation_never_auto_continues():
    reply = EloDialogueResponsePolicy().compose(
        _facts(
            decision="ESCALATE",
            continuation_permitted=False,
            human_required=True,
            state="HUMAN_APPROVAL_REQUIRED",
        )
    )

    assert reply.should_continue_automatically is False
    assert reply.human_required is True
    assert "aguardar intervenção humana" in reply.message


def test_complete_closes_objective_cycle():
    reply = EloDialogueResponsePolicy().compose(
        _facts(
            decision="COMPLETE",
            continuation_permitted=False,
            state="COMPLETED",
        )
    )

    assert reply.should_continue_automatically is False
    assert "encerrar o ciclo do objetivo" in reply.message


def test_ephemeral_checkpoint_is_explicitly_reported():
    reply = EloDialogueResponsePolicy().compose(
        _facts(
            persistence_state=PersistenceState.EPHEMERAL,
            continuation_permitted=False,
        )
    )

    assert "checkpoint efêmero" in reply.message
    assert reply.should_continue_automatically is False


def test_missing_authorization_is_not_converted_into_permission():
    reply = EloDialogueResponsePolicy().compose(
        _facts(
            authorization_state=AuthorizationState.MISSING,
            continuation_permitted=False,
            execution_state=ExecutionState.BLOCKED,
        )
    )

    assert "autorização canônica ausente" in reply.message
    assert "execução bloqueada" in reply.message
    assert reply.should_continue_automatically is False


def test_insufficient_evidence_is_not_presented_as_fact():
    reply = EloDialogueResponsePolicy().compose(
        _facts(
            evidence_refs=(),
            evidence_state=EvidenceState.INSUFFICIENT,
            continuation_permitted=False,
        )
    )

    assert "evidência insuficiente" in reply.message
    assert reply.evidence_refs == ()


def test_duplicate_evidence_references_are_deduplicated():
    reply = EloDialogueResponsePolicy().compose(
        _facts(evidence_refs=("ev-1", "ev-1", "ev-2"))
    )

    assert reply.evidence_refs == ("ev-1", "ev-2")


def test_invalid_decision_fails_closed():
    with pytest.raises(ValueError, match="unsupported canonical decision"):
        EloDialogueResponsePolicy().compose(_facts(decision="DO_ANYTHING"))


def test_human_required_cannot_coexist_with_automatic_continuation():
    with pytest.raises(ValueError, match="human_required cannot coexist"):
        EloDialogueResponsePolicy().compose(
            _facts(human_required=True, continuation_permitted=True)
        )


def test_checkpoint_version_must_be_real():
    with pytest.raises(ValueError, match="checkpoint_version"):
        EloDialogueResponsePolicy().compose(_facts(checkpoint_version=0))
