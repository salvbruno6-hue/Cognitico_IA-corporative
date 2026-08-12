"""Temporal conversation memory for governed ELO consulting sessions.

Temporal memory is a session-scoped working buffer. It may contain user
conversation, external-provider responses, evidence, analyses and provisional
conclusions. Nothing in this layer is canonical merely because it was observed.
Promotion to Evolution Memory, Evidence, Knowledge or Decision is explicit and
must pass the existing admission/governance path.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Mapping


@dataclass(frozen=True)
class TemporalRecord:
    """One authorized observation held only in temporal session context."""

    record_id: str
    conversation_id: str
    source_type: str
    content: str
    provenance: Mapping[str, str]
    created_at: str
    classification: str = "OBSERVATION"
    metadata: Mapping[str, str] = field(default_factory=dict)


class TemporalConversationMemory:
    """Session-scoped buffer used before permanent admission/promotion."""

    def __init__(self) -> None:
        self._records: dict[str, list[TemporalRecord]] = {}

    def append(
        self,
        *,
        conversation_id: str,
        record_id: str,
        source_type: str,
        content: str,
        provenance: Mapping[str, str],
        classification: str = "OBSERVATION",
        metadata: Mapping[str, str] | None = None,
    ) -> TemporalRecord:
        if not conversation_id:
            raise ValueError("conversation_id is required")
        if not record_id:
            raise ValueError("record_id is required")
        if not content:
            raise ValueError("content is required")
        if not provenance:
            raise ValueError("provenance is required")

        record = TemporalRecord(
            record_id=record_id,
            conversation_id=conversation_id,
            source_type=source_type,
            content=content,
            provenance=dict(provenance),
            created_at=datetime.now(timezone.utc).isoformat(),
            classification=classification,
            metadata=dict(metadata or {}),
        )
        self._records.setdefault(conversation_id, []).append(record)
        return record

    def list(self, conversation_id: str) -> tuple[TemporalRecord, ...]:
        return tuple(self._records.get(conversation_id, ()))

    def snapshot(self, conversation_id: str) -> tuple[TemporalRecord, ...]:
        """Return the complete temporary context for consultant analysis."""
        return self.list(conversation_id)

    def clear(self, conversation_id: str) -> tuple[TemporalRecord, ...]:
        """Expire the temporal context and return what was removed."""
        return tuple(self._records.pop(conversation_id, ()))
