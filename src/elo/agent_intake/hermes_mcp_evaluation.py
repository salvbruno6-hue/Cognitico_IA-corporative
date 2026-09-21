"""Controlled governed-loop evaluation for EXT-MCP-HERMES.

The evaluator reuses the existing native MCP contract and MCP test harness.
It measures recognition/pass-rate only; it never grants external authority,
executes real MCP infrastructure, mutates canonical state, or promotes a
candidate.
"""
from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.agents.hermes_contract import HermesExecutionRequest
from elo.cognitive.symbiont_mcp_test_harness import SymbiontMCPTestHarness
from elo.cognitive.symbiont_mcp_contracts import (
    MCPCapabilityDescriptor,
    MCPCapabilityTestCase,
    MCPTestDisposition,
)

CAPABILITY_ID = "EXT-MCP-HERMES"
METRIC = "governed_mcp_benchmark_pass_rate"
METRIC_DIRECTION = "maximize"


@dataclass(frozen=True, slots=True)
class MCPEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str


def _descriptor(i: int) -> MCPCapabilityDescriptor:
    capability = f"mcp:fixture:read:{i}"
    return MCPCapabilityDescriptor(
        capability,
        "fixture",
        "fixture-provider",
        "read",
        "controlled read",
        "controlled fixture read",
        {"type": "object"},
        f"fixture://mcp/{i}",
        "controlled-fixture",
        "multiteiner",
        "evaluation",
    )


def _case(i: int) -> MCPCapabilityTestCase:
    capability = f"mcp:fixture:read:{i}"
    return MCPCapabilityTestCase(
        f"mcp-governed-{i}",
        capability,
        "multiteiner",
        "verify controlled read",
        "read fixture",
        {"value": i},
        ("result is ok",),
        ("execution", "outcome"),
        non_destructive=True,
    )


def _request(i: int) -> HermesExecutionRequest:
    capability = f"mcp:fixture:read:{i}"
    return HermesExecutionRequest(
        f"mcp-request-{i}",
        "benchmark MCP capability",
        {"domain": "evaluation"},
        "multiteiner",
        "mcp_benchmark",
        (capability,),
        evidence_requirements=("execution", "outcome"),
        constraints={},
        execution_policy={"max_tool_calls": 10},
    )


def _transport(endpoint, payload):
    request_id = payload["request_id"]
    return {
        "request_id": request_id,
        "status": "completed",
        "execution": {"runtime": "controlled-fixture"},
        "evidence": ({"evidence_id": f"ev-{request_id}"},),
        "outcome": {"result": "ok"},
        "tool_usage": ({"tool": "fixture.read"},),
        "metrics": {
            "task_success_score": 1.0,
            "reliability_score": 1.0,
            "quality_score": 1.0,
            "latency_score": 1.0,
        },
        "learning_candidate": {"promotion_state": "candidate_only"},
    }


def _native_baseline_rate() -> float:
    # Baseline is the existing ELO-native gateway contract: all five controlled
    # allowlist probes must remain authorized and bounded.
    return 1.0


def _run_harness(prefix: str) -> tuple[float, bool]:
    passed = 0
    boundary_ok = 0
    harness = SymbiontMCPTestHarness()
    for i in range(1, 6):
        benchmark = harness.benchmark(
            _descriptor(i),
            _case(i),
            _request(i),
            endpoint=f"fixture://{prefix}/{i}",
            transport=_transport,
        )
        if benchmark.result.disposition == MCPTestDisposition.PASS:
            passed += 1
        if benchmark.result.candidate_only and benchmark.execution.learning_candidate.get(
            "promotion_state", "candidate_only"
        ) == "candidate_only":
            boundary_ok += 1
    return passed / 5, boundary_ok == 5


def evaluate() -> MCPEvaluation:
    baseline = _native_baseline_rate()
    adapted, boundary_ok = _run_harness("hermes")
    repeat_rate, repeat_boundary = _run_harness("repeat")
    repeatable = repeat_rate == adapted and repeat_boundary and boundary_ok
    result = "EVOLUTION_GATE_REQUIRED" if adapted > baseline and repeatable else "RETEST"
    return MCPEvaluation(
        baseline_rate=baseline,
        adapted_rate=adapted,
        boundary_integrity_rate=1.0 if boundary_ok else 0.0,
        repeatable=repeatable,
        result=result,
    )


__all__ = [
    "CAPABILITY_ID",
    "METRIC",
    "METRIC_DIRECTION",
    "MCPEvaluation",
    "evaluate",
]
