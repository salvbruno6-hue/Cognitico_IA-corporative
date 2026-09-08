"""Governed contract between ELO Cognitive/Symbionte and an external Hermes runtime.

Hermes is an execution/orchestration provider. This module defines the ELO-owned
boundary; it does not import Hermes or grant Hermes canonical authority.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping


_CONTRACT_VERSION = "1.0"
_FORBIDDEN_INFRASTRUCTURE_KEYS = frozenset(
    {"project_id", "project_ref", "supabase_project", "database_url"}
)
_ALLOWED_RESULT_STATUS = frozenset({"completed", "partial", "blocked", "failed"})
_ALLOWED_PROMOTION_STATES = frozenset({"candidate_only", "pending", "rejected"})


def _reject_infrastructure_leaks(value: Any, path: str = "payload") -> None:
    """Reject infrastructure identifiers from crossing the ELO/Hermes boundary."""
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).lower() in _FORBIDDEN_INFRASTRUCTURE_KEYS:
                raise ValueError(f"infrastructure field is not allowed: {path}.{key}")
            _reject_infrastructure_leaks(child, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_infrastructure_leaks(child, f"{path}[{index}]")


def _validate_learning_candidate(value: Mapping[str, Any] | None) -> None:
    """Keep Hermes learning output explicitly outside canonical promotion."""
    if value is None:
        return
    if "decision" in value or "canonical_knowledge" in value:
        raise ValueError("learning_candidate cannot contain canonical decision/knowledge")
    promotion_state = value.get("promotion_state", "candidate_only")
    if promotion_state not in _ALLOWED_PROMOTION_STATES:
        raise ValueError(f"invalid learning candidate promotion_state: {promotion_state}")


@dataclass(frozen=True)
class HermesExecutionRequest:
    """ELO-authorized mission sent to Hermes for execution."""

    request_id: str
    intent: str
    context: Mapping[str, Any]
    tenant_scope: str
    mission_class: str
    authorized_capabilities: tuple[str, ...]
    method: str | None = None
    constraints: Mapping[str, Any] = field(default_factory=dict)
    evidence_requirements: tuple[str, ...] = ()
    execution_policy: Mapping[str, Any] = field(default_factory=dict)
    contract_version: str = _CONTRACT_VERSION

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id is required")
        if not self.intent.strip():
            raise ValueError("intent is required")
        if not self.tenant_scope.strip():
            raise ValueError("tenant_scope is required")
        if not self.mission_class.strip():
            raise ValueError("mission_class is required")
        if not self.authorized_capabilities:
            raise ValueError("authorized_capabilities is required")
        if self.contract_version != _CONTRACT_VERSION:
            raise ValueError(f"unsupported contract_version: {self.contract_version}")
        _reject_infrastructure_leaks(self.context, "context")
        _reject_infrastructure_leaks(self.constraints, "constraints")
        _reject_infrastructure_leaks(self.execution_policy, "execution_policy")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HermesExecutionResult:
    """Evidence-bearing result returned by Hermes; never a canonical decision."""

    request_id: str
    status: str
    execution: Mapping[str, Any] = field(default_factory=dict)
    artifacts: tuple[Mapping[str, Any], ...] = ()
    evidence: tuple[Mapping[str, Any], ...] = ()
    tool_usage: tuple[Mapping[str, Any], ...] = ()
    skills_used: tuple[str, ...] = ()
    outcome: Mapping[str, Any] = field(default_factory=dict)
    gaps: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    metrics: Mapping[str, Any] = field(default_factory=dict)
    learning_candidate: Mapping[str, Any] | None = None
    contract_version: str = _CONTRACT_VERSION

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id is required")
        if self.status not in _ALLOWED_RESULT_STATUS:
            raise ValueError(f"unsupported result status: {self.status}")
        if self.contract_version != _CONTRACT_VERSION:
            raise ValueError(f"unsupported contract_version: {self.contract_version}")
        for name, value in (
            ("execution", self.execution),
            ("artifacts", self.artifacts),
            ("evidence", self.evidence),
            ("tool_usage", self.tool_usage),
            ("outcome", self.outcome),
            ("metrics", self.metrics),
            ("learning_candidate", self.learning_candidate),
        ):
            _reject_infrastructure_leaks(value, name)
        _validate_learning_candidate(self.learning_candidate)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
