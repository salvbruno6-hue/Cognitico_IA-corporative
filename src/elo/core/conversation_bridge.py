"""Zero-infrastructure bridge between authorized chat and ELO temporal intake.

The bridge is transport-neutral. It serializes an authorized conversation or
provider response into a deterministic JSON event. The event is first held in
temporal context; permanent promotion remains a separate governed operation.
"""

from dataclasses import asdict, dataclass
import json
from typing import Mapping

from .conversation_intake import ConversationEvent, ConversationIntake, ConversationIntakeResult


@dataclass(frozen=True)
class ChatBridgeEvent:
    conversation_id: str
    tenant_id: str
    domain: str
    principal: str
    session_id: str
    request_id: str
    correlation_id: str
    source_id: str
    content: str
    authorized: bool
    provenance: Mapping[str, str]
    source_type: str = "CHATGPT"
    schema_version: str = "1.1"
    event_role: str = "CONVERSATION"

    def validate(self) -> None:
        required = {
            "conversation_id": self.conversation_id,
            "tenant_id": self.tenant_id,
            "domain": self.domain,
            "principal": self.principal,
            "session_id": self.session_id,
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "source_id": self.source_id,
            "content": self.content,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ValueError(f"missing required bridge fields: {', '.join(missing)}")
        if not self.authorized:
            raise PermissionError("conversation bridge event is not authorized")
        if self.source_type not in {"CHATGPT", "CLAUDE", "GEMINI", "OTHER_PROVIDER"}:
            raise ValueError(f"unsupported source_type: {self.source_type}")
        if self.event_role not in {"CONVERSATION", "EXTERNAL_PROVIDER_RESPONSE"}:
            raise ValueError(f"unsupported event_role: {self.event_role}")
        if not self.provenance:
            raise ValueError("provenance is required")

    def to_json(self) -> str:
        self.validate()
        return json.dumps(asdict(self), ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    @classmethod
    def from_json(cls, content: str) -> "ChatBridgeEvent":
        event = cls(**json.loads(content))
        event.validate()
        return event

    def to_conversation_event(self) -> ConversationEvent:
        self.validate()
        return ConversationEvent(
            conversation_id=self.conversation_id,
            tenant_id=self.tenant_id,
            domain=self.domain,
            principal=self.principal,
            session_id=self.session_id,
            request_id=self.request_id,
            correlation_id=self.correlation_id,
            source_type=self.source_type,
            source_id=self.source_id,
            content=self.content,
            authorized=self.authorized,
            provenance=self.provenance,
        )


class ChatBridge:
    """Translate portable events into the canonical ELO temporal intake."""

    def __init__(self, intake: ConversationIntake) -> None:
        self._intake = intake

    def ingest(self, event: ChatBridgeEvent) -> ConversationIntakeResult:
        return self._intake.ingest(event.to_conversation_event())
