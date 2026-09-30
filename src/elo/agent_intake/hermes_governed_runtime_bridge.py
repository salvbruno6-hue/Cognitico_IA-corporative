"""Canonical ELO adapter for an already-authorized Hermes runtime.

The adapter transports canonical authorization into the external Hermes
contract. It does not issue authorization, infer capabilities, promote
learning, or mutate canonical state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol

from elo.application.use_cases.orchestrator import AuthorizationDecision


class HermesRuntimeClient(Protocol):
    """Transport boundary implemented by the actual Hermes runtime client."""

    def execute(self, payload: Mapping[str, Any]) -> Mapping[str, Any]:
        """Execute an already-admitted Hermes request."""


@dataclass(frozen=True, slots=True)
class HermesGovernedRequest:
    request_id: str
    tenant_scope: str
    mission_class: str
    intent: str
    skill_id: str
    decision_id: str
    authorized_capabilities: tuple[str, ...]
    evidence_requirements: tuple[str, ...] = ()
    context: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.request_id,
                self.tenant_scope,
                self.mission_class,
                self.intent,
                self.skill_id,
                self.decision_id,
            )
        ):
            raise ValueError("governed Hermes request identity is incomplete")
        if not self.authorized_capabilities:
            raise ValueError("authorized_capabilities cannot be empty")

    def to_payload(self, authorization: AuthorizationDecision) -> dict[str, Any]:
        if not authorization.is_transport_valid():
            raise PermissionError("canonical elo-authz transport authorization is invalid")
        if authorization.resource_id != self.skill_id:
            raise PermissionError("authorization resource is not bound to skill_id")

        request_context = {
            **dict(self.context),
            "skill_id": self.skill_id,
            "decision_id": self.decision_id,
            "authorization_id": authorization.grant_id,
            "authorization_evidence_ref": authorization.evidence_ref,
        }
        return {
            "contract_version": "1.0",
            "request_id": self.request_id,
            "intent": self.intent,
            "tenant_scope": self.tenant_scope,
            "mission_class": self.mission_class,
            "authorized_capabilities": list(self.authorized_capabilities),
            "context": request_context,
            "evidence_requirements": list(self.evidence_requirements),
        }


class GovernedHermesRuntimeBridge:
    """Send a canonical ELO authorization decision to Hermes exactly once."""

    def __init__(self, client: HermesRuntimeClient) -> None:
        self._client = client

    def execute(
        self,
        request: HermesGovernedRequest,
        authorization: AuthorizationDecision,
    ) -> Mapping[str, Any]:
        payload = request.to_payload(authorization)
        result = self._client.execute(payload)
        if not isinstance(result, Mapping):
            raise TypeError("Hermes runtime must return a mapping")
        if result.get("request_id") != request.request_id:
            raise ValueError("Hermes response request_id does not match ELO request")
        return result


__all__ = [
    "GovernedHermesRuntimeBridge",
    "HermesGovernedRequest",
    "HermesRuntimeClient",
]
