from __future__ import annotations

from elo.cognitive.symbiont_execution import (
    ActionResult,
    Reconciliation,
    ResumeStatus,
    SymbiontExecutionStore,
    SymbiontResumer,
    effect_key,
    operation_key,
)


def make_execution(store: SymbiontExecutionStore) -> None:
    store.create_execution(
        execution_id="exec-1",
        candidate_id="candidate-1",
        capability_id="cap-1",
        owner="owner-1",
        current_stage="TESTING",
        next_action="RUN_TEST",
        max_attempts=3,
    )


def test_operation_key_is_deterministic() -> None:
    first = operation_key("exec-1", 2, "TESTING", "RUN_TEST")
    second = operation_key("exec-1", 2, "TESTING", "RUN_TEST")
    assert first == second


def test_effect_key_is_deterministic() -> None:
    op = operation_key("exec-1", 2, "TESTING", "RUN_TEST")
    assert effect_key(op, "input-a", "LAB", "v1") == effect_key(op, "input-a", "LAB", "v1")


def test_resume_completes_without_repeating_completed_operation() -> None:
    store = SymbiontExecutionStore()
    make_execution(store)
    calls = 0

    def execute(state, operation):
        nonlocal calls
        calls += 1
        if state.next_action == "RUN_TEST":
            return ActionResult(
                status="COMPLETED",
                next_action="RECORD_EVIDENCE",
                result={"test": "pass"},
                evidence_ref="evidence-1",
                effect_key="effect-1",
            )
        return ActionResult(
            status="COMPLETED",
            next_action="DONE",
            result={"evidence": "recorded"},
            evidence_ref="evidence-2",
            effect_key="effect-2",
        )

    resumer = SymbiontResumer(store, executor=execute, reconciler=lambda _: Reconciliation(False))
    state = resumer.resume("exec-1", worker_id="worker-1")
    assert state.status == ResumeStatus.COMPLETED.value
    assert calls == 2

    # Repeated resume is a no-op at the terminal state.
    state_again = resumer.resume("exec-1", worker_id="worker-1")
    assert state_again.status == ResumeStatus.COMPLETED.value
    assert calls == 2
    store.close()


def test_interrupted_in_progress_operation_is_reconciled_without_reexecution() -> None:
    store = SymbiontExecutionStore()
    make_execution(store)
    op = operation_key("exec-1", 1, "TESTING", "RUN_TEST")
    store.create_operation(
        op_key=op,
        execution_id="exec-1",
        iteration=1,
        stage="TESTING",
        operation_type="RUN_TEST",
    )
    store.mark_in_progress(op)
    calls = 0

    def execute(state, operation):
        nonlocal calls
        calls += 1
        return ActionResult(
            status="COMPLETED",
            next_action="DONE",
            result={"test": "pass"},
            effect_key="effect-new",
        )

    def reconcile(operation):
        return Reconciliation(
            found_effect=True,
            effect_key="effect-existing",
            result={"test": "pass", "next_action": "DONE"},
        )

    resumer = SymbiontResumer(store, executor=execute, reconciler=reconcile)
    state = resumer.resume("exec-1", worker_id="worker-1")
    assert state.status == ResumeStatus.COMPLETED.value
    assert calls == 0
    store.close()


def test_ambiguous_reconciliation_requires_human() -> None:
    store = SymbiontExecutionStore()
    make_execution(store)
    op = operation_key("exec-1", 1, "TESTING", "RUN_TEST")
    store.create_operation(
        op_key=op,
        execution_id="exec-1",
        iteration=1,
        stage="TESTING",
        operation_type="RUN_TEST",
    )
    store.mark_in_progress(op)

    resumer = SymbiontResumer(
        store,
        executor=lambda *_: ActionResult("COMPLETED", "DONE", {}),
        reconciler=lambda _: Reconciliation(found_effect=False, ambiguous=True),
    )
    state = resumer.resume("exec-1", worker_id="worker-1")
    assert state.status == ResumeStatus.HUMAN_APPROVAL_REQUIRED.value
    assert state.human_required is True
    store.close()


def test_valid_lease_blocks_second_worker() -> None:
    store = SymbiontExecutionStore()
    make_execution(store)
    assert store.acquire_lease("exec-1", "worker-a", ttl_seconds=60)
    assert store.acquire_lease("exec-1", "worker-b", ttl_seconds=60) is False
    store.release_lease("exec-1", "worker-a")
    store.close()


def test_promotion_boundary_never_continues_automatically() -> None:
    store = SymbiontExecutionStore()
    make_execution(store)
    state = store.get_execution("exec-1")
    store.connection.execute(
        "UPDATE symbiont_executions SET promotion_authorized=1 WHERE execution_id=?",
        ("exec-1",),
    )
    store.connection.commit()

    calls = 0

    def execute(*_):
        nonlocal calls
        calls += 1
        return ActionResult("COMPLETED", "DONE", {})

    resumer = SymbiontResumer(store, executor=execute, reconciler=lambda _: Reconciliation(False))
    result = resumer.resume("exec-1", worker_id="worker-1")
    assert result.status == ResumeStatus.HUMAN_APPROVAL_REQUIRED.value
    assert calls == 0
    assert result.human_required is True
    store.close()


def test_retry_budget_exhaustion_blocks_without_silent_increase() -> None:
    store = SymbiontExecutionStore()
    store.create_execution(
        execution_id="exec-budget",
        candidate_id="candidate-1",
        capability_id="cap-1",
        owner="owner-1",
        current_stage="TESTING",
        next_action="RUN_TEST",
        max_attempts=1,
    )

    calls = 0

    def execute(*_):
        nonlocal calls
        calls += 1
        return ActionResult(
            status="COMPLETED",
            next_action="DONE",
            result={"test": "pass"},
        )

    resumer = SymbiontResumer(
        store,
        executor=execute,
        reconciler=lambda _: Reconciliation(found_effect=False),
    )
    op = operation_key("exec-budget", 1, "TESTING", "RUN_TEST")
    store.create_operation(
        op_key=op,
        execution_id="exec-budget",
        iteration=1,
        stage="TESTING",
        operation_type="RUN_TEST",
    )
    store.mark_in_progress(op)
    store.mark_retryable(op)

    state = resumer.resume("exec-budget", worker_id="worker-1")
    assert state.status == ResumeStatus.BLOCKED.value
    assert calls == 0
    store.close()
