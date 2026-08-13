"""Canonical contracts for governed ELO specialist agents."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


AUTONOMY_LEVELS = ("OBSERVE", "ANALYZE", "RECOMMEND", "APPROVAL_REQUIRED", "POLICY_LIMITED")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class AgentIdentity:
    agent_id: str
    tenant_id: str
    domain: str
    role: str
    version: str = "1.0"


@dataclass(frozen=True, slots=True)
class AgentCapability:
    capability_id: str
    name: str
    description: str = ""
    autonomy_level: str = "ANALYZE"
    allowed_tools: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.autonomy_level not in AUTONOMY_LEVELS:
            raise ValueError(f"unsupported autonomy level: {self.autonomy_level}")


@dataclass(frozen=True, slots=True)
class AgentTask:
    task_id: str = field(default_factory=lambda: str(uuid4()))
    tenant_id: str = ""
    domain: str = ""
    capability_id: str = ""
    instruction: str = ""
    request_id: str = ""
    correlation_id: str = ""
    requires_approval: bool = True


@dataclass(frozen=True, slots=True)
class AgentReport:
    report_id: str = field(default_factory=lambda: str(uuid4()))
    agent_id: str = ""
    tenant_id: str = ""
    domain: str = ""
    task_id: str = ""
    observation: str = ""
    evidence_refs: tuple[str, ...] = ()
    confidence: float = 0.0
    provenance: dict[str, object] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
