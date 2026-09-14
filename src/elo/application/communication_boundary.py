"""Governed communication intent; external transports remain adapters."""
from dataclasses import dataclass
from typing import Mapping


class CommunicationBoundaryError(ValueError):
    pass


@dataclass(frozen=True)
class CommunicationIntent:
    message_id: str
    tenant_id: str
    principal_id: str
    channel: str
    recipient_ref: str
    content: str
    evidence_ids: tuple[str, ...]
    provenance: Mapping[str, str]
    authorization_ref: str
    idempotency_key: str


class GovernedCommunicationBoundary:
    _SECRET_KEYS = {"password", "token", "access_token", "refresh_token", "api_key", "service_role"}

    def prepare(self, intent: CommunicationIntent) -> CommunicationIntent:
        required = (
            intent.message_id, intent.tenant_id, intent.principal_id,
            intent.channel, intent.recipient_ref, intent.content,
            intent.authorization_ref, intent.idempotency_key,
        )
        if any(not value for value in required):
            raise CommunicationBoundaryError("communication identity, authorization and content are required")
        if not intent.evidence_ids:
            raise CommunicationBoundaryError("evidence_ids are required")
        if any(key.lower() in self._SECRET_KEYS for key in intent.provenance):
            raise CommunicationBoundaryError("secret-bearing provenance is forbidden")
        return intent
