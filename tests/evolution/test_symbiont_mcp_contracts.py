import pytest

from elo.cognitive.symbiont_mcp_contracts import (
    MCPCapabilityBenchmarkResult,
    MCPCapabilityDescriptor,
    MCPCapabilityState,
    MCPCapabilityTestCase,
    MCPRecommendation,
    MCPTestDisposition,
)


def test_mcp_descriptor_requires_provenance_and_interface():
    descriptor = MCPCapabilityDescriptor(
        capability_id="mcp:google-sheets:read",
        server_id="google-sheets",
        provider="external",
        tool_name="read_sheet",
        purpose="read spreadsheet data",
        mechanism="MCP",
        interface_contract={"input": {"spreadsheet": "string"}},
        source_ref="mcp://google-sheets",
        source_commit="sha-001",
        tenant_id="multiteiner",
        domain="data",
    )
    assert descriptor.state is MCPCapabilityState.DISCOVERED


def test_mcp_test_case_is_non_destructive_by_default():
    case = MCPCapabilityTestCase(
        test_id="mcp-test-001",
        capability_id="mcp:google-sheets:read",
        tenant_id="multiteiner",
        objective="read a controlled test sheet",
        task="Read the test range and return structured evidence.",
        input_payload={"fixture": "controlled-sheet"},
        success_criteria=("returns expected rows", "preserves source data"),
        evidence_requirements=("execution", "outcome"),
    )
    assert case.non_destructive is True


def test_benchmark_result_is_always_candidate_only():
    result = MCPCapabilityBenchmarkResult(
        test_id="mcp-test-001",
        capability_id="mcp:google-sheets:read",
        request_id="req-001",
        tenant_id="multiteiner",
        disposition=MCPTestDisposition.PASS,
        task_success_score=1.0,
        reliability_score=0.9,
        quality_score=0.9,
        latency_score=0.8,
        evidence_ids=("e-001",),
        outcome={"rows_read": 10},
        recommendation=MCPRecommendation.LAB_CANDIDATE,
    )
    assert result.candidate_only is True
    assert result.aggregate_score == 0.9


def test_contract_rejects_infrastructure_secrets():
    with pytest.raises(ValueError, match="infrastructure/secret"):
        MCPCapabilityTestCase(
            test_id="mcp-test-002",
            capability_id="mcp:browser:navigate",
            tenant_id="multiteiner",
            objective="test navigation",
            task="Open a controlled page.",
            input_payload={"service_role_key": "secret"},
            success_criteria=("page loads",),
            evidence_requirements=("execution",),
        )


def test_benchmark_cannot_be_directly_promoted():
    with pytest.raises(ValueError, match="cannot be directly promoted"):
        MCPCapabilityBenchmarkResult(
            test_id="mcp-test-003",
            capability_id="mcp:youtube:search",
            request_id="req-003",
            tenant_id="multiteiner",
            disposition=MCPTestDisposition.PASS,
            task_success_score=1.0,
            reliability_score=1.0,
            quality_score=1.0,
            latency_score=1.0,
            evidence_ids=("e-003",),
            outcome={"matches": 3},
            candidate_only=False,
        )
