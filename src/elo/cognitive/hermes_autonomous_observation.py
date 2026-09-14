"""Governed boundary for Hermes autonomous-agent observations.

Autonomy is treated as an execution capability and source of experience, not
as an ELO authority. The adapter captures intent, bounded actions, outcomes
and evidence, then routes the result through the existing Symbiont intake.
No action is executed here and no canonical state is mutated.
"""
from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.symbiont_pattern_intake import (
    ExternalPatternInput,
    PatternIntakeDecision,
    SymbiontPatternIntake,
)


@dataclass(frozen=True)
class HermesAutonomousObservation:
    """Evidence-bearing record of one bounded autonomous execution."""

    observation_id: str
    tenant_id: str
    agent_skill: str
    source_ref: str
    source_commit: str
    objective: str
    planned_actions: tuple[str, ...]
    observed_outcome: str
    evidence_ids: tuple[str, ...]
    constraints: tuple[str, ...]
    limitations: tuple[str, ...]
    risk: str = "LOW"

    def __post_init__(self) -> None:
        for value, name in (
            (self.observation_id, "observation_id"),
            (self.tenant_id, "tenant_id"),
            (self.agent_skill, "agent_skill"),
            (self.source_ref, "source_ref"),
            (self.source_commit, "source_commit"),
            (self.objective, "objective"),
            (self.observed_outcome, "observed_outcome"),
        ):
            if not value.strip():
                raise ValueError(f"{name} is required")
        if not self.planned_actions:
            raise ValueError("autonomous observation requires bounded planned actions")
        if not self.evidence_ids:
            raise ValueError("autonomous observation requires evidence")
        if not self.constraints:
            raise ValueError("autonomous observation requires execution constraints")
        if not self.limitations:
            raise ValueError("autonomous observation requires limitations")
        if self.risk not in {"LOW", "MEDIUM", "HIGH"}:
            raise ValueError("risk must be LOW, MEDIUM or HIGH")

    def to_external_pattern(self) -> ExternalPatternInput:
        return ExternalPatternInput(
            pattern_id=self.observation_id,
            tenant_id=self.tenant_id,
            domain="autonomous-ai-agents",
            source_ref=self.source_ref,
            source_commit=self.source_commit,
            problem=self.objective,
            mechanism=(
                f"Hermes {self.agent_skill} executed a bounded plan: "
                + "; ".join(self.planned_actions)
                + f"; outcome={self.observed_outcome}"
            ),
            evidence_ids=self.evidence_ids,
            scope="symbiont-hermes-autonomous-agents",
            source_kind="hermes_autonomous_agent",
            risk=self.risk,
        )


class HermesAutonomousIntake:
    """Classify autonomous-agent experience through the canonical ELO gate."""

    def __init__(self, intake: SymbiontPatternIntake | None = None) -> None:
        self.intake = intake or SymbiontPatternIntake()

    def classify(self, observation: HermesAutonomousObservation) -> PatternIntakeDecision:
        return self.intake.classify(observation.to_external_pattern())
