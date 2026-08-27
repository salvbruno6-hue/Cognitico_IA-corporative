"""Evaluation signals for ELO memory retrieval.

Memory quality is measurable and must remain distinct from memory storage.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalEvaluation:
    query_id: str
    retrieved: int
    relevant: int
    expected_relevant: int
    latency_ms: float
    tenant_isolation_ok: bool
    provenance_ok: bool

    def validate(self) -> None:
        if self.retrieved < 0 or self.relevant < 0 or self.expected_relevant < 0:
            raise ValueError("retrieval counts cannot be negative")
        if self.relevant > self.retrieved:
            raise ValueError("relevant cannot exceed retrieved")
        if self.latency_ms < 0:
            raise ValueError("latency cannot be negative")

    @property
    def precision(self) -> float:
        return self.relevant / self.retrieved if self.retrieved else 0.0

    @property
    def recall(self) -> float:
        return self.relevant / self.expected_relevant if self.expected_relevant else 0.0

    @property
    def admissible(self) -> bool:
        return self.tenant_isolation_ok and self.provenance_ok
