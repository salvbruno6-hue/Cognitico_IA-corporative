"""ELO-owned runtime handoff for Hermes Skills Factory execution.

This module does not execute Hermes or call OpenAI/Supabase directly. It converts a
validated specialist intent into an ELO-governed execution envelope and makes the
expected execution contract explicit for the Hermes-side adapter.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

FORBIDDEN_INFRASTRUCTURE_KEYS = frozenset(
    {"project_id", "project_ref", "supabase_project", "database_url", "supabase_url"}
)

ALLOWED_SKILL_STATES = frozenset({"candidate_only", "pending", "rejected"})


@dataclass(frozen=True)
class IntentSpec:
    """Structured intent produced by the GPT interpretation layer."""

    request_id: str
    intent: str
    tenant_scope: str
    mission_class: str
    authorized_capabilities: tuple[str, ...]
    skill_name: str | None = None
    context: Mapping[str, Any] = field(default_factory=dict)
    evidence_requirements: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name, value in (
            ("request_id", self.request_id),
            ("intent", self.intent),
            ("tenant_scope", self.tenant_scope),
            ("mission_class", self.mission_class),
        ):
            if not value or not value.strip():
                raise ValueError(f"{name} is required")
        if not self.authorized_capabilities:
            raise ValueError("authorized_capabilities is required")
        _reject_infrastructure(self.context)

    def to_hermes_request(self) -> dict[str, Any]:
        """Produce the bridge-neutral request consumed by the Hermes adapter."""
        return {
            "request_id": self.request_id,
            "intent": self.intent,
            "tenant_scope": self.tenant_scope,
            "mission_class": self.mission_class,
            "authorized_capabilities": list(self.authorized_capabilities),
            "context": dict(self.context),
            "evidence_requirements": list(self.evidence_requirements),
            "skill_name": self.skill_name,
        }


def _reject_infrastructure(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_INFRASTRUCTURE_KEYS:
                raise ValueError(f"infrastructure field is not permitted: {key}")
            _reject_infrastructure(child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            _reject_infrastructure(child)


def validate_skill_candidate(candidate: Mapping[str, Any]) -> None:
    """Validate a Hermes-created skill as a non-canonical learning candidate."""
    _reject_infrastructure(candidate)
    state = candidate.get("promotion_state", candidate.get("status", "candidate_only"))
    if state not in ALLOWED_SKILL_STATES:
        raise ValueError("skill candidate must remain non-canonical")
    if "decision" in candidate or "canonical_knowledge" in candidate:
        raise ValueError("skill candidate cannot contain canonical authority fields")


def build_skill_execution_envelope(intent: IntentSpec) -> dict[str, Any]:
    """Create the governed envelope passed to the Hermes-side execution bridge."""
    payload = intent.to_hermes_request()
    payload["governance"] = {
        "authority": "elo_cognitive",
        "execution_runtime": "hermes",
        "learning_boundary": "candidate_only",
        "canonical_promotion": "elo_only",
    }
    _reject_infrastructure(payload)
    return payload
