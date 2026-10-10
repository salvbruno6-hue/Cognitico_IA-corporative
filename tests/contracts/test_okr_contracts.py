from datetime import date, datetime, timezone
from decimal import Decimal

import pytest

from elo.contracts.okr import (
    KeyResult,
    KeyResultDirection,
    Measurement,
    Objective,
    TargetApprovalState,
)


def test_objective_is_tenant_scoped_and_deduplicates_refs():
    objective = Objective(
        tenant_id="tenant-a",
        objective_id="OBJ-1",
        title="Improve delivery reliability",
        strategy_ref="STRATEGY-1",
        key_result_ids=("KR-1", "KR-1", "KR-2"),
        evidence_refs=("ev-1", "ev-1"),
    )

    assert objective.tenant_id == "tenant-a"
    assert objective.key_result_ids == ("KR-1", "KR-2")
    assert objective.evidence_refs == ("ev-1",)


def test_key_result_references_existing_metric_identity_without_defining_kpi():
    kr = KeyResult(
        tenant_id="tenant-a",
        key_result_id="KR-1",
        objective_id="OBJ-1",
        title="Reduce production lead time",
        metric_code="KPI-LEAD-TIME",
        direction=KeyResultDirection.DECREASE,
        baseline=Decimal("15"),
        target=Decimal("10"),
        deadline=date(2026, 12, 31),
        baseline_evidence_refs=("ev-baseline",),
        target_evidence_refs=("ev-target",),
        target_approval_state=TargetApprovalState.APPROVED,
        target_approval_ref="approval:human:42",
    )

    assert kr.metric_code == "KPI-LEAD-TIME"
    assert kr.approved_target == Decimal("10")


def test_draft_target_is_not_exposed_as_approved_target():
    kr = KeyResult(
        tenant_id="tenant-a",
        key_result_id="KR-1",
        objective_id="OBJ-1",
        title="Increase adherence",
        metric_code="KPI-ADHERENCE",
        direction=KeyResultDirection.INCREASE,
        target=Decimal("95"),
        target_evidence_refs=("ev-target",),
    )

    assert kr.target == Decimal("95")
    assert kr.approved_target is None


def test_baseline_and_target_require_evidence():
    with pytest.raises(ValueError, match="baseline requires evidence_refs"):
        KeyResult(
            tenant_id="tenant-a",
            key_result_id="KR-1",
            objective_id="OBJ-1",
            title="Reduce lead time",
            metric_code="KPI-LEAD-TIME",
            direction=KeyResultDirection.DECREASE,
            baseline=Decimal("15"),
        )

    with pytest.raises(ValueError, match="target requires evidence_refs"):
        KeyResult(
            tenant_id="tenant-a",
            key_result_id="KR-1",
            objective_id="OBJ-1",
            title="Reduce lead time",
            metric_code="KPI-LEAD-TIME",
            direction=KeyResultDirection.DECREASE,
            target=Decimal("10"),
        )


def test_approved_target_requires_explicit_approval_reference():
    with pytest.raises(ValueError, match="approved target requires target_approval_ref"):
        KeyResult(
            tenant_id="tenant-a",
            key_result_id="KR-1",
            objective_id="OBJ-1",
            title="Reduce lead time",
            metric_code="KPI-LEAD-TIME",
            direction=KeyResultDirection.DECREASE,
            target=Decimal("10"),
            target_evidence_refs=("ev-target",),
            target_approval_state=TargetApprovalState.APPROVED,
        )


def test_measurement_requires_evidence_and_timezone_aware_timestamp():
    measurement = Measurement(
        tenant_id="tenant-a",
        measurement_id="M-1",
        key_result_id="KR-1",
        metric_code="KPI-LEAD-TIME",
        value=Decimal("12.5"),
        measured_at=datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc),
        evidence_refs=("ev-measurement",),
        source_ref="mt_snapshots_kpi:row-1",
    )
    assert measurement.value == Decimal("12.5")

    with pytest.raises(ValueError, match="measurement requires evidence_refs"):
        Measurement(
            tenant_id="tenant-a",
            measurement_id="M-2",
            key_result_id="KR-1",
            metric_code="KPI-LEAD-TIME",
            value=Decimal("12.5"),
            measured_at=datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc),
            evidence_refs=(),
            source_ref="mt_snapshots_kpi:row-2",
        )

    with pytest.raises(ValueError, match="timezone-aware"):
        Measurement(
            tenant_id="tenant-a",
            measurement_id="M-3",
            key_result_id="KR-1",
            metric_code="KPI-LEAD-TIME",
            value=Decimal("12.5"),
            measured_at=datetime(2026, 10, 9, 12, 0),
            evidence_refs=("ev-measurement",),
            source_ref="mt_snapshots_kpi:row-3",
        )
