"""Native ELO bounded autonomous reasoning capability.

This module owns planning/validation of bounded autonomous work. It does not
execute tools and has no dependency on an external agent provider. Providers
can be plugged into the execution boundary later without becoming owners of
ELO reasoning or governance.
"""
from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.symbiont_pattern_intake import (
    ExternalPatternInput,
    PatternIntakeDecision,
    SymbiontPatternIntake,
)


@dataclass(frozen=True)
class AutonomousExecutionPlan:
    plan_id: str
    tenant_id: str
    objective: str
    planned_actions: tuple[str, ...]
    constraints: tuple[str, ...]
    expected_outcome: str
    evidence_ids: tuple[str, ...]
    limitations: tuple[str, ...]
    source_ref: str
    source_commit: str
    risk: str = "LOW"

    def __post_init__(self) -> None:
        for value, name in (
            (self.plan_id, "plan_id"),
            (self.tenant_id, "tenant_id"),
            (self.objective, "objective"),
            (self.expected_outcome, "expected_outcome"),
            (self.source_ref, "source_ref"),
            (self.source_commit, "source_commit"),
        ):
            if not value.strip():
                raise ValueError(f"{name} is required")
        if not self.planned_actions:
            raise ValueError("autonomous plan requires bounded planned actions")
        if not self.constraints:
            raise ValueError("autonomous plan requires execution constraints")
        if not self.evidence_ids:
            raise ValueError("autonomous plan requires evidence")
        if not self.limitations:
            raise ValueError("autonomous plan requires limitations")
        if self.risk not in {"LOW", "MEDIUM", "HIGH"}:
            raise ValueError("risk must be LOW, MEDIUM or HIGH")

    def to_pattern(self, observed_outcome: str) -> ExternalPatternInput:
        if not observed_outcome.strip():
            raise ValueError("observed_outcome is required")
        return ExternalPatternInput(
            pattern_id=self.plan_id,
            tenant_id=self.tenant_id,
            domain="autonomous-reasoning",
            source_ref=self.source_ref,
            source_commit=self.source_commit,
            problem=self.objective,
            mechanism=(
                "bounded planning with explicit constraints: "
                + "; ".join(self.planned_actions)
                + f"; expected={self.expected_outcome}; observed={observed_outcome}"
            ),
            evidence_ids=self.evidence_ids,
            scope="elo-autonomous-reasoning",
            source_kind="external_evidence",
            risk=self.risk,
        )


class AutonomousReasoning:
    """Native ELO planning boundary and Evolution Gate adapter."""

    def __init__(self, intake: SymbiontPatternIntake | None = None) -> None:
        self.intake = intake or SymbiontPatternIntake()

    def classify(
        self, plan: AutonomousExecutionPlan, observed_outcome: str
    ) -> PatternIntakeDecision:
        return self.intake.classify(plan.to_pattern(observed_outcome))
