from __future__ import annotations

import json

from elo.cognitive.symbiont_execution import (
    ActionResult,
    Reconciliation,
    ResumeStatus,
    SymbiontExecutionStore,
    SymbiontResumer,
    operation_key,
)


def test_resume_resume_resume_is_logically_idempotent() -> None:
    store = SymbiontExecutionStore()
    store.create_execution(
        execution_id="exec-invariant",
        candidate_id="candidate-1",
        capability_id="cap-1",
        owner="owner-1",
        current_stage="TESTING",
        next_action="RUN_TEST",
    )
    calls: list[str] = []

    def execute(state, operation):
        calls.append(operation.operation_key)
        return ActionResult(
            status="COMPLETED",
            next_action="DONE",
            result={"evidence_ref": "evidence-1"},
            evidence_ref="evidence-1",
            effect_key="effect-1",
        )

    resumer = SymbiontResumer(
        store,
        executor=execute,
        reconciler=lambda _: Reconciliation(found_effect=False),
    )

    first = resumer.resume("exec-invariant", worker_id="worker-1")
    snapshot_first = store.get_execution("exec-invariant")

    second = resumer.resume("exec-invariant", worker_id="worker-1")
    snapshot_second = store.get_execution("exec-invariant")

    third = resumer.resume("exec-invariant", worker_id="worker-1")
    snapshot_third = store.get_execution("exec-invariant")

    assert first.status == ResumeStatus.COMPLETED.value
    assert second.status == ResumeStatus.COMPLETED.value
    assert third.status == ResumeStatus.COMPLETED.value
    assert snapshot_first == snapshot_second == snapshot_third
    assert len(calls) == 1

    operation = store.get_operation(
        operation_key("exec-invariant", 1, "TESTING", "RUN_TEST")
    )
    assert operation is not None
    assert operation.status == "COMPLETED"
    assert operation.effect_key == "effect-1"
    assert json.loads(operation.result_json or "{}")["evidence_ref"] == "evidence-1"
    store.close()


def test_repeated_resume_after_reconciliation_does_not_duplicate_effect_or_evidence() -> None:
    store = SymbiontExecutionStore()
    store.create_execution(
        execution_id="exec-reconcile-invariant",
        candidate_id="candidate-1",
        capability_id="cap-1",
        owner="owner-1",
        current_stage="TESTING",
        next_action="RUN_TEST",
    )

    op = operation_key("exec-reconcile-invariant", 1, "TESTING", "RUN_TEST")
    store.create_operation(
        op_key=op,
        execution_id="exec-reconcile-invariant",
        iteration=1,
        stage="TESTING",
        operation_type="RUN_TEST",
    )
    store.mark_in_progress(op)

    calls = 0

    def execute(*_):
        nonlocal calls
        calls += 1
        return ActionResult(
            status="COMPLETED",
            next_action="DONE",
            result={"evidence_ref": "should-not-be-created"},
            effect_key="effect-new",
        )

    def reconcile(operation):
        return Reconciliation(
            found_effect=True,
            effect_key="effect-existing",
            result={
                "test": "pass",
                "evidence_ref": "evidence-existing",
                "next_action": "DONE",
            },
        )

    resumer = SymbiontResumer(
        store,
        executor=execute,
        reconciler=reconcile,
    )

    first = resumer.resume("exec-reconcile-invariant", worker_id="worker-1")
    snapshot_first = store.get_execution("exec-reconcile-invariant")
    second = resumer.resume("exec-reconcile-invariant", worker_id="worker-1")
    snapshot_second = store.get_execution("exec-reconcile-invariant")
    third = resumer.resume("exec-reconcile-invariant", worker_id="worker-1")
    snapshot_third = store.get_execution("exec-reconcile-invariant")

    assert first.status == ResumeStatus.COMPLETED.value
    assert second.status == ResumeStatus.COMPLETED.value
    assert third.status == ResumeStatus.COMPLETED.value
    assert snapshot_first == snapshot_second == snapshot_third
    assert calls == 0

    operation = store.get_operation(op)
    assert operation is not None
    assert operation.status == "COMPLETED"
    assert operation.effect_key == "effect-existing"
    result = json.loads(operation.result_json or "{}")
    assert result["evidence_ref"] == "evidence-existing"
    store.close()
