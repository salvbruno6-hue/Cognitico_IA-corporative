from __future__ import annotations

from dataclasses import dataclass

from .context import CognitiveContext
from .routing.router import CognitiveRouter, RoutingRequest
from .verification import CognitiveVerifier, VerificationResult


@dataclass(frozen=True, slots=True)
class CognitivePlan:
    capability: str
    reasoning_depth: int
    verification_required: bool
    rationale: tuple[str, ...]


class CognitiveEngine:
    """Provider-independent orchestration layer for the ELO cognitive loop."""

    def __init__(self, router: CognitiveRouter | None = None, verifier: CognitiveVerifier | None = None) -> None:
        self.router = router or CognitiveRouter()
        self.verifier = verifier or CognitiveVerifier()

    def plan(self, context: CognitiveContext, *, complexity: float = 0.5, risk: float = 0.0, uncertainty: float = 0.5, deterministic: bool = False, needs_retrieval: bool = False, available_capabilities: frozenset[str] = frozenset()) -> CognitivePlan:
        route = self.router.route(
            RoutingRequest(
                task=context.task,
                complexity=complexity,
                risk=risk,
                uncertainty=uncertainty,
                deterministic=deterministic,
                needs_retrieval=needs_retrieval,
                available_capabilities=available_capabilities,
            )
        )
        return CognitivePlan(route.capability, route.reasoning_depth, route.verification_required, route.rationale)

    def verify(self, answer: str, context: CognitiveContext, *, required_confidence: float = 0.7, contradiction: bool = False) -> VerificationResult:
        confidences = tuple(item.confidence for item in context.evidence)
        return self.verifier.verify(
            answer=answer,
            evidence_confidences=confidences,
            contradiction=contradiction,
            required_confidence=required_confidence,
        )
