"""Canonical intake boundary for authorized conversations with AI providers.

Conversation text and external-provider responses first enter TemporalConversationMemory.
Only an explicit promotion path may move material into EvolutionMemory, Evidence,
Knowledge or Decision. Temporal context is never canonical merely because it was observed.
"""

from dataclasses import dataclass
from typing import Literal, Mapping

from .evolution_memory import EvolutionMemory, EvolutionRecord
from .knowledge_admission import AdmissionRequest, AdmissionResult, KnowledgeAdmission
from .temporal_memory import TemporalConversationMemory

ConversationKind = Literal["CHATGPT", "CLAUDE", "GEMINI", "OTHER_PROVIDER", "GITHUB", "SYSTEM"]


@dataclass(frozen=True)
class ConversationEvent:
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
    admission: AdmissionResult
    evolution_id: str | None = None
    temporal_record_id: str | None = None


class ConversationIntake:
    """Place authorized events in temporal context before any permanent promotion."""

    def __init__(
        self,
        admission: KnowledgeAdmission,
        evolution_memory: EvolutionMemory,
        temporal_memory: TemporalConversationMemory | None = None,
    ) -> None:
        self._admission = admission
        self._evolution_memory = evolution_memory
        self._temporal_memory = temporal_memory or TemporalConversationMemory()

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
        if admission.outcome == "REJECT":
            return ConversationIntakeResult(admission=admission)

        temporal_id = f"temporal:{event.conversation_id}:{event.request_id}"
        self._temporal_memory.append(
            conversation_id=event.conversation_id,
            record_id=temporal_id,
            source_type=event.source_type,
            content=event.content,
            provenance={
                **dict(event.provenance),
                "conversation_id": event.conversation_id,
                "request_id": event.request_id,
                "correlation_id": event.correlation_id,
            },
            metadata={
                "tenant_id": event.tenant_id,
                "domain": event.domain,
                "principal": event.principal,
                "session_id": event.session_id,
            },
        )

        # ARCHIVE remains temporal/history only. It is not promoted.
        if admission.outcome == "ARCHIVE":
            return ConversationIntakeResult(admission=admission, temporal_record_id=temporal_id)

        # Existing admission contract permits retention, but promotion is kept explicit:
        # callers may use promote_temporal() after analysis/decision.
        return ConversationIntakeResult(admission=admission, temporal_record_id=temporal_id)

    def temporal_context(self, conversation_id: str):
        return self._temporal_memory.snapshot(conversation_id)

    def promote_temporal(
        self,
        *,
        conversation_id: str,
        evolution_id: str,
        tenant_id: str,
        domain: str,
        source_id: str,
        status: str = "OBSERVATION",
    ) -> EvolutionRecord:
        records = self._temporal_memory.snapshot(conversation_id)
        if not records:
            raise ValueError("no temporal context exists for conversation")
        content = "\n\n".join(record.content for record in records)
        provenance = {"conversation_id": conversation_id, "promotion": "explicit"}
        for record in records:
            provenance.update(dict(record.provenance))
        result = EvolutionRecord(
            evolution_id=evolution_id,
            tenant_id=tenant_id,
            domain=domain,
            source_type="CONVERSATION",
            source_id=source_id,
            content=content,
            status=status,
            provenance=provenance,
        )
        self._evolution_memory.store(result)
        return result
