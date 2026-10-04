"""Fail-closed intake for externally observed runtime evidence.

This boundary accepts facts reported by an external runtime and converts them
into the existing RuntimeOperationalEvidence contract. It does not authorize,
execute, persist, promote, or declare production outcomes.

Production proof remains the responsibility of the existing
runtime_operational_evidence_adapter and its canonical authorization/execution
bindings.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeOperationalEvidence,
    RuntimeProvenance,
    create_runtime_evidence,
)


_ALLOWED_ENVIRONMENTS = frozenset({"controlled", "production"})


@dataclass(frozen=True, slots=True)
class ExternalRuntimeObservation:
    """Facts explicitly reported by an external runtime.

    Authorization fields are references only. This class never interprets them
    as permission and never replaces the canonical authorization authority.
    """

    execution_id: str
    candidate_id: str
    owner: str
    runtime_entrypoint: str
    timestamp: datetime
    action_observed: bool
    metric: str
    direction: str
    baseline: float
    observed_value: float
    attribution: str
    runtime_commit: str
    runtime_trace: str
    environment: str
    decision_pattern_candidate_ref: str
    authorization_id: str
    authorization_evidence_ref: str

    def __post_init__(self) -> None:
        required = {
            "execution_id": self.execution_id,
            "candidate_id": self.candidate_id,
            "owner": self.owner,
            "runtime_entrypoint": self.runtime_entrypoint,
            "metric": self.metric,
            "direction": self.direction,
            "runtime_commit": self.runtime_commit,
            "runtime_trace": self.runtime_trace,
            "decision_pattern_candidate_ref": self.decision_pattern_candidate_ref,
            "authorization_id": self.authorization_id,
            "authorization_evidence_ref": self.authorization_evidence_ref,
        }
        missing = tuple(name for name, value in required.items() if not str(value).strip())
        if missing:
            raise ValueError("external runtime observation missing: " + ",".join(missing))
        if self.environment not in _ALLOWED_ENVIRONMENTS:
            raise ValueError(f"unsupported runtime environment: {self.environment}")
        if not self.action_observed:
            raise ValueError("external runtime observation requires action_observed=True")
        if self.attribution != "candidate":
            raise ValueError("external runtime observation requires candidate attribution")
        if self.observed_value == self.baseline:
            raise ValueError("external runtime observation requires a changed metric value")


def ingest_external_runtime_observation(
    observation: ExternalRuntimeObservation,
) -> RuntimeOperationalEvidence:
    """Convert externally observed facts into the existing evidence contract.

    The resulting evidence is still evidence only. In particular, an
    environment=production observation does not by itself establish
    production_proven=True.
    """

    return create_runtime_evidence(
        execution_id=observation.execution_id,
        candidate_id=observation.candidate_id,
        owner=observation.owner,
        runtime_entrypoint=observation.runtime_entrypoint,
        action_observed=observation.action_observed,
        metric=observation.metric,
        direction=observation.direction,
        baseline=observation.baseline,
        observed_value=observation.observed_value,
        attribution=observation.attribution,
        provenance=RuntimeProvenance(
            commit=observation.runtime_commit,
            runtime_trace=observation.runtime_trace,
        ),
        regression=False,
        repeatability=RepeatabilityEvidence(
            executions=1,
            successful=1,
            rate=1.0,
        ),
        timestamp=observation.timestamp,
        decision_pattern_candidate_ref=observation.decision_pattern_candidate_ref,
    )


__all__ = [
    "ExternalRuntimeObservation",
    "ingest_external_runtime_observation",
]
