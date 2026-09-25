"""Bounded repeatability validation for the Hermes tool-search candidate.

This module reuses the existing task-quality result. It performs no Hermes
execution, tool invocation, canonical-memory mutation, or promotion.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from elo.agent_intake.hermes_tool_search_quality import ToolSearchQualityResult


@dataclass(frozen=True, slots=True)
class ToolSearchRepeatabilityResult:
    run_count: int
    expected_run_count: int
    stable_metrics: bool
    all_runs_quality_equivalent: bool
    repeatable: bool
    candidate_id: str = "EXT-TOOL-SEARCH-HERMES"
    candidate_only: bool = True
    canonical_mutation: bool = False


def evaluate_repeatability(
    results: Iterable[ToolSearchQualityResult],
    *,
    expected_run_count: int = 3,
) -> ToolSearchRepeatabilityResult:
    """Validate deterministic quality metrics across repeated controlled runs.

    Repeatability requires the requested minimum number of runs, identical
    quality metrics on every run, and quality equivalence on every run.
    """
    if expected_run_count < 2:
        raise ValueError("expected_run_count must be at least 2")

    items = tuple(results)
    if len(items) < expected_run_count:
        raise ValueError(
            f"at least {expected_run_count} results are required"
        )

    baseline = (
        items[0].baseline_accuracy,
        items[0].adapted_accuracy,
        items[0].accuracy_delta,
        items[0].regressions,
        items[0].unreachable_cases,
    )
    stable = all(
        (
            item.baseline_accuracy,
            item.adapted_accuracy,
            item.accuracy_delta,
            item.regressions,
            item.unreachable_cases,
        )
        == baseline
        for item in items
    )
    equivalent = all(item.task_quality_equivalent for item in items)

    return ToolSearchRepeatabilityResult(
        run_count=len(items),
        expected_run_count=expected_run_count,
        stable_metrics=stable,
        all_runs_quality_equivalent=equivalent,
        repeatable=stable and equivalent,
    )


__all__ = ["ToolSearchRepeatabilityResult", "evaluate_repeatability"]
