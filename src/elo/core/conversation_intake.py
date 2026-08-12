"""Canonical intake boundary for authorized conversations with AI providers.

Conversation text is not canonical memory. It is transformed into a
provenance-bearing event and routed through KnowledgeAdmission before any
retention or promotion occurs.
"""

from dataclasses import dataclass
from typing import Literal, Mapping

from .evolution_memory import EvolutionMemory, EvolutionRecord
from .knowledge_admission import AdmissionRequest, AdmissionResult, KnowledgeAdmission

ConversationKind = Literal["CHATGPT", "CLAUDE", "GEMINI", "OTHER_PROVIDER", "GITHUB", "SYSTEM"]


@dataclass(frozen=True)
class ConversationEvent:
    """Authorized conversation event with mandatory execution context."""

    conversation_id: str
    tenant_id: str
    domain: str
    principal: str
    session_id: str
    request_id: str
    correlation_id: str
    source_type: ConversationKind
    source_id: str
    content: str
    authorized: bool
    provenance: Mapping[str, str]


@dataclass(frozen=True)
class ConversationIntakeResult:
    """Result of the admission stage."""

    admission: AdmissionResult
    evolution_id: str | None = None


class ConversationIntake:
    """Convert authorized conversations into governed retention records."""

    def __init__(self, admission: KnowledgeAdmission, evolution_memory: EvolutionMemory) -> None:
        self._admission = admission
        self._evolution_memory = evolution_memory

    def ingest(self, event: ConversationEvent) -> ConversationIntakeResult:
        request = AdmissionRequest(
            tenant_id=event.tenant_id,
            domain=event.domain,
            source_type=event.source_type,
            source_id=event.source_id,
            content=event.content,
            provenance=event.provenance,
            authorized=event.authorized,
            relevant=True,
        )
        admission = self._admission.evaluate(request)
        if admission.outcome in {"REJECT", "ARCHIVE"}:
            return ConversationIntakeResult(admission=admission)

        evolution_id = f"conv:{event.conversation_id}"
        self._evolution_memory.store(
            EvolutionRecord(
                evolution_id=evolution_id,
                tenant_id=event.tenant_id,
                domain=event.domain,
                source_type="CONVERSATION",
                source_id=event.source_id,
                content=event.content,
                status="OBSERVATION",
                provenance={
                    **dict(event.provenance),
                    "conversation_id": event.conversation_id,
                    "request_id": event.request_id,
                    "correlation_id": event.correlation_id,
                    "principal": event.principal,
                    "session_id": event.session_id,
                },
            )
        )
        return ConversationIntakeResult(admission=admission, evolution_id=evolution_id)
