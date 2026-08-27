from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet


@dataclass(frozen=True, slots=True)
class RoutingRequest:
    """Normalized request signals used to select a cognitive path."""

    task: str
    complexity: float = 0.5
    risk: float = 0.0
    uncertainty: float = 0.5
    deterministic: bool = False
    needs_retrieval: bool = False
    available_capabilities: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        for name, value in (
            ("complexity", self.complexity),
            ("risk", self.risk),
            ("uncertainty", self.uncertainty),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class CognitiveRoute:
    capability: str
    reasoning_depth: int
    verification_required: bool
    rationale: tuple[str, ...]


class CognitiveRouter:
    """Deterministic first-stage router.

    This is intentionally provider-agnostic. A later implementation can replace
    the scoring policy with learned routing while preserving this contract.
    """

    def route(self, request: RoutingRequest) -> CognitiveRoute:
        if request.deterministic:
            return CognitiveRoute(
                capability="deterministic",
                reasoning_depth=0,
                verification_required=request.risk >= 0.5,
                rationale=("deterministic task",),
            )

        if request.needs_retrieval:
            capability = "retrieval_reasoning"
            rationale = ["retrieval requested"]
        elif request.complexity >= 0.8 or request.risk >= 0.8:
            capability = "deliberative_search"
            rationale = ["high complexity or risk"]
        elif request.complexity >= 0.55 or request.uncertainty >= 0.7:
            capability = "multi_step_reasoning"
            rationale = ["moderate complexity or high uncertainty"]
        else:
            capability = "direct_reasoning"
            rationale = ["simple path is sufficient"]

        if request.available_capabilities and capability not in request.available_capabilities:
            capability = "direct_reasoning"
            rationale.append("selected path unavailable; safe fallback")

        depth = 1
        if request.complexity >= 0.55:
            depth = 2
        if request.complexity >= 0.8 or request.risk >= 0.8:
            depth = 3

        verification = request.risk >= 0.5 or request.uncertainty >= 0.7
        return CognitiveRoute(
            capability=capability,
            reasoning_depth=depth,
            verification_required=verification,
            rationale=tuple(rationale),
        )
