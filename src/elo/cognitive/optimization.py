from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvaluationRecord:
    capability: str
    score: float
    latency_ms: float
    evidence_count: int


@dataclass(frozen=True, slots=True)
class ImprovementProposal:
    capability: str
    baseline_score: float
    candidate_score: float
    score_delta: float
    latency_delta_ms: float
    evidence: tuple[str, ...]
    promotion_eligible: bool


class CognitiveOptimizer:
    """Evidence-first optimizer; it proposes changes but never mutates the Canon."""

    def propose(self, baseline: EvaluationRecord, candidate: EvaluationRecord, *, minimum_gain: float = 0.01, max_latency_regression_ms: float = 0.0) -> ImprovementProposal:
        if not 0.0 <= baseline.score <= 1.0 or not 0.0 <= candidate.score <= 1.0:
            raise ValueError("scores must be between 0 and 1")
        delta = candidate.score - baseline.score
        latency_delta = candidate.latency_ms - baseline.latency_ms
        eligible = delta >= minimum_gain and latency_delta <= max_latency_regression_ms
        evidence = (
            f"score delta={delta:.4f}",
            f"latency delta_ms={latency_delta:.2f}",
            f"baseline evidence={baseline.evidence_count}",
            f"candidate evidence={candidate.evidence_count}",
        )
        return ImprovementProposal(baseline.capability, baseline.score, candidate.score, delta, latency_delta, evidence, eligible)
