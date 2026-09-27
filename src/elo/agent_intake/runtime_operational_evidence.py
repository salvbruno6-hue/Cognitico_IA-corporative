"""Runtime-generated operational evidence for governed ELO mechanisms.

This module records observations produced by an actual runtime invocation.
It does not authorize implementation, create an Evolution Gate, or promote
canonical state. Evidence is only considered operational when the runtime
supplies an execution identity, observed action, metric result, provenance,
and repeatability/attribution data.

The producer must supply the facts observed by the runtime; this module does
not infer that an execution happened merely because a test or candidate exists.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Mapping
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class RuntimeProvenance:
    commit: str
    runtime_trace: str
    test_run: str | None = None


@dataclass(frozen=True, slots=True)
class RepeatabilityEvidence:
    executions: int
    successful: int
    rate: float

    def __post_init__(self) -> None:
        if self.executions < 1:
            raise ValueError("executions must be >= 1")
        if not 0 <= self.successful <= self.executions:
            raise ValueError("successful must be between 0 and executions")
        expected = self.successful / self.executions
        if abs(self.rate - expected) > 1e-9:
            raise ValueError("repeatability rate does not match executions/successful")


@dataclass(frozen=True, slots=True)
class RuntimeOperationalEvidence:
    execution_id: str
    candidate_id: str
    owner: str
    runtime_entrypoint: str
    timestamp: str
    action_observed: bool
    metric: str
    direction: str
    baseline: float
    observed_value: float
    attribution: str
    provenance: RuntimeProvenance
    regression: bool
    repeatability: RepeatabilityEvidence
    evidence_hash: str

    @property
    def operational_outcome_proven(self) -> bool:
        return (
            bool(self.execution_id)
            and bool(self.candidate_id)
            and bool(self.owner)
            and bool(self.runtime_entrypoint)
            and self.action_observed
            and bool(self.metric)
            and self.attribution == "candidate"
            and ((self.direction == "minimize" and self.observed_value < self.baseline) or (self.direction != "minimize" and self.observed_value > self.baseline))
            and bool(self.provenance.commit)
            and bool(self.provenance.runtime_trace)
            and not self.regression
            and self.repeatability.executions >= 2
            and self.repeatability.successful == self.repeatability.executions
        )

    def to_record(self) -> dict[str, Any]:
        record = asdict(self)
        record["operational_outcome_proven"] = self.operational_outcome_proven
        return record


def create_execution_id(candidate_id: str, *, now: datetime | None = None) -> str:
    """Create an execution identity at the runtime boundary."""
    if not candidate_id:
        raise ValueError("candidate_id is required")
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    return f"exec-{current.strftime('%Y%m%dT%H%M%S%fZ')}-{uuid4().hex[:12]}"


def create_runtime_evidence(
    *,
    execution_id: str,
    candidate_id: str,
    owner: str,
    runtime_entrypoint: str,
    action_observed: bool,
    metric: str,
    direction: str,
    baseline: float,
    observed_value: float,
    attribution: str,
    provenance: RuntimeProvenance,
    regression: bool,
    repeatability: RepeatabilityEvidence,
    timestamp: datetime | None = None,
) -> RuntimeOperationalEvidence:
    """Build evidence from runtime-observed facts; never manufacture action."""
    if not execution_id:
        raise ValueError("execution_id is required")
    if not action_observed:
        raise ValueError("operational evidence requires an observed runtime action")
    if attribution != "candidate":
        raise ValueError("operational evidence requires candidate attribution")
    if not provenance.commit or not provenance.runtime_trace:
        raise ValueError("commit and runtime_trace are required")
    if repeatability.executions < 2:
        raise ValueError("operational evidence requires repeatability across >= 2 executions")

    ts = (timestamp or datetime.now(timezone.utc)).astimezone(timezone.utc)
    payload = "|".join(
        (
            execution_id,
            candidate_id,
            owner,
            runtime_entrypoint,
            ts.isoformat(),
            metric,
            direction,
            str(baseline),
            str(observed_value),
            attribution,
            provenance.commit,
            provenance.runtime_trace,
            provenance.test_run or "",
            str(regression),
            str(repeatability.executions),
            str(repeatability.successful),
        )
    )
    evidence_hash = sha256(payload.encode("utf-8")).hexdigest()

    return RuntimeOperationalEvidence(
        execution_id=execution_id,
        candidate_id=candidate_id,
        owner=owner,
        runtime_entrypoint=runtime_entrypoint,
        timestamp=ts.isoformat(),
        action_observed=action_observed,
        metric=metric,
        direction=direction,
        baseline=baseline,
        observed_value=observed_value,
        attribution=attribution,
        provenance=provenance,
        regression=regression,
        repeatability=repeatability,
        evidence_hash=evidence_hash,
    )


def validate_operational_evidence(
    evidence: RuntimeOperationalEvidence,
) -> tuple[bool, tuple[str, ...]]:
    """Validate provenance and outcome criteria without changing governance state."""
    errors: list[str] = []

    if not evidence.action_observed:
        errors.append("ACTION_NOT_OBSERVED")
    if evidence.attribution != "candidate":
        errors.append("CANDIDATE_ATTRIBUTION_REQUIRED")
    if not evidence.provenance.commit:
        errors.append("COMMIT_PROVENANCE_REQUIRED")
    if not evidence.provenance.runtime_trace:
        errors.append("RUNTIME_TRACE_REQUIRED")
    if evidence.repeatability.executions < 2:
        errors.append("REPEATABILITY_REQUIRED")
    if evidence.repeatability.successful != evidence.repeatability.executions:
        errors.append("REPEATABILITY_NOT_ESTABLISHED")
    if evidence.regression:
        errors.append("REGRESSION_DETECTED")

    return not errors, tuple(errors)


def aggregate_repeatability(
    observations: tuple[RuntimeOperationalEvidence, ...],
) -> RepeatabilityEvidence:
    """Aggregate independent runtime observations for one candidate."""
    if not observations:
        raise ValueError("at least one observation is required")
    executions = len(observations)
    successful = sum(item.operational_outcome_proven for item in observations)
    return RepeatabilityEvidence(
        executions=executions,
        successful=successful,
        rate=successful / executions,
    )


__all__ = [
    "RepeatabilityEvidence",
    "RuntimeOperationalEvidence",
    "RuntimeProvenance",
    "aggregate_repeatability",
    "create_execution_id",
    "create_runtime_evidence",
    "validate_operational_evidence",
]
