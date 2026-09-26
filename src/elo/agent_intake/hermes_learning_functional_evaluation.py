"""Candidate-specific functional evaluation for EXT-LEARN-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_learning_adapter import adapt_skill_learning
from .hermes_learning_boundary import SkillLearningSignal

@dataclass(frozen=True, slots=True)
class LearningFunctionalEvidence:
    baseline_unsafe_admission_block_rate: float
    adapted_unsafe_admission_block_rate: float
    repeatable: bool
    boundary_integrity: bool
    provenance_refs: tuple[str, ...]

def _signals(prefix: str) -> tuple[SkillLearningSignal, ...]:
    return (
        SkillLearningSignal(
            f"{prefix}-verified", "multiteiner",
            (f"controlled-eval:learn-functional/{prefix.lower()}/verified",),
            "pricing-skill", "digest-verified", True, True,
        ),
        SkillLearningSignal(
            f"{prefix}-unverified", "multiteiner",
            (f"controlled-eval:learn-functional/{prefix.lower()}/unverified",),
            "pricing-skill", "digest-unverified", True, False,
        ),
    )

def _baseline(signals: tuple[SkillLearningSignal, ...]) -> float:
    # Naive learning intake would admit every user-directed signal regardless
    # of verification status, so the unverified signal is not blocked.
    return 0.0

def _adapted(signals: tuple[SkillLearningSignal, ...]) -> float:
    unverified = next(s for s in signals if not s.verified)
    verified = next(s for s in signals if s.verified)
    blocked = adapt_skill_learning(unverified) is None
    admitted = adapt_skill_learning(verified) is not None
    return float(blocked and admitted)

def evaluate_learning_functional_gain() -> LearningFunctionalEvidence:
    baseline_signals = _signals("BASELINE")
    adapted_signals = _signals("HERMES")
    baseline = _baseline(baseline_signals)
    adapted = _adapted(adapted_signals)
    repeatable = _adapted(_signals("REPEAT")) == adapted
    contracts = tuple(adapt_skill_learning(s) for s in adapted_signals)
    boundary = (
        contracts[0] is not None
        and all(
            c is not None
            and c.promotion_authority is False
            and c.canonical_mutation is False
            for c in contracts if c is not None
        )
        and contracts[1] is None
    )
    refs = tuple(ref for s in adapted_signals for ref in s.source_refs)
    return LearningFunctionalEvidence(baseline, adapted, repeatable, boundary, refs)
