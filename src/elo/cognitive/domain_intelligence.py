"""Native ELO domain-intelligence capability.

The capability is provider-neutral: it models evidence, uncertainty and
limitations without requiring Hermes or any other acquisition provider.
External providers may supply observations, but they are not part of this
contract and never become its authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from elo.cognitive.symbiont_pattern_intake import (
    ExternalPatternInput,
    PatternIntakeDecision,
    SymbiontPatternIntake,
)


@dataclass(frozen=True)
class DomainIntelligenceObservation:
    observation_id: str
    tenant_id: str
    target: str
    source_ref: str
    source_commit: str
    evidence_ids: tuple[str, ...]
    observations: tuple[str, ...]
    limitations: tuple[str, ...]
    confidence: str = "UNKNOWN"
    risk: str = "LOW"
    metadata: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        for value, name in (
            (self.observation_id, "observation_id"),
            (self.tenant_id, "tenant_id"),
            (self.target, "target"),
            (self.source_ref, "source_ref"),
            (self.source_commit, "source_commit"),
        ):
            if not value.strip():
                raise ValueError(f"{name} is required")
        if not self.evidence_ids:
            raise ValueError("domain intelligence requires evidence")
        if not self.observations:
            raise ValueError("domain intelligence requires observations")
        if not self.limitations:
            raise ValueError("domain intelligence requires limitations")
        if self.confidence not in {"HIGH", "MEDIUM", "LOW", "UNKNOWN"}:
            raise ValueError("confidence must be HIGH, MEDIUM, LOW or UNKNOWN")
        if self.risk not in {"LOW", "MEDIUM", "HIGH"}:
            raise ValueError("risk must be LOW, MEDIUM or HIGH")
        forbidden = {"api_key", "authorization", "token", "service_role_key", "private_key"}
        if any(key.lower() in forbidden for key in (self.metadata or {})):
            raise ValueError("domain intelligence metadata cannot contain credentials or secrets")

    def to_pattern(self) -> ExternalPatternInput:
        return ExternalPatternInput(
            pattern_id=self.observation_id,
            tenant_id=self.tenant_id,
            domain="domain-intelligence",
            source_ref=self.source_ref,
            source_commit=self.source_commit,
            problem=f"passive intelligence for {self.target}",
            mechanism=(
                f"evidence-bearing domain observations ({self.confidence} confidence): "
                + "; ".join(self.observations)
            ),
            evidence_ids=self.evidence_ids,
            scope="elo-domain-intelligence",
            source_kind="external_evidence",
            risk=self.risk,
        )


class DomainIntelligence:
    """Native ELO reasoning boundary for domain intelligence."""

    def __init__(self, intake: SymbiontPatternIntake | None = None) -> None:
        self.intake = intake or SymbiontPatternIntake()

    def classify(self, observation: DomainIntelligenceObservation) -> PatternIntakeDecision:
        return self.intake.classify(observation.to_pattern())
