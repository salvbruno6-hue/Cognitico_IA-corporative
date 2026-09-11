import pytest

from elo.cognitive.agents.hermes_contract import HermesExecutionRequest
from elo.cognitive.symbiont_mcp_contracts import (
    MCPCapabilityDescriptor,
    MCPCapabilityTestCase,
    MCPTestDisposition,
)
from elo.cognitive.symbiont_mcp_test_harness import SymbiontMCPTestHarness


CAPABILITY = "mcp:google-sheets:read"


def _descriptor() -> MCPCapabilityDescriptor:
    return MCPCapabilityDescriptor(
        capability_id=CAPABILITY,
        server_id="google-sheets",
        provider="external",
        tool_name="read_sheet",
        purpose="read controlled spreadsheet data",
        mechanism="MCP",
        interface_contract={"input": {"spreadsheet": "string"}},
        source_ref="mcp://google-sheets",
        source_commit="sha-001",
        tenant_id="multiteiner",
        domain="data",
    )


def _test_case() -> MCPCapabilityTestCase:
    return MCPCapabilityTestCase(
        test_id="mcp-test-001",
        capability_id=CAPABILITY,
        tenant_id="multiteiner",
        objective="read a controlled test sheet",
        task="Read the test range and return structured evidence.",
        input_payload={"fixture": "controlled-sheet"},
        success_criteria=("returns expected rows", "preserves source data"),
        evidence_requirements=("execution", "outcome"),
        max_tool_calls=2,
    )


def _request() -> HermesExecutionRequest:
    return HermesExecutionRequest(
        request_id="req-mcp-001",
        intent="run controlled MCP capability benchmark",
        context={"test_id": "mcp-test-001"},
        tenant_scope="multiteiner",
        mission_class="laboratory",
        authorized_capabilities=(CAPABILITY,),
        method="mcp",
        evidence_requirements=("execution", "outcome"),
    )


def _transport(endpoint, payload):
    assert endpoint == "http://hermes.test"
    assert payload["request_id"] == "req-mcp-001"
    assert payload["authorized_capabilities"] == (CAPABILITY,)
    return {
        "request_id": "req-mcp-001",
        "status": "completed",
        "execution": {"tool": "read_sheet"},
        "evidence": ({"id": "e-mcp-001", "type": "execution"},),
        "outcome": {"rows_read": 10},
        "tool_usage": ({"tool": "read_sheet"},),
        "metrics": {
            "task_success_score": 1.0,
            "reliability_score": 0.9,
            "quality_score": 0.9,
            "latency_score": 0.8,
        },
        "learning_candidate": {"promotion_state": "candidate_only"},
    }


def test_harness_executes_authorized_mcp_experiment_and_returns_candidate_only_result():
    run = SymbiontMCPTestHarness().run(
        _descriptor(),
        _test_case(),
        _request(),
        endpoint="http://hermes.test",
        transport=_transport,
    )

    assert run.receipt.request_id == "req-mcp-001"
    assert run.benchmark.disposition is MCPTestDisposition.PASS
    assert run.benchmark.evidence_ids == ("e-mcp-001",)
    assert run.benchmark.candidate_only is True
    assert run.benchmark.aggregate_score == 0.9


def test_harness_rejects_capability_mismatch_before_execution():
    case = _test_case()
    case = MCPCapabilityTestCase(
        **{**case.to_dict(), "capability_id": "mcp:youtube:search"}
    )
    with pytest.raises(ValueError, match="capability_id do not match"):
        SymbiontMCPTestHarness().run(
            _descriptor(), case, _request(), endpoint="http://hermes.test", transport=_transport
        )


def test_harness_rejects_destructive_test_without_explicit_review():
    case = MCPCapabilityTestCase(
        **{**_test_case().to_dict(), "non_destructive": False}
    )
    with pytest.raises(ValueError, match="explicit_review"):
        SymbiontMCPTestHarness().run(
            _descriptor(), case, _request(), endpoint="http://hermes.test", transport=_transport
        )


def test_harness_rejects_more_tool_calls_than_test_budget():
    def transport(endpoint, payload):
        response = _transport(endpoint, payload)
        response["tool_usage"] = ({"tool": "a"}, {"tool": "b"}, {"tool": "c"})
        return response

    with pytest.raises(ValueError, match="max_tool_calls"):
        SymbiontMCPTestHarness().run(
            _descriptor(), _test_case(), _request(), endpoint="http://hermes.test", transport=transport
        )
