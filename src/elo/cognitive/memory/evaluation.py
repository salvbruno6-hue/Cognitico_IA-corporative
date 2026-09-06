"""Evaluation signals for ELO memory retrieval.

Memory quality is measurable and must remain distinct from memory storage.
"""
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class RetrievalEvaluation:
    """Canonical retrieval evaluation contract.

    The original count-based fields remain the canonical compatibility surface.
    Versioned ranking metrics are optional extensions of the same owner; they do
    not create a second RetrievalEvaluation authority in Core.
    """

    query_id: str
    retrieved: int
    relevant: int
    expected_relevant: int
    latency_ms: float
    tenant_isolation_ok: bool
    provenance_ok: bool
    dataset_version: str = ""
    queries: int = 0
    recall_at_k: float = 0.0
    precision_at_k: float = 0.0
    mrr: float = 0.0
    stale_hit_rate: float = 0.0
    p95_latency_ms: float = 0.0

    def validate(self) -> None:
        if self.retrieved < 0 or self.relevant < 0 or self.expected_relevant < 0:
            raise ValueError("retrieval counts cannot be negative")
        if self.relevant > self.retrieved:
            raise ValueError("relevant cannot exceed retrieved")
        if self.latency_ms < 0 or self.p95_latency_ms < 0:
            raise ValueError("latency cannot be negative")
        for name in ("recall_at_k", "precision_at_k", "mrr", "stale_hit_rate"):
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")
        if self.queries < 0:
            raise ValueError("queries cannot be negative")

    @property
    def precision(self) -> float:
        return self.relevant / self.retrieved if self.retrieved else 0.0

    @property
    def recall(self) -> float:
        return self.relevant / self.expected_relevant if self.expected_relevant else 0.0

    @property
    def admissible(self) -> bool:
        """Preserve the original admissibility boundary: isolation + provenance."""
        return self.tenant_isolation_ok and self.provenance_ok

    @property
    def quality_gate(self) -> str:
        """Fail closed on stale evidence, governance failures, or weak quality."""
        if self.stale_hit_rate > 0.0:
            return "BLOCKED_STALE"
        if not self.admissible:
            return "BLOCKED_GOVERNANCE"
        if self.queries and min(self.recall_at_k, self.precision_at_k, self.mrr) < 0.5:
            return "INSUFFICIENT_QUALITY"
        return "PASS"

    @staticmethod
    def from_rankings(
        *,
        dataset_version: str,
        queries: Sequence[Mapping[str, Any]],
        k: int = 5,
        tenant_isolation_ok: bool = False,
        provenance_ok: bool = False,
    ) -> "RetrievalEvaluation":
        """Build the canonical evaluation from already-captured rankings.

        No retriever, provider, tool, or persistence layer is invoked. Security
        and provenance assertions must be supplied as explicit evidence; this
        constructor never assumes them to be true.
        """
        if not dataset_version or k < 1 or not queries:
            raise ValueError("dataset_version, positive k and queries are required")

        recall_total = precision_total = mrr_total = stale_total = 0.0
        retrieved_total = relevant_total = expected_total = 0
        latencies: list[float] = []

        for query in queries:
            relevant = set(query.get("relevant_ids", ()))
            ranked = list(query.get("ranked_ids", ()))[:k]
            stale = set(query.get("stale_ids", ()))
            raw_latencies = tuple(float(v) for v in query.get("latency_ms", ()))
            if any(v < 0 for v in raw_latencies):
                raise ValueError("latency_ms cannot contain negative values")
            latencies.extend(raw_latencies)

            hits = len(set(ranked) & relevant)
            retrieved_total += len(ranked)
            relevant_total += hits
            expected_total += len(relevant)
            if relevant:
                recall_total += hits / len(relevant)
            precision_total += hits / k
            first_rank = next((i for i, item in enumerate(ranked, 1) if item in relevant), None)
            mrr_total += 0.0 if first_rank is None else 1.0 / first_rank
            stale_total += sum(item in stale for item in ranked) / max(len(ranked), 1)

        ordered = sorted(latencies)
        if ordered:
            rank = max(1, (95 * len(ordered) + 99) // 100)
            p95 = ordered[rank - 1]
        else:
            p95 = 0.0
        count = len(queries)
        evaluation = RetrievalEvaluation(
            query_id=dataset_version,
            retrieved=retrieved_total,
            relevant=relevant_total,
            expected_relevant=expected_total,
            latency_ms=p95,
            tenant_isolation_ok=tenant_isolation_ok,
            provenance_ok=provenance_ok,
            dataset_version=dataset_version,
            queries=count,
            recall_at_k=recall_total / count,
            precision_at_k=precision_total / count,
            mrr=mrr_total / count,
            stale_hit_rate=stale_total / count,
            p95_latency_ms=p95,
        )
        evaluation.validate()
        return evaluation
