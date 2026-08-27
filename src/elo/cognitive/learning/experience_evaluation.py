"""Evaluation and learning boundary for execution experiences.

An experience becomes learning evidence only after explicit evaluation. This
module deliberately does not promote anything into the Canon or tenant method.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Experience:
    tenant_id: str
    capability: str
    context: dict[str, Any]
    model_id: str | None
    tool_id: str | None
    result: Any
    verified: bool
    latency_ms: float = 0.0
    cost: float = 0.0


@dataclass(frozen=True)
class ExperienceEvaluation:
    quality: float
    reliability: float
    efficiency: float
    reusable: bool
    rationale: str


class ExperienceEvaluator:
    def evaluate(self, experience: Experience) -> ExperienceEvaluation:
        quality = 1.0 if experience.verified else 0.0
        reliability = quality
        efficiency = 1.0 / (1.0 + max(experience.latency_ms, 0.0) / 1000.0 + max(experience.cost, 0.0))
        reusable = experience.verified and quality >= 1.0
        return ExperienceEvaluation(
            quality=quality,
            reliability=reliability,
            efficiency=efficiency,
            reusable=reusable,
            rationale="verified execution with recorded provenance" if reusable else "execution is not reusable evidence",
        )


class LearningCandidateBuilder:
    def build(self, experience: Experience, evaluation: ExperienceEvaluation) -> dict[str, Any] | None:
        if not evaluation.reusable:
            return None
        return {
            "tenant_id": experience.tenant_id,
            "capability": experience.capability,
            "context": experience.context,
            "model_id": experience.model_id,
            "tool_id": experience.tool_id,
            "quality": evaluation.quality,
            "reliability": evaluation.reliability,
            "efficiency": evaluation.efficiency,
            "source": "verified-experience",
            "promotion_state": "candidate",
        }
