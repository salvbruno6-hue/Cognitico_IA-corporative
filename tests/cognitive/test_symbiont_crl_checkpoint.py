from __future__ import annotations

from elo.cognitive.runtime.symbiont_checkpoint import (
    advance_crl_checkpoint,
    checkpoint_for_crl,
)
from elo.cognitive.symbiont_execution import (
    ActionResult,
    SymbiontExecutionStore,
)


def test_checkpoint_is_projection_of_existing_symbiont_state() -> None:
    store = SymbiontExecutionStore()
    store.create_execution(
        execution_id="crl-exec-1",
        candidate_id="candidate-1",
        capability_id="cap-1",
        owner="elo-cognitive",
        current_stage="ANALYZE",
        next_action="RUN_ANALYSIS",
    )

    checkpoint = checkpoint_for_crl(store, "crl-exec-1")

    assert checkpoint.execution_id == "crl-exec-1"
    assert checkpoint.stage == "ANALYZE"
    assert checkpoint.next_action == "RUN_ANALYSIS"
    assert checkpoint.iteration == 1
    assert checkpoint.operation_key.startswith("op_")


def test_checkpoint_advance_reuses_existing_operation_contract() -> None:
    store = SymbiontExecutionStore()
    state = store.create_execution(
        execution_id="crl-exec-2",
        candidate_id="candidate-2",
        capability_id="cap-2",
        owner="elo-cognitive",
        current_stage="TESTING",
        next_action="RUN_TEST",
    )

    checkpoint = checkpoint_for_crl(store, state.execution_id)
    operation = store.create_operation(
        op_key=checkpoint.operation_key,
        execution_id=state.execution_id,
        iteration=state.iteration,
        stage=state.current_stage,
        operation_type=state.next_action,
    )
    store.mark_in_progress(operation.operation_key)

    updated = advance_crl_checkpoint(
        store,
        state,
        store.get_operation(operation.operation_key),
        ActionResult(
            status="COMPLETED",
            next_action="RECORD_EVIDENCE",
            result={"evidence_ref": "evidence-2"},
            evidence_ref="evidence-2",
            effect_key="effect-2",
        ),
    )

    assert updated.status == "ACTIVE"
    assert updated.next_action == "RECORD_EVIDENCE"
    assert updated.iteration == 2
    persisted = store.get_operation(operation.operation_key)
    assert persisted is not None
    assert persisted.status == "COMPLETED"
    assert persisted.effect_key == "effect-2"


def test_checkpoint_never_authorizes_governed_boundaries() -> None:
    store = SymbiontExecutionStore()
    state = store.create_execution(
        execution_id="crl-exec-3",
        candidate_id="candidate-3",
        capability_id="cap-3",
        owner="elo-cognitive",
        current_stage="REVIEW",
        next_action="REQUEST_PROMOTION",
    )

    checkpoint = checkpoint_for_crl(store, state.execution_id)
    operation = store.create_operation(
        op_key=checkpoint.operation_key,
        execution_id=state.execution_id,
        iteration=state.iteration,
        stage=state.current_stage,
        operation_type=state.next_action,
    )

    updated = advance_crl_checkpoint(
        store,
        state,
        operation,
        ActionResult(
            status="COMPLETED",
            next_action="HUMAN_APPROVAL_REQUIRED",
            result={"boundary": "promotion"},
            boundary="promotion",
            human_required=True,
        ),
    )

    assert updated.status == "HUMAN_APPROVAL_REQUIRED"
    assert updated.human_required is True
    assert updated.promotion_authorized is False
    assert updated.canonical_mutation is False
    assert updated.production_authorized is False
