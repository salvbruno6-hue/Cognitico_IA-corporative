"""Controlled MCP capability test harness.

The harness composes existing ELO contracts and the governed Symbiont -> Hermes
bridge. It provides repeatable experimental execution without installing MCP
servers or creating another authorization/evolution authority.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .symbiont_hermes_bridge import SymbiontExecutionReceipt, SymbiontHermesBridge
from .symbiont_mcp_contracts import (
    MCPCapabilityBenchmarkResult,
    MCPCapabilityDescriptor,
    MCPCapabilityTestCase,
    MCPRecommendation,
    MCPTestDisposition,
)
from .agents.hermes_contract import HermesExecutionRequest
from .agents.hermes_runtime import Transport


@dataclass(frozen=True)
class MCPHarnessRun:
    """One controlled test execution and its candidate-only benchmark result."""

    descriptor: MCPCapabilityDescriptor
    test_case: MCPCapabilityTestCase
    receipt: SymbiontExecutionReceipt
    benchmark: MCPCapabilityBenchmarkResult


class SymbiontMCPTestHarness:
    """Run bounded MCP experiments through the existing governed bridge."""

    def __init__(self, bridge: SymbiontHermesBridge | None = None) -> None:
        self._bridge = bridge or SymbiontHermesBridge()

    def run(
        self,
        descriptor: MCPCapabilityDescriptor,
        test_case: MCPCapabilityTestCase,
        request: HermesExecutionRequest,
        *,
        endpoint: str,
        transport: Transport | None = None,
    ) -> MCPHarnessRun:
        """Execute a test and normalize its evidence into a benchmark result."""
        self._validate_alignment(descriptor, test_case, request)
        receipt = self._bridge.execute(
            request,
            capability=descriptor.capability_id,
            endpoint=endpoint,
            transport=transport,
        )
        benchmark = self._benchmark(descriptor, test_case, receipt)
        return MCPHarnessRun(descriptor, test_case, receipt, benchmark)

    @staticmethod
    def _validate_alignment(
        descriptor: MCPCapabilityDescriptor,
        test_case: MCPCapabilityTestCase,
        request: HermesExecutionRequest,
    ) -> None:
        if descriptor.capability_id != test_case.capability_id:
            raise ValueError("descriptor and test case capability_id do not match")
        if descriptor.tenant_id != test_case.tenant_id or descriptor.tenant_id != request.tenant_scope:
            raise ValueError("MCP experiment tenant scope does not match ELO request")
        if descriptor.capability_id not in request.authorized_capabilities:
            raise ValueError("MCP capability is not authorized by ELO request")
        if test_case.max_tool_calls < 1:
            raise ValueError("MCP test must allow at least one tool call")
        if not test_case.non_destructive and not test_case.constraints.get("explicit_review"):
            raise ValueError("destructive MCP tests require explicit_review")

    @staticmethod
    def _benchmark(
        descriptor: MCPCapabilityDescriptor,
        test_case: MCPCapabilityTestCase,
        receipt: SymbiontExecutionReceipt,
    ) -> MCPCapabilityBenchmarkResult:
        result = receipt.result
        outcome = dict(result.outcome or {})
        metrics = result.metrics if isinstance(result.metrics, Mapping) else {}

        scores = {
            "task_success_score": SymbiontMCPTestHarness._metric(metrics, "task_success_score"),
            "reliability_score": SymbiontMCPTestHarness._metric(metrics, "reliability_score"),
            "quality_score": SymbiontMCPTestHarness._metric(metrics, "quality_score"),
            "latency_score": SymbiontMCPTestHarness._metric(metrics, "latency_score"),
        }
        evidence_ids = tuple(str(item) for item in result.evidence.keys()) if isinstance(result.evidence, Mapping) else ()
        if not evidence_ids:
            evidence_ids = tuple(str(item) for item in test_case.evidence_requirements)

        disposition = {
            "completed": MCPTestDisposition.PASS,
            "partial": MCPTestDisposition.PARTIAL,
            "failed": MCPTestDisposition.FAIL,
            "blocked": MCPTestDisposition.BLOCKED,
        }[result.status]
        recommendation = MCPRecommendation.LAB_CANDIDATE if disposition is MCPTestDisposition.PASS else MCPRecommendation.ADAPT

        return MCPCapabilityBenchmarkResult(
            test_id=test_case.test_id,
            capability_id=descriptor.capability_id,
            request_id=receipt.request_id,
            tenant_id=descriptor.tenant_id,
            disposition=disposition,
            evidence_ids=evidence_ids,
            outcome=outcome,
            tool_usage=tuple(result.tool_usage or ()),
            gaps=tuple(result.gaps or ()),
            conflicts=tuple(result.conflicts or ()),
            recommendation=recommendation,
            candidate_only=True,
            **scores,
        )

    @staticmethod
    def _metric(metrics: Mapping[str, Any], name: str) -> float:
        value = metrics.get(name, 0.0)
        if isinstance(value, bool):
            raise ValueError(f"{name} must be numeric")
        try:
            score = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{name} must be numeric") from exc
        if not 0.0 <= score <= 1.0:
            raise ValueError(f"{name} must be between 0 and 1")
        return score


__all__ = ["MCPHarnessRun", "SymbiontMCPTestHarness"]
