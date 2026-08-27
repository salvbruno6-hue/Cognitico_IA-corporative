from __future__ import annotations

from dataclasses import dataclass

from .router import CognitiveRoute, CognitiveRouter, RoutingRequest


@dataclass(frozen=True, slots=True)
class RoutingExperience:
    capability: str
    score: float
    latency_ms: float
    success: bool


class AdaptiveCognitiveRouter(CognitiveRouter):
    """Experience-aware router that learns only from explicit, bounded feedback."""

    def __init__(self) -> None:
        self._experiences: dict[str, list[RoutingExperience]] = {}

    def record(self, experience: RoutingExperience) -> None:
        if not 0.0 <= experience.score <= 1.0:
            raise ValueError("score must be between 0 and 1")
        if experience.latency_ms < 0:
            raise ValueError("latency_ms cannot be negative")
        self._experiences.setdefault(experience.capability, []).append(experience)

    def route(self, request: RoutingRequest) -> CognitiveRoute:
        baseline = super().route(request)
        candidates = [baseline.capability]
        candidates.extend(sorted(self._experiences))
        if request.available_capabilities:
            candidates = [name for name in candidates if name in request.available_capabilities]
        if not candidates:
            return baseline

        def utility(capability: str) -> float:
            samples = self._experiences.get(capability, [])
            if not samples:
                return 0.0
            avg_score = sum(x.score for x in samples) / len(samples)
            success = sum(1 for x in samples if x.success) / len(samples)
            avg_latency = sum(x.latency_ms for x in samples) / len(samples)
            latency_penalty = min(0.25, avg_latency / 10000.0)
            return 0.65 * avg_score + 0.35 * success - latency_penalty

        best = max(candidates, key=lambda name: (utility(name), name == baseline.capability))
        if best == baseline.capability:
            return baseline
        return CognitiveRoute(
            capability=best,
            reasoning_depth=baseline.reasoning_depth,
            verification_required=baseline.verification_required,
            rationale=baseline.rationale + ("experience-aware route",),
        )

    def experience_count(self, capability: str) -> int:
        return len(self._experiences.get(capability, []))
