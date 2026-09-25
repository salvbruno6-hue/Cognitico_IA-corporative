from elo.cognitive.symbiont_execution import ActionResult, SymbiontExecutionStore, SymbiontResumer
from elo.cognitive.symbiont_gate_perception import ExternalGateObservation, wait_for_external_gate
from elo.cognitive.symbiont_gate_resume import perceive_and_resume


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
    wait_for_external_gate(store, "resume-gate-1", gate_id="ci-1")
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
    wait_for_external_gate(store, "resume-gate-2", gate_id="ci-2")
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
