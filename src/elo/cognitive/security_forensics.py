"""Native ELO security-forensics boundary derived from reusable evidence-first mechanisms."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from elo.cognitive.symbiont_pattern_intake import ExternalPatternInput, PatternIntakeDecision, SymbiontPatternIntake


_FORBIDDEN_KEYS = frozenset({"api_key", "access_token", "authorization", "password", "secret", "service_role_key"})


@dataclass(frozen=True)
class SecurityObservation:
    observation_id: str
    tenant_id: str
    target: str
    source_ref: str
    source_commit: str
    evidence_ids: tuple[str, ...]
    facts: tuple[str, ...]
    hypotheses: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    risk: str = "LOW"
    metadata: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        required = (self.observation_id, self.tenant_id, self.target, self.source_ref, self.source_commit)
        if not all(value.strip() for value in required):
            raise ValueError("security observation requires identity and provenance")
        if not self.evidence_ids:
            raise ValueError("security observation requires evidence")
        if not self.facts:
            raise ValueError("security observation requires facts")
        self._reject_secrets(self.metadata or {}, "metadata")

    @staticmethod
    def _reject_secrets(value: Any, path: str) -> None:
        if isinstance(value, Mapping):
            for key, child in value.items():
                if str(key).lower() in _FORBIDDEN_KEYS:
                    raise ValueError(f"secret field is not allowed: {path}.{key}")
                SecurityObservation._reject_secrets(child, f"{path}.{key}")
        elif isinstance(value, (list, tuple)):
            for index, child in enumerate(value):
                SecurityObservation._reject_secrets(child, f"{path}[{index}]")

    def to_pattern(self) -> ExternalPatternInput:
        return ExternalPatternInput(
            pattern_id=self.observation_id,
            tenant_id=self.tenant_id,
            domain="security-forensics",
            source_ref=self.source_ref,
            source_commit=self.source_commit,
            problem=f"Security investigation of {self.target}",
            mechanism="evidence-first forensic analysis with fact/hypothesis separation",
            evidence_ids=self.evidence_ids,
            scope="elo-security-forensics",
            source_kind="external_evidence",
            risk=self.risk,
        )


class SecurityForensics:
    """Deterministic security observation classifier; it never executes target code."""

    def __init__(self, intake: SymbiontPatternIntake | None = None) -> None:
        self.intake = intake or SymbiontPatternIntake()

    def classify(self, observation: SecurityObservation) -> PatternIntakeDecision:
        return self.intake.classify(observation.to_pattern())
