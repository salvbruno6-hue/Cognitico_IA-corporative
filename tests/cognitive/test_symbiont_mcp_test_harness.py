import pytest

from elo.cognitive.agents.hermes_contract import HermesExecutionRequest
from elo.cognitive.symbiont_mcp_contracts import MCPCapabilityDescriptor, MCPCapabilityTestCase, MCPTestDisposition
from elo.cognitive.symbiont_mcp_test_harness import SymbiontMCPTestHarness


def _descriptor(capability="mcp:fixture:read"):
    return MCPCapabilityDescriptor(capability, "fixture", "fixture-provider", "read", "read fixture", "controlled read", {"type": "object"}, "fixture://mcp", "test-commit", "tenant-test", "test")


def _case(capability="mcp:fixture:read", non_destructive=True):
    return MCPCapabilityTestCase("mcp-test-001", capability, "tenant-test", "verify read", "read fixture", {"value": "fixture"}, ("result is ok",), ("execution", "outcome"), non_destructive=non_destructive)


def _request(capability="mcp:fixture:read", review=False):
    return HermesExecutionRequest("mcp-request-001", "benchmark MCP", {"domain": "test"}, "tenant-test", "mcp_benchmark", (capability,), evidence_requirements=("execution", "outcome"), constraints={"destructive_test_review": review}, execution_policy={"max_tool_calls": 10})


def _transport(endpoint, payload):
    return {"request_id": payload["request_id"], "status": "completed", "execution": {"runtime": "hermes"}, "evidence": ({"evidence_id": "ev-mcp-001"},), "outcome": {"result": "ok"}, "tool_usage": ({"tool": "fixture.read"},), "metrics": {"task_success_score": .9, "reliability_score": .9, "quality_score": .9, "latency_score": .9}, "learning_candidate": {"promotion_state": "candidate_only"}}


def test_mcp_harness_returns_candidate_only_benchmark():
    benchmark = SymbiontMCPTestHarness().benchmark(_descriptor(), _case(), _request(), endpoint="http://hermes.test", transport=_transport)
    assert benchmark.result.disposition == MCPTestDisposition.PASS
    assert benchmark.result.recommendation.value == "LAB_CANDIDATE"
    assert benchmark.result.candidate_only is True
    assert benchmark.result.evidence_ids == ("ev-mcp-001",)
    assert benchmark.result.aggregate_score == .9


def test_mcp_harness_rejects_unauthorized_capability():
    with pytest.raises(ValueError, match="not authorized"):
        SymbiontMCPTestHarness().benchmark(_descriptor(), _case(), _request("mcp:other:read"), endpoint="http://hermes.test", transport=_transport)


def test_mcp_harness_rejects_tenant_mismatch():
    request = HermesExecutionRequest("mcp-request-001", "benchmark MCP", {"domain": "test"}, "other-tenant", "mcp_benchmark", ("mcp:fixture:read",), evidence_requirements=("execution", "outcome"))
    with pytest.raises(ValueError, match="tenant scope"):
        SymbiontMCPTestHarness().benchmark(_descriptor(), _case(), request, endpoint="http://hermes.test", transport=_transport)


def test_mcp_harness_rejects_destructive_test_without_review():
    with pytest.raises(ValueError, match="destructive"):
        SymbiontMCPTestHarness().benchmark(_descriptor(), _case(non_destructive=False), _request(), endpoint="http://hermes.test", transport=_transport)


def test_mcp_harness_requires_traceable_evidence():
    def no_ids(endpoint, payload):
        result = _transport(endpoint, payload)
        result["evidence"] = ({"type": "execution"},)
        return result
    with pytest.raises(ValueError, match="traceable evidence"):
        SymbiontMCPTestHarness().benchmark(_descriptor(), _case(), _request(), endpoint="http://hermes.test", transport=no_ids)
