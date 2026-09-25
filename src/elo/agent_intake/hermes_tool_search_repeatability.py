"""Bounded repeatability validation for the Hermes tool-search candidate.

Reuses the existing task-quality and footprint measurement contracts. It performs
no Hermes execution, tool invocation, canonical-memory mutation, or promotion.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .hermes_tool_search_measurement import measure_footprint
from .hermes_tool_search_quality import ToolSearchQualityResult


@dataclass(frozen=True, slots=True)
class ToolSearchRepeatabilityResult:
    run_count: int
    expected_run_count: int
    stable_quality_metrics: bool
    all_runs_quality_equivalent: bool
    footprint_reduction_ratio: float
    footprint_repeatable: bool
    repeatable: bool
    result: str
    candidate_id: str = "EXT-TOOL-SEARCH-HERMES"
    candidate_only: bool = True
    canonical_mutation: bool = False


def _footprint_ratio() -> float:
    result = measure_footprint(
        eager_schemas=("A" * 100, "B" * 100, "C" * 100),
        deferred_schemas=("A" * 10, "B" * 10),
        selected_tool_schema="C" * 10,
    )
    return result.reduction_ratio


def evaluate_repeatability(
    results: Iterable[ToolSearchQualityResult],
    *,
    expected_run_count: int = 3,
) -> ToolSearchRepeatabilityResult:
    """Validate stable quality plus repeatable measured footprint reduction."""
    if expected_run_count < 2:
        raise ValueError("expected_run_count must be at least 2")

    items = tuple(results)
    if len(items) < expected_run_count:
        raise ValueError(f"at least {expected_run_count} results are required")

    baseline = (
        items[0].baseline_accuracy,
        items[0].adapted_accuracy,
        items[0].accuracy_delta,
        items[0].regressions,
        items[0].unreachable_cases,
    )
    stable_quality = all(
        (
            item.baseline_accuracy,
            item.adapted_accuracy,
            item.accuracy_delta,
            item.regressions,
            item.unreachable_cases,
        ) == baseline
        for item in items
    )
    equivalent = all(item.task_quality_equivalent for item in items)

    footprint_runs = tuple(_footprint_ratio() for _ in items)
    footprint_repeatable = len(set(footprint_runs)) == 1
    footprint_reduction = footprint_runs[0]
    repeatable = stable_quality and equivalent and footprint_repeatable
    result = (
        "EVOLUTION_GATE_REQUIRED"
        if repeatable and footprint_reduction > 0
        else "RETEST"
    )

    return ToolSearchRepeatabilityResult(
        run_count=len(items),
        expected_run_count=expected_run_count,
        stable_quality_metrics=stable_quality,
        all_runs_quality_equivalent=equivalent,
        footprint_reduction_ratio=footprint_reduction,
        footprint_repeatable=footprint_repeatable,
        repeatable=repeatable,
        result=result,
    )


__all__ = ["ToolSearchRepeatabilityResult", "evaluate_repeatability"]
