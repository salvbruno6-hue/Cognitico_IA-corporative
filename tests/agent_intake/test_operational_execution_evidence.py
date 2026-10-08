from elo.agent_intake.capability_promotion import activate_operational_capabilities
from elo.agent_intake.operational_capability_runtime import OperationalCapabilityRuntime
from elo.memory.persistent import PersistentMemoryStore


def test_operational_execution_writes_immutable_historical_evidence():
    registry = activate_operational_capabilities(tenant_scope="evidence-test")
    store = PersistentMemoryStore()
    runtime = OperationalCapabilityRuntime(
        registry,
        tenant_scope="evidence-test",
        evidence_store=store,
    )

    execution = runtime.execute("HERMES-MEMORY", {"key": "evidence", "value": "ok"})

    assert execution.selected is True
    assert execution.evidence_memory_id

    evidence = store.get(
        execution.evidence_memory_id,
        tenant_id="evidence-test",
        domain="capability_execution",
    )
    assert evidence is not None
    assert evidence.kind == "historical"
    assert evidence.provenance["capability_id"] == "HERMES-MEMORY"
    assert evidence.provenance["promotion_state"] == "success"
    assert evidence.provenance["canonical_mutation"] is False

    replay = store.replay_history(
        execution.evidence_memory_id,
        tenant_id="evidence-test",
        domain="capability_execution",
    )
    assert replay == (evidence,)

    store.close()
