"""Canonical contracts for the ELO cognitive interface."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SourceReference(BaseModel):
    source_id: str
    source_type: str
    title: str | None = None
    uri: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentReference(BaseModel):
    agent_id: str
    role: str | None = None
    provider: str | None = None
    model: str | None = None


class SuggestedAction(BaseModel):
    action_id: str = Field(default_factory=lambda: str(uuid4()))
    label: str
    action_type: str = "suggestion"
    payload: dict[str, Any] = Field(default_factory=dict)
    requires_approval: bool = False


class Provenance(BaseModel):
    request_id: str
    provider: str | None = None
    model: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    policy_decision: str | None = None
    validation_status: str | None = None
    generated_at: datetime = Field(default_factory=utc_now)
    metadata: dict[str, Any] = Field(default_factory=dict)


class CognitiveRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    message: str = Field(min_length=1)
    session_id: str | None = None
    user_id: str | None = None
    tenant_id: str | None = None
    domain: str | None = None
    context: dict[str, Any] = Field(default_factory=dict)


class CognitiveResponse(BaseModel):
    response_id: str = Field(default_factory=lambda: str(uuid4()))
    request_id: str
    session_id: str
    domain: str | None = None
    response: dict[str, Any]
    sources: list[SourceReference] = Field(default_factory=list)
    agents_used: list[AgentReference] = Field(default_factory=list)
    confidence: float = 0.0
    provenance: Provenance
    suggestions: list[SuggestedAction] = Field(default_factory=list)
    processing_time_ms: float = 0.0
    timestamp: datetime = Field(default_factory=utc_now)

    @field_validator("confidence")
    @classmethod
    def normalize_confidence(cls, value: float) -> float:
        return max(0.0, min(1.0, float(value)))
