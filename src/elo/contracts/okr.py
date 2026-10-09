"""Strategic OKR contracts consumed by the canonical ELO orchestrator.

Layer: cognitive
Owner: strategic-objective-domain
Status: implemented
Authority: contract
Related: GovernedOrchestrator, CapabilityRegistry, EvidenceRepository, KPI registry

These value objects do not orchestrate, route, authorize, execute, learn, or
persist.  They represent the minimum strategic state the existing ELO
orchestrator needs to query and correlate an Objective/Key Result chain.

KPI authority remains outside this module: ``metric_code`` references the
existing formal KPI registry (``mt_definicoes_kpi``). Evidence authority remains
``EvidenceRepository`` and evidence references are identities only.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum


class KeyResultDirection(StrEnum):
    """How movement of a measured value relates to the desired result."""

    INCREASE = "INCREASE"
    DECREASE = "DECREASE"
    MAINTAIN = "MAINTAIN"


class TargetApprovalState(StrEnum):
    """Human-governed target state; a draft target is never silently approved."""

    DRAFT = "DRAFT"
    APPROVED = "APPROVED"


def _required(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} is required")
    return normalized


def _refs(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(item.strip() for item in values if item and item.strip()))


@dataclass(frozen=True, slots=True)
class Objective:
    """Strategic objective exposed to, but not owned by, the orchestrator."""

    tenant_id: str
    objective_id: str
    title: str
    strategy_ref: str | None = None
    owner_ref: str | None = None
    key_result_ids: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "tenant_id", _required(self.tenant_id, "tenant_id"))
        object.__setattr__(self, "objective_id", _required(self.objective_id, "objective_id"))
        object.__setattr__(self, "title", _required(self.title, "title"))
        object.__setattr__(self, "key_result_ids", _refs(self.key_result_ids))
        object.__setattr__(self, "evidence_refs", _refs(self.evidence_refs))


@dataclass(frozen=True, slots=True)
class KeyResult:
    """Measurable result linked to one Objective and one formal metric identity."""

    tenant_id: str
    key_result_id: str
    objective_id: str
    title: str
    metric_code: str
    direction: KeyResultDirection
    baseline: Decimal | None = None
    target: Decimal | None = None
    deadline: date | None = None
    weight: Decimal = Decimal("1")
    baseline_evidence_refs: tuple[str, ...] = ()
    target_evidence_refs: tuple[str, ...] = ()
    target_approval_state: TargetApprovalState = TargetApprovalState.DRAFT
    target_approval_ref: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "tenant_id", _required(self.tenant_id, "tenant_id"))
        object.__setattr__(self, "key_result_id", _required(self.key_result_id, "key_result_id"))
        object.__setattr__(self, "objective_id", _required(self.objective_id, "objective_id"))
        object.__setattr__(self, "title", _required(self.title, "title"))
        object.__setattr__(self, "metric_code", _required(self.metric_code, "metric_code"))
        object.__setattr__(self, "baseline_evidence_refs", _refs(self.baseline_evidence_refs))
        object.__setattr__(self, "target_evidence_refs", _refs(self.target_evidence_refs))
        if self.weight <= 0:
            raise ValueError("weight must be greater than zero")
        if self.baseline is not None and not self.baseline_evidence_refs:
            raise ValueError("baseline requires evidence_refs")
        if self.target is not None and not self.target_evidence_refs:
            raise ValueError("target requires evidence_refs")
        if self.target_approval_state is TargetApprovalState.APPROVED and not (self.target_approval_ref or "").strip():
            raise ValueError("approved target requires target_approval_ref")

    @property
    def approved_target(self) -> Decimal | None:
        """Return a target only when human approval is explicitly represented."""

        if self.target_approval_state is TargetApprovalState.APPROVED:
            return self.target
        return None


@dataclass(frozen=True, slots=True)
class Measurement:
    """Evidence-backed observation for a Key Result metric.

    This is an OKR-domain reference to a measurement, not a competing metric or
    KPI snapshot authority. Persistence/adaptation to ``mt_snapshots_kpi`` is a
    later application/infrastructure concern.
    """

    tenant_id: str
    measurement_id: str
    key_result_id: str
    metric_code: str
    value: Decimal
    measured_at: datetime
    evidence_refs: tuple[str, ...]
    source_ref: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "tenant_id", _required(self.tenant_id, "tenant_id"))
        object.__setattr__(self, "measurement_id", _required(self.measurement_id, "measurement_id"))
        object.__setattr__(self, "key_result_id", _required(self.key_result_id, "key_result_id"))
        object.__setattr__(self, "metric_code", _required(self.metric_code, "metric_code"))
        object.__setattr__(self, "source_ref", _required(self.source_ref, "source_ref"))
        object.__setattr__(self, "evidence_refs", _refs(self.evidence_refs))
        if not self.evidence_refs:
            raise ValueError("measurement requires evidence_refs")
        if self.measured_at.tzinfo is None or self.measured_at.utcoffset() is None:
            raise ValueError("measured_at must be timezone-aware")


__all__ = [
    "KeyResult",
    "KeyResultDirection",
    "Measurement",
    "Objective",
    "TargetApprovalState",
]
