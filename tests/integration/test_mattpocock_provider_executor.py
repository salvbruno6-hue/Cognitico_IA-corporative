"""Governed live-provider transport contract; mocks cannot prove productive activation."""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from elo.agent_intake.mattpocock_catalog import ExternalSkillCatalog
from elo.agent_intake.mattpocock_provider_executor import (
    EloAuthzExternalSkillVerifier, MattPocockProviderExecutor, OPERATION,
)
from elo.application.use_cases.orchestrator import AuthorizationDecision, GovernedOrchestrator, OrchestrationRequest
from elo.cognitive.routing.execution_routing import ExecutionRouter
from elo.cognitive.routing.intelligence_router import IntelligenceRouter
from elo.cognitive.routing.model_selection import ModelCandidate, ModelSelector
from elo.cognitive.routing.tool_selection import ToolSelector
from elo.core.execution_boundary import ExecutionStatus
from elo.evidence import EvidenceAccessError, EvidenceRepository
from elo.integrations.ai_provider import AIResponse

ROOT = Path(__file__).resolve().parents[2]
ENDPOINT = "https://fxbpevjrkwhbicpmecow.supabase.co/functions/v1/elo-authz"


def sample_request(skill_id="mattpocock:diagnosing-bugs"):
    return OrchestrationRequest(
        tenant_id="tenant-a", principal_id="identity-1", domain="engineering",
        objective="Explain a deterministic failure without changing source files",
        request_id="request-1", correlation_id="trace-1",
        evidence_ids=("evidence:source-1",),
        authorization=AuthorizationDecision(
            authorized=True, authority="elo-authz", identity_id="identity-1",
            role="ELO_OPERATOR", evidence_ref="elo-authz:request-1",
            session_id="session-1", binding_id="binding-1",
            grant_id="grant-1", operation="execute", resource_id=skill_id,
            expires_at=(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat(),
        ),
    )


class FakeHTTPResponse:
    status = 200
    def __init__(self, payload):
        self.payload = payload
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def authz_payload(request, skill_id):
    auth = request.authorization
    return {
        "authorized": True, "authorization_authority": "elo-authz",
        "authorization_state": "elo-execution-authorized",
        "operation": OPERATION, "repository": "salvbruno6-hue/Cognitico_IA-corporative",
        "tenant_id": request.tenant_id, "resource_id": skill_id,
        "identity_id": auth.identity_id, "session_id": auth.session_id,
        "binding_id": auth.binding_id, "grant_id": auth.grant_id,
        "evidence_ref": auth.evidence_ref, "request_id": request.request_id,
        "expires_at": auth.expires_at,
    }


class FakeProvider:
    provider_id = "fake"
    def __init__(self, *, output="Evidence-limited diagnostic analysis"):
        self.calls = []
        self.output = output
    def generate(self, request):
        self.calls.append(request)
        return AIResponse(
            request_id=request.request_id,
            provider="fake", model=request.model, output=self.output,
        )


def make_executor(request, *, payload_changes=None, allow_nonpromoted=False, network_error=False):
    body = authz_payload(request, request.authorization.resource_id)
    body.update(payload_changes or {})
    http_calls = []
    def http_post(wire, *, timeout):
        http_calls.append(json.loads(wire.data))
        if network_error:
            raise OSError("network down")
        return FakeHTTPResponse(body)
    verifier = EloAuthzExternalSkillVerifier(
        endpoint=ENDPOINT, bearer_token="test-session-bearer", transport=http_post
    )
    router = ExecutionRouter(ModelSelector(), ToolSelector())
    selection = router.route(
        request.authorization.resource_id,
        models=[ModelCandidate("fake:test-model", frozenset({request.authorization.resource_id}), quality=1.0)],
    )
    provider = FakeProvider()
    evidence = EvidenceRepository()
    adapter = MattPocockProviderExecutor(
        request=request, route=selection,
        intelligence_router=IntelligenceRouter(router, {"fake": provider}),
        authz_verifier=verifier, evidence_repository=evidence,
        allow_nonpromoted=allow_nonpromoted,
    )
    return adapter, provider, evidence, http_calls


def test_promoted_skill_uses_actual_evidence_boundary_and_provider_contract():
    request = sample_request()
    executor, provider, evidence, http_calls = make_executor(request)
    result = GovernedOrchestrator().invoke_external_skill(
        request, skill_id=request.authorization.resource_id,
        approved_skill_ids=frozenset({request.authorization.resource_id}),
        executor=executor, catalog=ExternalSkillCatalog(ROOT),
    )
    assert result.outcome.status is ExecutionStatus.EXECUTED
    assert len(provider.calls) == 1
    assert http_calls[0]["operation"] == OPERATION
    assert http_calls[0]["resource_id"] == "mattpocock:diagnosing-bugs"
    assert "UNTRUSTED EXTERNAL SKILL SOURCE" in provider.calls[0].context
    assert "Do not claim to execute files" in provider.calls[0].instructions
    ref = result.outcome.provenance["runtime_evidence_ref"]
    observed = evidence.get(ref, tenant_id="tenant-a")
    assert observed.value == provider.output
    assert observed.provenance["source_commit"] == result.reference.source_commit
    assert observed.provenance["production_efficacy_proven"] is False
    assert result.symbiont_decision.disposition == "REUSE"
    assert not result.symbiont_decision.candidate_creation_allowed
    with pytest.raises(EvidenceAccessError):
        evidence.get(ref, tenant_id="tenant-other")


@pytest.mark.parametrize("field", [
    "tenant_id", "resource_id", "identity_id", "session_id", "binding_id",
    "grant_id", "evidence_ref", "authorization_state", "repository", "expires_at",
])
def test_authz_mismatch_blocks_provider_without_side_effect(field):
    request = sample_request()
    executor, provider, evidence, _ = make_executor(
        request, payload_changes={field: "INVALID"}
    )
    result = GovernedOrchestrator().invoke_external_skill(
        request, skill_id=request.authorization.resource_id,
        approved_skill_ids=frozenset({request.authorization.resource_id}),
        executor=executor, catalog=ExternalSkillCatalog(ROOT),
    )
    assert result.outcome.status is ExecutionStatus.FAILED
    assert result.symbiont_decision is None
    assert provider.calls == []


def test_failed_authz_network_blocks_provider():
    request = sample_request()
    executor, provider, _, _ = make_executor(request, network_error=True)
    outcome = GovernedOrchestrator().invoke_external_skill(
        request, skill_id=request.authorization.resource_id,
        approved_skill_ids=frozenset({request.authorization.resource_id}),
        executor=executor, catalog=ExternalSkillCatalog(ROOT),
    )
    assert outcome.outcome.status is ExecutionStatus.FAILED
    assert provider.calls == []


def test_unpromoted_skill_requires_extra_admission_even_with_authz():
    request = sample_request("mattpocock:software-factory")
    executor, provider, _, _ = make_executor(request)
    result = GovernedOrchestrator().invoke_external_skill(
        request, skill_id=request.authorization.resource_id,
        approved_skill_ids=frozenset({request.authorization.resource_id}),
        executor=executor, catalog=ExternalSkillCatalog(ROOT),
    )
    assert result.outcome.status is ExecutionStatus.FAILED
    assert provider.calls == []


def test_unpromoted_skill_can_be_used_only_with_two_explicit_gates():
    request = sample_request("mattpocock:software-factory")
    executor, provider, evidence, _ = make_executor(request, allow_nonpromoted=True)
    result = GovernedOrchestrator().invoke_external_skill(
        request, skill_id=request.authorization.resource_id,
        approved_skill_ids=frozenset({request.authorization.resource_id}),
        executor=executor, catalog=ExternalSkillCatalog(ROOT),
    )
    assert result.outcome.status is ExecutionStatus.EXECUTED
    assert len(provider.calls) == 1
    assert evidence.get(result.outcome.provenance["runtime_evidence_ref"], tenant_id="tenant-a")


def test_no_matching_model_route_prohibits_execution():
    request = sample_request()
    executor, provider, _, _ = make_executor(request)
    from elo.cognitive.routing.execution_routing import RoutingDecision
    executor.route = RoutingDecision("mattpocock:other-skill", "fake:test-model", None, "mismatch")
    result = GovernedOrchestrator().invoke_external_skill(
        request, skill_id=request.authorization.resource_id,
        approved_skill_ids=frozenset({request.authorization.resource_id}),
        executor=executor, catalog=ExternalSkillCatalog(ROOT),
    )
    assert result.outcome.status is ExecutionStatus.FAILED
    assert provider.calls == []


def test_invalid_authz_endpoint_refused():
    with pytest.raises(ValueError):
        EloAuthzExternalSkillVerifier(
            endpoint="http://attacker.test/functions/v1/elo-authz",
            bearer_token="a",
        )
