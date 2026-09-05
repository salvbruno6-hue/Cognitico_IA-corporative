"""Governed assurance contracts for ELO A15-A19.

This module is deliberately non-authoritative: it does not authorize actions,
execute tools, persist canonical knowledge, or mutate Core/Forge. It supplies
small deterministic contracts that existing retrieval, reasoning, execution,
and Evolution Gate owners can consume.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


class AssuranceError(ValueError):
    """Raised when an assurance contract cannot be constructed safely."""


def _canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True, slots=True)
class RetrievalEvaluation:
    """Deterministic retrieval-quality evidence for a fixed evaluation set."""

    dataset_version: str
    queries: int
    recall_at_k: float
    precision_at_k: float
    mrr: float
    stale_hit_rate: float
    p95_latency_ms: float

    def __post_init__(self) -> None:
        if not self.dataset_version or self.queries < 1:
            raise AssuranceError("dataset_version and a positive query count are required")
        for name in ("recall_at_k", "precision_at_k", "mrr", "stale_hit_rate"):
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                raise AssuranceError(f"{name} must be between 0 and 1")
        if self.p95_latency_ms < 0:
            raise AssuranceError("p95_latency_ms cannot be negative")

    @staticmethod
    def from_rankings(
        *,
        dataset_version: str,
        queries: Sequence[Mapping[str, Any]],
        k: int = 5,
    ) -> "RetrievalEvaluation":
        """Build retrieval metrics from deterministic query fixtures.

        Each query contains ``relevant_ids``, ``ranked_ids``, optional
        ``stale_ids`` and optional ``latency_ms``. No provider or retriever is
        invoked; this is an evaluator over already captured evidence.
        """
        if k < 1 or not queries:
            raise AssuranceError("k must be positive and queries cannot be empty")

        recall_total = precision_total = mrr_total = stale_total = 0.0
        latencies: list[float] = []
        for query in queries:
            relevant = set(query.get("relevant_ids", ()))
            ranked = list(query.get("ranked_ids", ()))[:k]
            stale = set(query.get("stale_ids", ()))
            if any(float(v) < 0 for v in query.get("latency_ms", ())):
                raise AssuranceError("latency_ms cannot contain negative values")
            latencies.extend(float(v) for v in query.get("latency_ms", ()))
            if relevant:
                recall_total += len(set(ranked) & relevant) / len(relevant)
            precision_total += len(set(ranked) & relevant) / k
            first_rank = next((i for i, item in enumerate(ranked, 1) if item in relevant), None)
            mrr_total += 0.0 if first_rank is None else 1.0 / first_rank
            stale_total += sum(item in stale for item in ranked) / max(len(ranked), 1)

        ordered = sorted(latencies)
        if not ordered:
            p95 = 0.0
        else:
            index = min(len(ordered) - 1, max(0, int(0.95 * len(ordered)) - 1))
            p95 = ordered[index]
        count = len(queries)
        return RetrievalEvaluation(
            dataset_version=dataset_version,
            queries=count,
            recall_at_k=recall_total / count,
            precision_at_k=precision_total / count,
            mrr=mrr_total / count,
            stale_hit_rate=stale_total / count,
            p95_latency_ms=p95,
        )

    @property
    def quality_gate(self) -> str:
        if self.stale_hit_rate > 0.0:
            return "BLOCKED_STALE"
        if min(self.recall_at_k, self.precision_at_k, self.mrr) < 0.5:
            return "INSUFFICIENT_QUALITY"
        return "PASS"


@dataclass(frozen=True, slots=True)
class ReplayRecord:
    """Immutable replay material; verification never invokes tools/providers."""

    execution_id: str
    input_snapshot: Mapping[str, Any]
    decision_snapshot: Mapping[str, Any]
    tool_plan: tuple[Mapping[str, Any], ...]
    result_snapshot: Mapping[str, Any]
    trace_digest: str
    world_snapshot: Mapping[str, Any] = None  # type: ignore[assignment]
    compiler_version: str = ""

    @staticmethod
    def build(
        *,
        execution_id: str,
        input_snapshot: Mapping[str, Any],
        decision_snapshot: Mapping[str, Any],
        tool_plan: tuple[Mapping[str, Any], ...],
        result_snapshot: Mapping[str, Any],
        world_snapshot: Mapping[str, Any] | None = None,
        compiler_version: str = "",
    ) -> "ReplayRecord":
        if not execution_id:
            raise AssuranceError("execution_id is required")
        world = {} if world_snapshot is None else world_snapshot
        payload = {
            "execution_id": execution_id,
            "input_snapshot": input_snapshot,
            "decision_snapshot": decision_snapshot,
            "tool_plan": tool_plan,
            "result_snapshot": result_snapshot,
            "world_snapshot": world,
            "compiler_version": compiler_version,
        }
        digest = hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()
        return ReplayRecord(execution_id, input_snapshot, decision_snapshot, tool_plan, result_snapshot, digest, world, compiler_version)

    def verify(
        self,
        *,
        expected_world_snapshot: Mapping[str, Any] | None = None,
        expected_compiler_version: str | None = None,
    ) -> bool:
        rebuilt = ReplayRecord.build(
            execution_id=self.execution_id,
            input_snapshot=self.input_snapshot,
            decision_snapshot=self.decision_snapshot,
            tool_plan=self.tool_plan,
            result_snapshot=self.result_snapshot,
            world_snapshot=self.world_snapshot,
            compiler_version=self.compiler_version,
        )
        if rebuilt.trace_digest != self.trace_digest:
            return False
        if expected_world_snapshot is not None and self.world_snapshot != expected_world_snapshot:
            return False
        if expected_compiler_version is not None and self.compiler_version != expected_compiler_version:
            return False
        return True


_REQUIRED_CLOSURE_FIELDS = (
    "identity", "scope", "direction", "authority", "mutation", "protection",
    "epistemic_state", "proof", "freshness",
)


@dataclass(frozen=True, slots=True)
class CompletionReceipt:
    """Closure receipt proving that all required execution dimensions are present."""

    execution_id: str
    fields: Mapping[str, str]
    replay_digest: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        missing = [name for name in _REQUIRED_CLOSURE_FIELDS if not self.fields.get(name)]
        if missing:
            raise AssuranceError(f"closure fields missing: {','.join(missing)}")
        if not self.replay_digest or not self.evidence_refs:
            raise AssuranceError("closure requires replay proof and evidence")

    def validate_replay(self, replay: ReplayRecord) -> bool:
        """Bind closure to the exact immutable replay artifact."""
        return replay.execution_id == self.execution_id and replay.trace_digest == self.replay_digest and replay.verify()

    @property
    def closed(self) -> bool:
        return True


@dataclass(frozen=True, slots=True)
class CustodyEnvelope:
    """Hash-linked intent/delegation/tool/result custody record."""

    sequence: int
    kind: str
    payload_digest: str
    previous_digest: str
    digest: str

    @staticmethod
    def build(*, sequence: int, kind: str, payload: Mapping[str, Any], previous_digest: str = "") -> "CustodyEnvelope":
        if sequence < 0 or not kind:
            raise AssuranceError("sequence and kind are required")
        payload_digest = hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()
        material = f"{sequence}|{kind}|{payload_digest}|{previous_digest}"
        digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
        return CustodyEnvelope(sequence, kind, payload_digest, previous_digest, digest)

    def verify(self, previous: "CustodyEnvelope | None" = None) -> bool:
        material = f"{self.sequence}|{self.kind}|{self.payload_digest}|{self.previous_digest}"
        if hashlib.sha256(material.encode("utf-8")).hexdigest() != self.digest:
            return False
        return self.verify_link(previous)

    def verify_link(self, previous: "CustodyEnvelope | None") -> bool:
        if previous is None:
            return self.sequence == 0 and self.previous_digest == ""
        return self.sequence == previous.sequence + 1 and self.previous_digest == previous.digest


@dataclass(frozen=True, slots=True)
class AbstentionDecision:
    """Fail-closed retrieval/decision outcome when evidence is unsafe to use."""

    status: str
    reasons: tuple[str, ...]

    @staticmethod
    def decide(*, evidence_count: int, out_of_scope: bool = False, stale: bool = False, conflict: bool = False) -> "AbstentionDecision":
        reasons: list[str] = []
        if evidence_count < 1:
            reasons.append("INSUFFICIENT_EVIDENCE")
        if out_of_scope:
            reasons.append("OUT_OF_SCOPE")
        if stale:
            reasons.append("STALE_EVIDENCE")
        if conflict:
            reasons.append("UNRESOLVED_CONFLICT")
        return AbstentionDecision("ABSTAIN" if reasons else "PROCEED", tuple(reasons))
