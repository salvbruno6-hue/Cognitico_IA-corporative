"""Orchestrator for post-budget competitiveness analysis.

The analyzer is deliberately non-mutating: it ranks and describes opportunities;
arbitration remains outside the component.
"""

from typing import Any, Dict, Iterable, List

from .abc import analyze_abc
from .models import BudgetItem


class BudgetCompetitivenessAnalyzer:
    """Run the economic prioritization stage without changing canonical state."""

    def __init__(self, class_a_limit: float = 0.80, class_b_limit: float = 0.95) -> None:
        self.class_a_limit = class_a_limit
        self.class_b_limit = class_b_limit

    def analyze(self, items: Iterable[BudgetItem]) -> Dict[str, Any]:
        rows = analyze_abc(
            list(items),
            class_a_limit=self.class_a_limit,
            class_b_limit=self.class_b_limit,
        )
        return {
            "abc": rows,
            "priority_items": [row for row in rows if row["abc_class"] == "A"],
            "authority": "analysis_only",
            "canonical_mutation": False,
            "decision_status": "AGUARDANDO_ARBITRAGEM",
        }
