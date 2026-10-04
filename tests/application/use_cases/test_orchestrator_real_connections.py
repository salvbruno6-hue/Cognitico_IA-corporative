from datetime import datetime, timedelta, timezone

from elo.application.use_cases.orchestrator import (
    AuthorizationDecision,
    GovernedOrchestrator,
    OrchestrationRequest,
)
from elo.core.capability_registry import CapabilityProbe, CapabilityRegistry
from elo.cognitive.reasoning.capability_selection import CapabilityRequirement, CapabilitySelector
from elo.cognitive.routing.execution_routing import ExecutionRouter
from elo.cognitive.routing.intelligence_router import IntelligenceRouter
from elo.cognitive.routing.model_selection import ModelCandidate, ModelSelector
from elo.cognitive.routing.tool_selection import ToolSelector
from elo.integrations.ai_provider import AIResponse


class FakeProvider:
    provider_id = "fake"

    def generate(self, request):
        return AIResponse(
            request_id=request.request_id,
            provider=self.provider_id,
            model=request.model,
            output="executed",
            provenance={"tenant_id": request.tenant_id},
        )


def _authorization():
    expiry = (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat()
    return AuthorizationDecision(
        authorized=True,
        authority="elo-authz",
        identity_id="principal-1",
        role="operator",
        evidence_ref="auth-evidence-1",
        session_id="session-1",
        binding_id="binding-1",
        grant_id="grant-1",
        operation="execute",
        resource_id="EXT-TEST",
        expires_at=expiry,
    )


def test_orchestrator_connects_registry_selector_router_boundary_and_runtime():
    registry = CapabilityRegistry(
        (
            CapabilityProbe(
                "LOCAL_RUNTIME",
                "EXT-TEST",
                health_check=lambda: True,
                metadata={"capabilities": "EXT-TEST"},
            ),
        )
    )
    selector = CapabilitySelector(registry)
    execution_router = ExecutionRouter(ModelSelector(), ToolSelector())
    intelligence_router = IntelligenceRouter(
        execution_router,
        {"fake": FakeProvider()},
    )
    request = OrchestrationRequest(
        tenant_id="tenant-a",
        principal_id="principal-1",
        domain="cognitive",
        objective="execute governed test",
        evidence_ids=("evidence-1",),
        authorization=_authorization(),
        request_id="request-1",
        correlation_id="corr-1",
    )

    selection, outcome = GovernedOrchestrator().execute_capability(
        request,
        requirement=CapabilityRequirement("EXT-TEST", preferred_kinds=("LOCAL_RUNTIME",)),
        selector=selector,
        execution_router=execution_router,
        intelligence_router=intelligence_router,
        models=[ModelCandidate("fake:test-model", frozenset({"EXT-TEST"}), 1.0)],
    )

    assert selection.status == "SELECTED"
    assert outcome.executed is True
    assert outcome.status.value == "EXECUTED"
    assert outcome.authorization_id == "grant-1"
    assert outcome.correlation_id == "corr-1"


def test_orchestrator_does_not_execute_without_transport_valid_authorization():
    registry = CapabilityRegistry(
        (
            CapabilityProbe(
                "LOCAL_RUNTIME",
                "EXT-TEST",
                health_check=lambda: True,
                metadata={"capabilities": "EXT-TEST"},
            ),
        )
    )
    router = ExecutionRouter(ModelSelector(), ToolSelector())
    intelligence_router = IntelligenceRouter(router, {"fake": FakeProvider()})
    request = OrchestrationRequest(
        tenant_id="tenant-a",
        principal_id="principal-1",
        domain="cognitive",
        objective="must not execute",
        evidence_ids=("evidence-1",),
        authorization=AuthorizationDecision(
            authorized=True,
            authority="elo-authz",
            identity_id="principal-1",
            role="operator",
            evidence_ref="auth-evidence-1",
        ),
        request_id="request-2",
        correlation_id="corr-2",
    )

    selection, outcome = GovernedOrchestrator().execute_capability(
        request,
        requirement=CapabilityRequirement("EXT-TEST"),
        selector=CapabilitySelector(registry),
        execution_router=router,
        intelligence_router=intelligence_router,
        models=[ModelCandidate("fake:test-model", frozenset({"EXT-TEST"}), 1.0)],
    )

    assert selection.status == "SELECTED"
    assert outcome is None


def test_orchestrator_rejects_tool_only_route_without_claiming_runtime_execution():
    registry = CapabilityRegistry(
        (
            CapabilityProbe(
                "LOCAL_RUNTIME",
                "EXT-TEST",
                health_check=lambda: True,
                metadata={"capabilities": "EXT-TEST"},
            ),
        )
    )
    router = ExecutionRouter(ModelSelector(), ToolSelector())
    intelligence_router = IntelligenceRouter(router, {"fake": FakeProvider()})
    request = OrchestrationRequest(
        tenant_id="tenant-a",
        principal_id="principal-1",
        domain="cognitive",
        objective="must not execute as a provider route",
        evidence_ids=("evidence-1",),
        authorization=_authorization(),
        request_id="request-tool-only",
        correlation_id="corr-tool-only",
    )

    try:
        GovernedOrchestrator().execute_capability(
            request,
            requirement=CapabilityRequirement("EXT-TEST"),
            selector=CapabilitySelector(registry),
            execution_router=router,
            intelligence_router=intelligence_router,
            tools=[],
        )
    except LookupError as exc:
        assert "no executable model/provider path" in str(exc)
    else:
        raise AssertionError("tool-only routing must fail closed before runtime execution")
