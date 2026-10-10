from datetime import datetime, timezone
from decimal import Decimal

import pytest

from elo.application.queries.okr import OkrQueryService
from elo.contracts.okr import KeyResult, KeyResultDirection, Measurement, Objective


class FakeOkrRepository:
    def __init__(self, *, objectives=(), key_results=(), measurements=()):
        self.objectives = {item.objective_id: item for item in objectives}
        self.key_results = {item.key_result_id: item for item in key_results}
        self.measurements = tuple(measurements)

    def get_objective(self, *, tenant_id: str, objective_id: str):
        return self.objectives.get(objective_id)

    def get_key_result(self, *, tenant_id: str, key_result_id: str):
        return self.key_results.get(key_result_id)

    def list_key_results(self, *, tenant_id: str, objective_id: str):
        return tuple(item for item in self.key_results.values() if item.objective_id == objective_id)

    def list_measurements(self, *, tenant_id: str, key_result_id: str):
        return tuple(item for item in self.measurements if item.key_result_id == key_result_id)


def _objective(tenant_id="tenant-a"):
    return Objective(
        tenant_id=tenant_id,
        objective_id="OBJ-1",
        title="Improve operational reliability",
        key_result_ids=("KR-1",),
    )


def _kr(tenant_id="tenant-a", metric_code="KPI-LEAD-TIME"):
    return KeyResult(
        tenant_id=tenant_id,
        key_result_id="KR-1",
        objective_id="OBJ-1",
        title="Reduce lead time",
        metric_code=metric_code,
        direction=KeyResultDirection.DECREASE,
    )


def _measurement(tenant_id="tenant-a", metric_code="KPI-LEAD-TIME"):
    return Measurement(
        tenant_id=tenant_id,
        measurement_id="M-1",
        key_result_id="KR-1",
        metric_code=metric_code,
        value=Decimal("12.4"),
        measured_at=datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc),
        evidence_refs=("ev-1",),
        source_ref="mt_snapshots_kpi:row-1",
    )


def test_objective_context_returns_objective_and_related_key_results():
    service = OkrQueryService(FakeOkrRepository(objectives=(_objective(),), key_results=(_kr(),)))

    context = service.objective_context(tenant_id="tenant-a", objective_id="OBJ-1")

    assert context is not None
    assert context.objective.objective_id == "OBJ-1"
    assert tuple(item.key_result_id for item in context.key_results) == ("KR-1",)


def test_key_result_context_returns_measurements_without_calculating_status():
    service = OkrQueryService(
        FakeOkrRepository(key_results=(_kr(),), measurements=(_measurement(),))
    )

    context = service.key_result_context(tenant_id="tenant-a", key_result_id="KR-1")

    assert context is not None
    assert context.key_result.metric_code == "KPI-LEAD-TIME"
    assert context.measurements[0].value == Decimal("12.4")
    assert not hasattr(context, "status")
    assert not hasattr(context, "progress")


def test_service_fails_closed_on_cross_tenant_objective():
    service = OkrQueryService(FakeOkrRepository(objectives=(_objective("tenant-b"),)))

    with pytest.raises(PermissionError, match="tenant boundary"):
        service.objective_context(tenant_id="tenant-a", objective_id="OBJ-1")


def test_service_fails_closed_on_cross_tenant_measurement():
    service = OkrQueryService(
        FakeOkrRepository(
            key_results=(_kr(),),
            measurements=(_measurement("tenant-b"),),
        )
    )

    with pytest.raises(PermissionError, match="tenant boundary"):
        service.key_result_context(tenant_id="tenant-a", key_result_id="KR-1")


def test_measurement_metric_must_match_key_result_metric():
    service = OkrQueryService(
        FakeOkrRepository(
            key_results=(_kr(),),
            measurements=(_measurement(metric_code="KPI-OTHER"),),
        )
    )

    with pytest.raises(ValueError, match="metric_code"):
        service.key_result_context(tenant_id="tenant-a", key_result_id="KR-1")
