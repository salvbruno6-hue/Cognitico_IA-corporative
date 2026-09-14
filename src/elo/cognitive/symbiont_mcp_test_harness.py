"""Governed laboratory harness for benchmarking an already-authorized MCP capability."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .agents.hermes_contract import HermesExecutionRequest, HermesExecutionResult
from .agents.hermes_runtime import Transport
from .symbiont_hermes_bridge import SymbiontHermesBridge
from .symbiont_mcp_contracts import (
    MCPCapabilityBenchmarkResult,
    MCPCapabilityDescriptor,
    MCPCapabilityTestCase,
    MCPRecommendation,
    MCPTestDisposition,
)


@dataclass(frozen=True)
class MCPCapabilityBenchmark:
    result: MCPCapabilityBenchmarkResult
    request: HermesExecutionRequest
    execution: HermesExecutionResult


class SymbiontMCPTestHarness:
    """Benchmark one ELO-authorized MCP capability without granting authority."""

    def __init__(self, bridge: SymbiontHermesBridge | None = None) -> None:
        self._bridge = bridge or SymbiontHermesBridge()

    def benchmark(
        self,
        descriptor: MCPCapabilityDescriptor,
        test_case: MCPCapabilityTestCase,
        request: HermesExecutionRequest,
        *,
        endpoint: str,
        transport: Transport | None = None,
    ) -> MCPCapabilityBenchmark:
        self._validate_boundary(descriptor, test_case, request)
        receipt = self._bridge.execute(
            request,
            capability=descriptor.capability_id,
            endpoint=endpoint,
            transport=transport,
        )
        execution = receipt.result
        evidence_ids = self._evidence_ids(execution.evidence)
        if not evidence_ids:
            raise ValueError("MCP benchmark requires traceable evidence IDs")
        scores = self._scores(execution)
        disposition = self._disposition(execution, scores)
        recommendation = (
            MCPRecommendation.LAB_CANDIDATE
            if disposition == MCPTestDisposition.PASS
            else MCPRecommendation.BLOCK
            if disposition in {MCPTestDisposition.BLOCKED, MCPTestDisposition.FAIL}
            else MCPRecommendation.ADAPT
        )
        result = MCPCapabilityBenchmarkResult(
            test_id=test_case.test_id,
            capability_id=descriptor.capability_id,
            request_id=request.request_id,
            tenant_id=test_case.tenant_id,
            disposition=disposition,
            task_success_score=scores["task_success"],
            reliability_score=scores["reliability"],
            quality_score=scores["quality"],
            latency_score=scores["latency"],
            evidence_ids=evidence_ids,
            outcome=execution.outcome or {"status": execution.status},
            tool_usage=execution.tool_usage,
            gaps=execution.gaps,
            conflicts=execution.conflicts,
            recommendation=recommendation,
            candidate_only=True,
        )
        return MCPCapabilityBenchmark(result=result, request=request, execution=execution)

    @staticmethod
    def _validate_boundary(descriptor, test_case, request) -> None:
        if descriptor.capability_id != test_case.capability_id:
            raise ValueError("capability identity mismatch")
        if descriptor.capability_id not in request.authorized_capabilities:
            raise ValueError("MCP capability is not authorized by ELO")
        if descriptor.tenant_id != test_case.tenant_id or descriptor.tenant_id != request.tenant_scope:
            raise ValueError("tenant scope mismatch")
        if not set(test_case.evidence_requirements).issubset(set(request.evidence_requirements)):
            raise ValueError("test evidence requirements exceed ELO authorization envelope")
        if not test_case.non_destructive and not bool(request.constraints.get("destructive_test_review")):
            raise ValueError("destructive MCP tests require explicit review")
        max_calls = request.execution_policy.get("max_tool_calls")
        if max_calls is not None and test_case.max_tool_calls > int(max_calls):
            raise ValueError("MCP test exceeds authorized tool-call bound")

    @staticmethod
    def _evidence_ids(evidence) -> tuple[str, ...]:
        ids = []
        for item in evidence:
            evidence_id = item.get("evidence_id") or item.get("id")
            if isinstance(evidence_id, str) and evidence_id.strip():
                ids.append(evidence_id)
        return tuple(dict.fromkeys(ids))

    @staticmethod
    def _scores(execution: HermesExecutionResult) -> dict[str, float]:
        metrics: Mapping[str, Any] = execution.metrics
        def bounded(name: str, default: float) -> float:
            try:
                value = float(metrics.get(name, default))
            except (TypeError, ValueError):
                value = default
            return max(0.0, min(1.0, value))
        success = 1.0 if execution.status == "completed" else 0.0
        return {"task_success": bounded("task_success_score", success), "reliability": bounded("reliability_score", success), "quality": bounded("quality_score", success), "latency": bounded("latency_score", 1.0)}

    @staticmethod
    def _disposition(execution, scores) -> MCPTestDisposition:
        if execution.status == "blocked":
            return MCPTestDisposition.BLOCKED
        if execution.status == "failed":
            return MCPTestDisposition.FAIL
        if all(value >= 0.8 for value in scores.values()):
            return MCPTestDisposition.PASS
        return MCPTestDisposition.PARTIAL
