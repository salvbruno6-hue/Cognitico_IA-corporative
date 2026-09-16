from elo.agent_intake.capability_promotion import activate_operational_capabilities
from elo.agent_intake.native_capabilities import CAPABILITY_IDS
from elo.agent_intake.operational_capability_runtime import OperationalCapabilityRuntime
from elo.core.capability_registry import CapabilityStatus


def test_all_eight_capabilities_are_selectable_and_executable():
    registry = activate_operational_capabilities(tenant_scope="test-operational")
    runtime = OperationalCapabilityRuntime(registry, tenant_scope="test-operational")

    available = {item.name for item in registry.snapshot() if item.status == CapabilityStatus.AVAILABLE}
    assert available == set(CAPABILITY_IDS)

    payloads = {
        "HERMES-MEMORY": {"key": "x", "value": 1},
        "HERMES-SKILLS": {"value": "ok"},
        "HERMES-TOOLSETS": {"capability": "read"},
        "HERMES-CONTEXT": {"parent": {"a": 1}, "child": {"b": 2}},
        "HERMES-DELEGATION": {"value": 7},
        "HERMES-AUTOMATION": {"expression": "manual-safe-no-op"},
        "HERMES-MCP": {"capability": "capability.read", "allowlist": ("capability.read",)},
        "HERMES-CHECKPOINT": {"state": {"version": 1}},
    }

    for capability_id in CAPABILITY_IDS:
        decision = __import__("elo.cognitive.reasoning.capability_selection", fromlist=["CapabilityRequirement", "CapabilitySelector"]).CapabilitySelector(registry).select(
            __import__("elo.cognitive.reasoning.capability_selection", fromlist=["CapabilityRequirement"]).CapabilityRequirement(capability_id)
        )
        assert decision.status == "SELECTED"
        execution = runtime.execute(capability_id, payloads[capability_id])
        assert execution.selected and execution.capability_id == capability_id


def test_registry_remains_discovery_authority_and_runtime_owns_execution():
    registry = activate_operational_capabilities(tenant_scope="test-boundary")
    runtime = OperationalCapabilityRuntime(registry, tenant_scope="test-boundary")

    assert not hasattr(registry, "execute")
    assert runtime.execute("HERMES-MEMORY", {"key": "boundary", "value": "ok"}).result == {"value": "ok"}
