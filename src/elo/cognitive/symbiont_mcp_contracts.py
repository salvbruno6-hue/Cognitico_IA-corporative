"""Governed contracts for discovering and benchmarking external MCP capabilities.

MCP is an external capability transport. These contracts keep discovery,
testing, evidence and candidate evaluation inside ELO governance without
granting an MCP server canonical authority.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any, Mapping


CONTRACT_VERSION = "1.0"


class MCPCapabilityState(StrEnum):
    DISCOVERED = "DISCOVERED"
    TESTABLE = "TESTABLE"
    TESTED = "TESTED"
    CANDIDATE = "CANDIDATE"
    BLOCKED = "BLOCKED"


class MCPTestDisposition(StrEnum):
    PASS = "PASS"
    PARTIAL = "PARTIAL"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"


class MCPRecommendation(StrEnum):
    REUSE = "REUSE"
    ADAPT = "ADAPT"
    LAB_CANDIDATE = "LAB_CANDIDATE"
    BLOCK = "BLOCK"


_FORBIDDEN_KEYS = frozenset(
    {"project_id", "project_ref", "supabase_project", "database_url", "service_role_key"}
)


def _reject_forbidden(value: Any, path: str) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).lower() in _FORBIDDEN_KEYS:
                raise ValueError(f"infrastructure/secret field is not allowed: {path}.{key}")
            _reject_forbidden(child, f"{path}.{key}")
    elif isinstance(value, (tuple, list)):
        for index, child in enumerate(value):
            _reject_forbidden(child, f"{path}[{index}]")


def _required(value: str, name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{name} is required")


def _score(value: float, name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")


@dataclass(frozen=True)
class MCPCapabilityDescriptor:
    """Evidence-bearing description of an externally discovered MCP capability."""

    capability_id: str
    server_id: str
    provider: str
    tool_name: str
    purpose: str
    mechanism: str
    interface_contract: Mapping[str, Any]
    source_ref: str
    source_commit: str
    tenant_id: str
    domain: str
    risk: str = "LOW"
    state: MCPCapabilityState = MCPCapabilityState.DISCOVERED
    contract_version: str = CONTRACT_VERSION

    def __post_init__(self) -> None:
        for value, name in (
            (self.capability_id, "capability_id"),
            (self.server_id, "server_id"),
            (self.provider, "provider"),
            (self.tool_name, "tool_name"),
            (self.purpose, "purpose"),
            (self.mechanism, "mechanism"),
            (self.source_ref, "source_ref"),
            (self.source_commit, "source_commit"),
            (self.tenant_id, "tenant_id"),
            (self.domain, "domain"),
        ):
            _required(value, name)
        if not self.interface_contract:
            raise ValueError("interface_contract is required")
        if self.contract_version != CONTRACT_VERSION:
            raise ValueError(f"unsupported contract_version: {self.contract_version}")
        _reject_forbidden(self.interface_contract, "interface_contract")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MCPCapabilityTestCase:
    """Controlled benchmark contract executed through an authorized Hermes mission."""

    test_id: str
    capability_id: str
    tenant_id: str
    objective: str
    task: str
    input_payload: Mapping[str, Any]
    success_criteria: tuple[str, ...]
    evidence_requirements: tuple[str, ...]
    constraints: Mapping[str, Any] = field(default_factory=dict)
    non_destructive: bool = True
    max_tool_calls: int = 10
    contract_version: str = CONTRACT_VERSION

    def __post_init__(self) -> None:
        for value, name in (
            (self.test_id, "test_id"),
            (self.capability_id, "capability_id"),
            (self.tenant_id, "tenant_id"),
            (self.objective, "objective"),
            (self.task, "task"),
        ):
            _required(value, name)
        if not self.success_criteria:
            raise ValueError("success_criteria is required")
        if not self.evidence_requirements:
            raise ValueError("evidence_requirements is required")
        if self.max_tool_calls < 1:
            raise ValueError("max_tool_calls must be positive")
        if self.contract_version != CONTRACT_VERSION:
            raise ValueError(f"unsupported contract_version: {self.contract_version}")
        _reject_forbidden(self.input_payload, "input_payload")
        _reject_forbidden(self.constraints, "constraints")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MCPCapabilityBenchmarkResult:
    """Evidence/outcome returned after a governed MCP benchmark."""

    test_id: str
    capability_id: str
    request_id: str
    tenant_id: str
    disposition: MCPTestDisposition
    task_success_score: float
    reliability_score: float
    quality_score: float
    latency_score: float
    evidence_ids: tuple[str, ...]
    outcome: Mapping[str, Any]
    tool_usage: tuple[Mapping[str, Any], ...] = ()
    gaps: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    recommendation: MCPRecommendation = MCPRecommendation.ADAPT
    candidate_only: bool = True
    contract_version: str = CONTRACT_VERSION

    def __post_init__(self) -> None:
        for value, name in (
            (self.test_id, "test_id"),
            (self.capability_id, "capability_id"),
            (self.request_id, "request_id"),
            (self.tenant_id, "tenant_id"),
        ):
            _required(value, name)
        for value, name in (
            (self.task_success_score, "task_success_score"),
            (self.reliability_score, "reliability_score"),
            (self.quality_score, "quality_score"),
            (self.latency_score, "latency_score"),
        ):
            _score(value, name)
        if not self.evidence_ids:
            raise ValueError("evidence_ids are required")
        if not self.outcome:
            raise ValueError("outcome is required")
        if not self.candidate_only:
            raise ValueError("MCP benchmark results cannot be directly promoted")
        if self.contract_version != CONTRACT_VERSION:
            raise ValueError(f"unsupported contract_version: {self.contract_version}")
        _reject_forbidden(self.outcome, "outcome")
        _reject_forbidden(self.tool_usage, "tool_usage")

    @property
    def aggregate_score(self) -> float:
        """Deterministic benchmark score; governance still decides promotion."""
        return round(
            (
                self.task_success_score
                + self.reliability_score
                + self.quality_score
                + self.latency_score
            )
            / 4.0,
            4,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
