from elo.cognitive.symbiont_execution import ActionResult, SymbiontExecutionStore, SymbiontResumer
from elo.cognitive.symbiont_gate_perception import ExternalGateObservation, wait_for_external_gate
from elo.cognitive.symbiont_gate_resume import perceive_and_resume
from elo.cognitive.symbiont_wait_timer import read_wait_timer, timer_ready


def test_completed_external_gate_reenters_existing_resumer() -> None:
    store = SymbiontExecutionStore()
    store.create_execution(
        execution_id="resume-gate-1",
        candidate_id="candidate",
        capability_id="capability",
        owner="elo",
        current_stage="TESTING",
        next_action="MEASURE",
    )
    wait_for_external_gate(store, "resume-gate-1", gate_id="ci-1", delay_seconds=30.0)
    calls = []

    def executor(state, operation):
        calls.append(operation.operation_key)
        return ActionResult(
            status="COMPLETED",
            next_action="DONE",
            result={"ok": True},
            evidence_ref="ci-1",
        )

    resumer = SymbiontResumer(
        store,
        executor=executor,
        reconciler=lambda operation: __import__(
            "elo.cognitive.symbiont_execution",
            fromlist=["Reconciliation"],
        ).Reconciliation(found_effect=False),
    )

    result = perceive_and_resume(
        store,
        resumer,
        "resume-gate-1",
        observe=lambda gate_id: ExternalGateObservation(
            gate_id, "SUCCESS", evidence_ref="ci-1"
        ),
        worker_id="worker-1",
        now=lambda: 1030.0,
    )

    assert result.resumed is True
    assert result.state.status == "COMPLETED"
    assert len(calls) == 1


def test_pending_external_gate_does_not_enter_resumer() -> None:
    store = SymbiontExecutionStore()
    store.create_execution(
        execution_id="resume-gate-2",
        candidate_id="candidate",
        capability_id="capability",
        owner="elo",
        current_stage="TESTING",
        next_action="MEASURE",
    )
    wait_for_external_gate(store, "resume-gate-2", gate_id="ci-2", delay_seconds=30.0)
    called = False

    def executor(state, operation):
        nonlocal called
        called = True
        return ActionResult(status="COMPLETED", next_action="DONE", result={})

    resumer = SymbiontResumer(
        store,
        executor=executor,
        reconciler=lambda operation: __import__(
            "elo.cognitive.symbiont_execution",
            fromlist=["Reconciliation"],
        ).Reconciliation(found_effect=False),
    )

    result = perceive_and_resume(
        store,
        resumer,
        "resume-gate-2",
        observe=lambda gate_id: ExternalGateObservation(gate_id, "PENDING"),
        worker_id="worker-2",
    )

    assert result.resumed is False
    assert result.state.status == "WAITING_FOR_EXTERNAL_GATE"
    assert called is False


def test_pending_external_gate_waits_until_timer_is_due() -> None:
    store = SymbiontExecutionStore()
    store.create_execution(
        execution_id="resume-gate-3",
        candidate_id="candidate",
        capability_id="capability",
        owner="elo",
        current_stage="TESTING",
        next_action="MEASURE",
    )
    wait_for_external_gate(
        store, "resume-gate-3", gate_id="ci-3", delay_seconds=30.0
    )
    state = store.get_execution("resume-gate-3")
    timer = read_wait_timer(state)
    assert timer is not None
    assert timer.remaining_seconds(now=1000.0) > 0
    assert timer_ready(state, now=1000.0) is False

    called = False

    def observe(_gate_id):
        nonlocal called
        called = True
        return ExternalGateObservation("ci-3", "SUCCESS", evidence_ref="ci-3")

    result = perceive_and_resume(
        store,
        SymbiontResumer(
            store,
            executor=lambda state, operation: ActionResult(
                status="COMPLETED", next_action="DONE", result={}
            ),
            reconciler=lambda operation: __import__(
                "elo.cognitive.symbiont_execution", fromlist=["Reconciliation"]
            ).Reconciliation(found_effect=False),
        ),
        "resume-gate-3",
        observe=observe,
        worker_id="worker-3",
        now=lambda: 1000.0,
    )
    assert result.resumed is False
    assert result.state.status == "WAITING_FOR_EXTERNAL_GATE"
    assert called is False


def test_pending_external_gate_rearms_timer_after_due_poll() -> None:
    store = SymbiontExecutionStore()
    store.create_execution(
        execution_id="resume-gate-4",
        candidate_id="candidate",
        capability_id="capability",
        owner="elo",
        current_stage="TESTING",
        next_action="MEASURE",
    )
    wait_for_external_gate(
        store, "resume-gate-4", gate_id="ci-4", delay_seconds=30.0
    )
    result = perceive_external_gate = __import__(
        "elo.cognitive.symbiont_gate_perception", fromlist=["perceive_external_gate"]
    ).perceive_external_gate(
        store,
        "resume-gate-4",
        observe=lambda gate_id: ExternalGateObservation(gate_id, "PENDING"),
        now=lambda: 1030.0,
    )
    timer = read_wait_timer(result)
    assert result.status == "WAITING_FOR_EXTERNAL_GATE"
    assert timer is not None
    assert timer.attempt == 2
    assert timer.wake_at == 1060.0
