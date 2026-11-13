from elo.agent_intake.operational_capability_runtime import OperationalCapabilityRuntime
from elo.application.use_cases.governed_execution import (
    GovernedExecutionRequest,
    GovernedExecutionUseCase,
)
from elo.application.use_cases.orchestrator import AuthorizationDecision
from elo.application.web_request_boundary import GovernedWebRequestBoundary
from elo.core.capability_registry import CapabilityRegistry
from elo.core.capability_resolution import resolve_capability
from elo.agent_intake.capability_promotion import activate_operational_capabilities


def _request(condition: str, *, authorized: bool = True) -> GovernedExecutionRequest:
    core_decision = resolve_capability(
        request_id="req-001",
        tenant_scope="test-tenant",
        condition=condition,
        analysis_evidence=("evidence-001",),
    )
    return GovernedExecutionRequest(
        tenant_id="test-tenant",
        principal_id="test-principal",
        domain="capability",
        objective=f"execute {condition}",
        core_capability_decision=core_decision,
        evidence_ids=("evidence-001",),
        authorization=AuthorizationDecision(
            authorized=authorized,
            authority="elo-authz",
            identity_id="identity-001",
            role="operator",
        ),
        payload={"value": "governed"},
    )


def _authorization(*, authorized: bool = True) -> AuthorizationDecision:
    return AuthorizationDecision(
        authorized=authorized,
        authority="elo-authz",
        identity_id="identity-001",
        role="operator",
    )


def test_governed_execution_reaches_active_operational_capability():
    registry = activate_operational_capabilities(CapabilityRegistry())
    runtime = OperationalCapabilityRuntime(registry)
    use_case = GovernedExecutionUseCase(runtime=runtime)

    result = use_case.execute(_request("skill-execution"))

    assert result.decision.status == "AUTHORIZED"
    assert result.decision.stage.value == "EXECUTE"
    assert result.execution is not None
    assert result.execution.selected is True
    assert result.execution.capability_id == "HERMES-SKILLS"
    assert result.execution.result == {"echo": "governed"}


def test_governed_execution_stops_before_runtime_when_core_cannot_resolve():
    registry = activate_operational_capabilities(CapabilityRegistry())
    runtime = OperationalCapabilityRuntime(registry)
    use_case = GovernedExecutionUseCase(runtime=runtime)

    result = use_case.execute(_request("unknown-condition"))

    assert result.execution is None
    assert result.decision.stage.value == "HANDOFF"
    assert "Core did not resolve" in result.decision.reason


def test_governed_execution_stops_before_runtime_when_authorization_is_denied():
    registry = activate_operational_capabilities(CapabilityRegistry())
    runtime = OperationalCapabilityRuntime(registry)
    use_case = GovernedExecutionUseCase(runtime=runtime)

    result = use_case.execute(_request("skill-execution", authorized=False))

    assert result.execution is None
    assert result.decision.stage.value == "HANDOFF"
    assert result.decision.status == "RECOMMENDATION"
    assert "not granted" in result.decision.reason


def test_web_request_enters_core_before_operational_execution():
    web_request = GovernedWebRequestBoundary().accept(
        request_id="web-001",
        tenant_id="test-tenant",
        principal_id="test-principal",
        intent="execute skill",
        scope="capability",
        evidence_ids=("web-evidence-001",),
        provenance={"source": "test-web"},
    )
    registry = activate_operational_capabilities(CapabilityRegistry())
    runtime = OperationalCapabilityRuntime(registry)
    use_case = GovernedExecutionUseCase(runtime=runtime)

    result = use_case.execute_from_core_analysis(
        web_request=web_request,
        analysis_condition="skill-execution",
        authorization=_authorization(),
        payload={"value": "web-governed"},
    )

    assert result.execution is not None
    assert result.execution.capability_id == "HERMES-SKILLS"
    assert result.execution.result == {"echo": "web-governed"}


def test_web_request_core_resolution_blocks_unknown_analysis_condition():
    web_request = GovernedWebRequestBoundary().accept(
        request_id="web-002",
        tenant_id="test-tenant",
        principal_id="test-principal",
        intent="execute unknown",
        scope="capability",
        evidence_ids=(),
        provenance={"source": "test-web"},
    )
    registry = activate_operational_capabilities(CapabilityRegistry())
    runtime = OperationalCapabilityRuntime(registry)
    use_case = GovernedExecutionUseCase(runtime=runtime)

    result = use_case.execute_from_core_analysis(
        web_request=web_request,
        analysis_condition="unknown-condition",
        authorization=_authorization(),
    )

    assert result.execution is None
    assert result.decision.stage.value == "HANDOFF"
    assert "Core did not resolve" in result.decision.reason
