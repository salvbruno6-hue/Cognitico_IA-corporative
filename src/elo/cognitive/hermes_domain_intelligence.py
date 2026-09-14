"""Governed adapter for Hermes passive domain-intelligence observations.

The adapter turns an authorized, evidence-bearing Hermes observation into a
canonical ELO domain-intelligence candidate without granting Hermes authority.
It deliberately does not perform DNS/WHOIS/network access or persist facts.
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
    """Structured passive-domain observation with explicit uncertainty."""

    observation_id: str
    tenant_id: str
    target: str
    source_ref: str
    source_commit: str
    evidence_ids: tuple[str, ...]
    observations: tuple[str, ...]
    limitations: tuple[str, ...]
    confidence: str = "UNKNOWN"
    source_kind: str = "hermes_domain_intel"
    risk: str = "LOW"
    metadata: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        required = (
            (self.observation_id, "observation_id"),
            (self.tenant_id, "tenant_id"),
            (self.target, "target"),
            (self.source_ref, "source_ref"),
            (self.source_commit, "source_commit"),
        )
        for value, name in required:
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
        forbidden = {"api_key", "authorization", "token", "service_role_key", "private_key"}
        if any(key.lower() in forbidden for key in (self.metadata or {})):
            raise ValueError("domain intelligence metadata cannot contain credentials or secrets")

    def to_external_pattern(self) -> ExternalPatternInput:
        return ExternalPatternInput(
            pattern_id=self.observation_id,
            tenant_id=self.tenant_id,
            domain="domain-intelligence",
            source_ref=self.source_ref,
            source_commit=self.source_commit,
            problem=f"passive intelligence for {self.target}",
            mechanism=(
                f"Hermes domain-intel observations ({self.confidence} confidence): "
                + "; ".join(self.observations)
            ),
            evidence_ids=self.evidence_ids,
            scope="symbiont-hermes-domain-intelligence",
            source_kind=self.source_kind,
            risk=self.risk,
        )


class HermesDomainIntelligence:
    """Connect domain intelligence to the existing Evolution Gate spine."""

    def __init__(self, intake: SymbiontPatternIntake | None = None) -> None:
        self.intake = intake or SymbiontPatternIntake()

    def classify(self, observation: DomainIntelligenceObservation) -> PatternIntakeDecision:
        return self.intake.classify(observation.to_external_pattern())
