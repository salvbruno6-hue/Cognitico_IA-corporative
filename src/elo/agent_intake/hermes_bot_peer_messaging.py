"""Candidate-only durable peer-message evidence over ELO delegation ownership."""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256

@dataclass(frozen=True, slots=True)
class PeerMessage:
    message_id: str
    tenant_scope: str
    sender_agent_id: str
    recipient_agent_id: str
    body_digest: str
    provenance_ref: str
    durable: bool = True

@dataclass(frozen=True, slots=True)
class PeerMessageAssessment:
    valid: bool
    reason: str
    delivery_permitted: bool = False

def build_peer_message(message_id: str, tenant_scope: str, sender_agent_id: str,
                       recipient_agent_id: str, body: str, provenance_ref: str) -> PeerMessage:
    values=(message_id,tenant_scope,sender_agent_id,recipient_agent_id,body,provenance_ref)
    if not all(v.strip() for v in values):
        raise ValueError("peer message identity, body and provenance are required")
    digest=sha256(body.encode("utf-8")).hexdigest()
    return PeerMessage(message_id,tenant_scope,sender_agent_id,recipient_agent_id,digest,provenance_ref)

def assess_peer_message(message: PeerMessage) -> PeerMessageAssessment:
    if message.sender_agent_id == message.recipient_agent_id:
        return PeerMessageAssessment(False,"self_delivery_not_peer_message")
    if not message.durable:
        return PeerMessageAssessment(False,"durability_required")
    return PeerMessageAssessment(True,"peer_message_contract_valid",False)
