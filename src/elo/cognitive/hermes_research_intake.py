"""Governed adaptation boundary for Hermes Research capabilities.

Hermes research skills are evidence producers, not ELO authorities. This adapter
normalizes a completed research observation into the existing Symbiont pattern
intake so the canonical Evolution Gate remains responsible for classification.
No network access, persistence, promotion, or credentials are performed here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from elo.cognitive.symbiont_pattern_intake import (
    ExternalPatternInput,
    PatternIntakeDecision,
    SymbiontPatternIntake,
)


@dataclass(frozen=True)
class HermesResearchObservation:
    """Evidence-bearing result produced by an authorized Hermes research run."""

    observation_id: str
    tenant_id: str
    skill: str
    domain: str
    source_ref: str
    source_commit: str
    evidence_ids: tuple[str, ...]
    question: str
    findings: tuple[str, ...]
    limitations: tuple[str, ...]
    source_kind: str = "hermes_skill"
    risk: str = "LOW"
    metadata: Mapping[str, Any] = None

    def __post_init__(self) -> None:
        required = (
            (self.observation_id, "observation_id"),
            (self.tenant_id, "tenant_id"),
            (self.skill, "skill"),
            (self.domain, "domain"),
            (self.source_ref, "source_ref"),
            (self.source_commit, "source_commit"),
            (self.question, "question"),
        )
        for value, name in required:
            if not value or not value.strip():
                raise ValueError(f"{name} is required")
        if not self.evidence_ids:
            raise ValueError("research observation requires evidence")
        if not self.findings:
            raise ValueError("research observation requires findings")
        if not self.limitations:
            raise ValueError("research observation requires limitations")
        if self.metadata is None:
            object.__setattr__(self, "metadata", {})
        forbidden = {"api_key", "authorization", "token", "service_role_key", "private_key"}
        if any(str(key).lower() in forbidden for key in self.metadata):
            raise ValueError("research metadata cannot contain credentials or secrets")

    def to_external_pattern(self) -> ExternalPatternInput:
        """Translate research evidence into the existing canonical intake envelope."""
        return ExternalPatternInput(
            pattern_id=self.observation_id,
            tenant_id=self.tenant_id,
            domain=self.domain,
            source_ref=self.source_ref,
            source_commit=self.source_commit,
            problem=self.question,
            mechanism=(
                f"Hermes skill {self.skill} produced evidence-backed findings; "
                "adaptation remains candidate-only"
            ),
            evidence_ids=self.evidence_ids,
            scope="symbiont-hermes-research",
            source_kind=self.source_kind,
            risk=self.risk,
        )


class HermesResearchIntake:
    """Attach Hermes research observations to the existing ELO evolution spine."""

    def __init__(self, intake: SymbiontPatternIntake | None = None) -> None:
        self.intake = intake or SymbiontPatternIntake()

    def classify(self, observation: HermesResearchObservation) -> PatternIntakeDecision:
        return self.intake.classify(observation.to_external_pattern())
