"""Controlled task-quality validation for the Hermes tool-search candidate.

This module evaluates a supplied baseline/adapted selection trace. It does not
invoke Hermes, execute tools, mutate canonical ELO state, or grant promotion.
The existing ELO Model/Tool Routing owner remains authoritative.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True, slots=True)
class ToolSearchQualityCase:
    case_id: str
    expected_tool: str
    baseline_selected: str
    adapted_selected: str
    adapted_reachable: bool = True


@dataclass(frozen=True, slots=True)
class ToolSearchQualityResult:
    case_count: int
    baseline_accuracy: float
    adapted_accuracy: float
    accuracy_delta: float
    unreachable_cases: tuple[str, ...]
    regressions: tuple[str, ...]
    task_quality_equivalent: bool
    candidate_id: str = "EXT-TOOL-SEARCH-HERMES"
    candidate_only: bool = True
    canonical_mutation: bool = False


def _accuracy(values: Iterable[bool]) -> float:
    results = tuple(values)
    return sum(results) / len(results) if results else 0.0


def evaluate_task_quality(
    cases: Iterable[ToolSearchQualityCase],
) -> ToolSearchQualityResult:
    """Compare adapted tool selection with the baseline on controlled cases.

    Equivalence means adapted selection is at least as accurate as baseline,
    introduces no unreachable expected selection, and introduces no per-case
    regression. This is a quality-equivalence test, not a production benchmark.
    """
    items = tuple(cases)
    if not items:
        raise ValueError("cases must not be empty")

    baseline_hits = tuple(c.baseline_selected == c.expected_tool for c in items)
    adapted_hits = tuple(c.adapted_selected == c.expected_tool for c in items)

    regressions = tuple(
        c.case_id
        for c, baseline_hit, adapted_hit in zip(items, baseline_hits, adapted_hits)
        if baseline_hit and not adapted_hit
    )
    unreachable = tuple(c.case_id for c in items if not c.adapted_reachable)

    baseline_accuracy = _accuracy(baseline_hits)
    adapted_accuracy = _accuracy(adapted_hits)
    equivalent = (
        adapted_accuracy >= baseline_accuracy
        and not regressions
        and not unreachable
    )

    return ToolSearchQualityResult(
        case_count=len(items),
        baseline_accuracy=baseline_accuracy,
        adapted_accuracy=adapted_accuracy,
        accuracy_delta=adapted_accuracy - baseline_accuracy,
        unreachable_cases=unreachable,
        regressions=regressions,
        task_quality_equivalent=equivalent,
    )


def result_as_metrics(
    result: ToolSearchQualityResult,
) -> Mapping[str, float]:
    """Expose only quality metrics for the existing candidate measurement loop."""
    return {
        "selection_accuracy": result.adapted_accuracy,
        "baseline_selection_accuracy": result.baseline_accuracy,
        "accuracy_delta": result.accuracy_delta,
    }


__all__ = [
    "ToolSearchQualityCase",
    "ToolSearchQualityResult",
    "evaluate_task_quality",
    "result_as_metrics",
]
