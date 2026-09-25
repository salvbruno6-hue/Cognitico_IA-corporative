from elo.cognitive.symbiont_execution import SymbiontExecutionStore
from elo.cognitive.symbiont_gate_perception import (
    ExternalGateObservation,
    WAITING_FOR_EXTERNAL_GATE,
    perceive_external_gate,
    wait_for_external_gate,
)


def test_gate_perception_waits_without_mutating_while_gate_is_pending() -> None:
    store = SymbiontExecutionStore()
    store.create_execution(
        execution_id="gate-1",
        candidate_id="candidate",
        capability_id="capability",
        owner="elo",
        current_stage="TESTING",
        next_action="MEASURE",
    )
    wait_for_external_gate(store, "gate-1", gate_id="ci-123")

    before = store.get_execution("gate-1")
    after = perceive_external_gate(
        store,
        "gate-1",
        observe=lambda gate_id: ExternalGateObservation(gate_id, "PENDING"),
    )

    assert after.status == WAITING_FOR_EXTERNAL_GATE
    assert after.next_action == before.next_action
    assert after.iteration == before.iteration
    assert after.state_version == before.state_version


def test_gate_perception_resumes_after_deterministic_completion() -> None:
    store = SymbiontExecutionStore()
    store.create_execution(
        execution_id="gate-2",
        candidate_id="candidate",
        capability_id="capability",
        owner="elo",
        current_stage="TESTING",
        next_action="MEASURE",
    )
    wait_for_external_gate(store, "gate-2", gate_id="ci-456")

    after = perceive_external_gate(
        store,
        "gate-2",
        observe=lambda gate_id: ExternalGateObservation(
            gate_id, "SUCCESS", evidence_ref="ci-run-456"
        ),
    )

    assert after.status == "ACTIVE"
    assert after.next_action == "MEASURE"
    assert after.iteration == 2
    assert "ci-run-456" in (after.boundary or "")


def test_gate_perception_is_not_a_human_approval() -> None:
    store = SymbiontExecutionStore()
    store.create_execution(
        execution_id="gate-3",
        candidate_id="candidate",
        capability_id="capability",
        owner="elo",
        current_stage="TESTING",
        next_action="MEASURE",
    )
    wait_for_external_gate(store, "gate-3", gate_id="prod-approval")

    after = perceive_external_gate(
        store,
        "gate-3",
        observe=lambda gate_id: ExternalGateObservation(gate_id, "MERGED"),
    )

    assert after.human_required is False
    assert after.status == "ACTIVE"
    assert after.production_authorized is False
    assert after.promotion_authorized is False
    assert after.canonical_mutation is False
