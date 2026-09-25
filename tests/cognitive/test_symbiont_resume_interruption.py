from __future__ import annotations

from elo.cognitive.symbiont_execution import (
    ActionResult,
    Reconciliation,
    ResumeStatus,
    SymbiontExecutionStore,
    SymbiontResumer,
)


def test_repeated_resume_after_interruption_preserves_logical_progress() -> None:
    store = SymbiontExecutionStore()
    store.create_execution(
        execution_id="exec-interrupt",
        candidate_id="candidate-1",
        capability_id="cap-1",
        owner="owner-1",
        current_stage="TESTING",
        next_action="RUN_TEST",
        max_attempts=3,
    )

    calls: list[str] = []
    first_effect = "effect-run-test"

    def execute(state, operation):
        calls.append(operation.operation_key)
        if state.next_action == "RUN_TEST":
            raise RuntimeError("simulated interruption after external work")
        return ActionResult(
            status="COMPLETED",
            next_action="DONE",
            result={"evidence_ref": "evidence-final"},
            effect_key="effect-record-evidence",
        )

    def reconcile(operation):
        return Reconciliation(
            found_effect=True,
            effect_key=first_effect,
            result={
                "test": "pass",
                "next_action": "RECORD_EVIDENCE",
                "effect_key": first_effect,
            },
        )

    resumer = SymbiontResumer(
        store,
        executor=execute,
        reconciler=reconcile,
    )

    try:
        resumer.resume("exec-interrupt", worker_id="worker-1", max_steps=1)
    except RuntimeError:
        pass

    interrupted = store.get_execution("exec-interrupt")
    assert interrupted.status == "ACTIVE"
    assert interrupted.next_action == "RUN_TEST"

    resumed_once = resumer.resume("exec-interrupt", worker_id="worker-1", max_steps=1)
    assert resumed_once.status == "ACTIVE"
    assert resumed_once.next_action == "RECORD_EVIDENCE"

    resumed_twice = resumer.resume("exec-interrupt", worker_id="worker-1")
    assert resumed_twice.status == ResumeStatus.COMPLETED.value

    resumed_again = resumer.resume("exec-interrupt", worker_id="worker-1")
    assert resumed_again.status == ResumeStatus.COMPLETED.value

    # RUN_TEST was externally effective before interruption and was reconciled,
    # so the same operation was never executed a second time.
    assert len(calls) == 2
    assert calls[0] != calls[1]
    store.close()
