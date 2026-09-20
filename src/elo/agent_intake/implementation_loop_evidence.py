"""Evidence contract for the governed ELO implementation loop.

The record is immutable and descriptive. It does not promote, deploy, or
mutate canonical ELO state.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ImplementationEvidence:
    candidate_id: str
    owner: str
    baseline: Mapping[str, float]
    adapted: Mapping[str, float]
    metric_directions: Mapping[str, str]
    regressions: tuple[str, ...]
    repeatable: bool
    provenance_refs: tuple[str, ...]
    boundary_integrity: bool
    decision: str = "UNASSESSED"

    def is_complete(self) -> bool:
        """Return whether the minimum evidence package is present and bounded."""
        if not self.candidate_id or not self.owner:
            return False
        if not self.baseline or not self.adapted:
            return False
        common = self.baseline.keys() & self.adapted.keys()
        if not common:
            return False
        if any(self.metric_directions.get(metric) not in {"maximize", "minimize"} for metric in common):
            return False
        if self.regressions or not self.repeatable or not self.provenance_refs:
            return False
        return self.boundary_integrity
