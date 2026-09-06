"""Deterministic financial ABC classification for budget analysis."""

from typing import Iterable, List, Sequence, Tuple

from .models import BudgetItem


def calculate_weights(items: Iterable[BudgetItem]) -> List[Tuple[BudgetItem, float, float]]:
    """Return items sorted by value with individual and accumulated weights."""
    ordered = sorted(items, key=lambda item: item.total_value, reverse=True)
    total = sum(item.total_value for item in ordered)
    if total <= 0:
        raise ValueError("budget total must be positive")

    accumulated = 0.0
    result = []
    for item in ordered:
        weight = item.total_value / total
        accumulated += weight
        result.append((item, weight, accumulated))
    return result


def classify_abc(
    accumulated_weight: float,
    class_a_limit: float = 0.80,
    class_b_limit: float = 0.95,
) -> str:
    """Classify an item using configurable cumulative thresholds."""
    if not 0 < class_a_limit < class_b_limit <= 1:
        raise ValueError("thresholds must satisfy 0 < A < B <= 1")
    if accumulated_weight <= class_a_limit:
        return "A"
    if accumulated_weight <= class_b_limit:
        return "B"
    return "C"


def analyze_abc(
    items: Sequence[BudgetItem],
    class_a_limit: float = 0.80,
    class_b_limit: float = 0.95,
) -> List[dict]:
    """Produce a pure, non-mutating ABC analysis."""
    rows = []
    for item, weight, accumulated in calculate_weights(items):
        rows.append(
            {
                "item_id": item.item_id,
                "total_value": item.total_value,
                "financial_weight": weight,
                "accumulated_weight": accumulated,
                "abc_class": classify_abc(accumulated, class_a_limit, class_b_limit),
            }
        )
    return rows
