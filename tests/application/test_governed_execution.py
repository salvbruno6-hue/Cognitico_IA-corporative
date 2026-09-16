from elo.agent_intake.operational_capability_runtime import OperationalCapabilityRuntime
from elo.application.use_cases.governed_execution import (
    GovernedExecutionRequest,
    GovernedExecutionUseCase,
)
from elo.application.use_cases.orchestrator import AuthorizationDecision
from elo.core.capability_registry import CapabilityRegistry
from elo.agent_intake.capability_promotion import activate_operational_capabilities


def _request(capability_id: str, *, authorized: bool = True) -> GovernedExecutionRequest:
    return GovernedExecutionRequest(
        tenant_id="test-tenant",
        principal_id="test-principal",
        domain="capability",
        objective=f"execute {capability_id}",
        capability_id=capability_id,
        evidence_ids=("evidence-001",),
        authorization=AuthorizationDecision(
            authorized=authorized,
            authority="elo-authz",
            identity_id="identity-001",
            role="operator",
        ),
        payload={"value": "governed"},
    )


def test_governed_execution_reaches_active_operational_capability():
    registry = activate_operational_capabilities(CapabilityRegistry())
    runtime = OperationalCapabilityRuntime(registry)
    use_case = GovernedExecutionUseCase(runtime=runtime)

    result = use_case.execute(_request("HERMES-SKILLS"))

    assert result.decision.status == "AUTHORIZED"
    assert result.decision.stage.value == "EXECUTE"
    assert result.execution is not None
    assert result.execution.selected is True
    assert result.execution.capability_id == "HERMES-SKILLS"
    assert result.execution.result == {"echo": "governed"}


def test_governed_execution_stops_before_runtime_when_authorization_is_denied():
    registry = activate_operational_capabilities(CapabilityRegistry())
    runtime = OperationalCapabilityRuntime(registry)
    use_case = GovernedExecutionUseCase(runtime=runtime)

    result = use_case.execute(_request("HERMES-SKILLS", authorized=False))

    assert result.execution is None
    assert result.decision.stage.value == "HANDOFF"
    assert result.decision.status == "RECOMMENDATION"
    assert "not granted" in result.decision.reason
