"""Evidence-based maturity state for ELO/GPT collaboration."""

from dataclasses import dataclass


MATURITY_DIMENSIONS = (
    "enterprise_context",
    "end_to_end_process",
    "systemic_reasoning",
    "evidence_analysis",
    "decision_memory",
    "uncertainty_management",
    "outcome_feedback",
)


@dataclass(frozen=True)
class MaturityAssessment:
    scores: dict[str, float]
    minimum_threshold: float = 0.75

    def __post_init__(self) -> None:
        unknown = set(self.scores) - set(MATURITY_DIMENSIONS)
        if unknown:
            raise ValueError(f"unknown maturity dimensions: {sorted(unknown)}")
        if not 0.0 <= self.minimum_threshold <= 1.0:
            raise ValueError("minimum_threshold must be between 0 and 1")
        if any(not 0.0 <= value <= 1.0 for value in self.scores.values()):
            raise ValueError("maturity scores must be between 0 and 1")

    @property
    def is_mature_for_specialist_mode(self) -> bool:
        return all(self.scores.get(dimension, 0.0) >= self.minimum_threshold for dimension in MATURITY_DIMENSIONS)

    @property
    def mode(self) -> str:
        return "SPECIALIST_VALIDATION" if self.is_mature_for_specialist_mode else "DISCOVERY_ASSIST"
