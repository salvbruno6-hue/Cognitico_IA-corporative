from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Sequence, TypeVar

T = TypeVar("T")
P = TypeVar("P")


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    score: float
    samples: int
    failures: int


class Evaluator:
    """Minimal metric-driven evaluation harness.

    It intentionally mirrors the useful architectural idea of metric-driven
    optimization without coupling ELO to an external framework.
    """

    def evaluate(
        self,
        examples: Sequence[T],
        predict: Callable[[T], P],
        metric: Callable[[T, P], float],
    ) -> EvaluationResult:
        if not examples:
            raise ValueError("evaluation requires at least one example")

        scores: list[float] = []
        failures = 0
        for example in examples:
            try:
                value = float(metric(example, predict(example)))
            except Exception:
                failures += 1
                continue
            if not 0.0 <= value <= 1.0:
                raise ValueError("metric values must be between 0 and 1")
            scores.append(value)

        if not scores:
            return EvaluationResult(score=0.0, samples=len(examples), failures=failures)
        return EvaluationResult(
            score=sum(scores) / len(scores),
            samples=len(examples),
            failures=failures,
        )


def exact_match(expected: str, predicted: str) -> float:
    return 1.0 if expected.strip() == predicted.strip() else 0.0


def groundedness(required: Iterable[str], response: str) -> float:
    """Simple deterministic baseline for claim-support experiments."""
    claims = [item.strip().lower() for item in required if item.strip()]
    if not claims:
        return 1.0
    text = response.lower()
    return sum(claim in text for claim in claims) / len(claims)
