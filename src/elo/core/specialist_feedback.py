"""Governed specialist-feedback admission without historical mutation."""
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class SpecialistFeedback:
    feedback_id: str
    specialist_id: str
    tenant_id: str
    domain: str
    source_reference: str
    observation: str
    evidence_ids: tuple[str, ...]
    provenance: Mapping[str, str]
    valid_from: str | None = None
    valid_to: str | None = None

    def __post_init__(self) -> None:
        if not all((self.feedback_id, self.specialist_id, self.tenant_id, self.domain, self.source_reference, self.observation)):
            raise ValueError("feedback identity/context fields are required")
        if not self.evidence_ids or not self.provenance:
            raise ValueError("feedback requires evidence and provenance")


class SpecialistFeedbackRegistry:
    """Append-only contextual feedback registry; historical records are never edited."""
    def __init__(self) -> None:
        self._records: dict[str, SpecialistFeedback] = {}

    def ingest(self, feedback: SpecialistFeedback) -> SpecialistFeedback:
        if feedback.feedback_id in self._records:
            raise ValueError("feedback_id already exists; historical feedback is immutable")
        self._records[feedback.feedback_id] = feedback
        return feedback

    def list(self, *, tenant_id: str, domain: str) -> tuple[SpecialistFeedback, ...]:
        return tuple(item for item in self._records.values() if item.tenant_id == tenant_id and item.domain == domain)
