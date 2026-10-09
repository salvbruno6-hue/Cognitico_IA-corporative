from datetime import datetime, timedelta, timezone
from decimal import Decimal

from elo.application.queries.okr import KeyResultContext
from elo.application.queries.okr_metric import OkrMetricResolver
from elo.contracts.okr import KeyResult, KeyResultDirection, Measurement


class FakeFormalKpiRegistry:
    def __init__(self, definitions):
        self.definitions = definitions

    def get_definition(self, *, metric_code: str):
        return self.definitions.get(metric_code)


def _kr(metric_code="KPI-LEAD-TIME"):
    return KeyResult(
        tenant_id="tenant-a",
        key_result_id="KR-1",
        objective_id="OBJ-1",
        title="Reduce lead time",
        metric_code=metric_code,
        direction=KeyResultDirection.DECREASE,
    )


def _measurement(mid: str, value: str, when: datetime):
    return Measurement(
        tenant_id="tenant-a",
        measurement_id=mid,
        key_result_id="KR-1",
        metric_code="KPI-LEAD-TIME",
        value=Decimal(value),
        measured_at=when,
        evidence_refs=(f"ev:{mid}",),
        source_ref=f"mt_snapshots_kpi:{mid}",
    )


def _definition(active=True):
    return {
        "codigo_kpi": "KPI-LEAD-TIME",
        "nome": "Lead Time",
        "unidade": "dias",
        "formula": "data_fim - data_inicio",
        "ativo": active,
    }


def test_missing_definition_keeps_metric_fail_closed_and_current_unknown():
    resolver = OkrMetricResolver(FakeFormalKpiRegistry({}))

    state = resolver.resolve(KeyResultContext(key_result=_kr(), measurements=()))

    assert state.metric_state == "SEM_KPI_FORMAL_REGISTRADO"
    assert state.kpi is None
    assert state.current is None


def test_inactive_definition_is_not_treated_as_formal_kpi():
    resolver = OkrMetricResolver(
        FakeFormalKpiRegistry({"KPI-LEAD-TIME": _definition(active=False)})
    )

    state = resolver.resolve(KeyResultContext(key_result=_kr(), measurements=()))

    assert state.metric_state == "SEM_KPI_FORMAL_REGISTRADO"
    assert state.current is None


def test_formal_kpi_without_measurement_does_not_turn_current_into_zero():
    resolver = OkrMetricResolver(
        FakeFormalKpiRegistry({"KPI-LEAD-TIME": _definition()})
    )

    state = resolver.resolve(KeyResultContext(key_result=_kr(), measurements=()))

    assert state.metric_state == "KPI_FORMAL_SEM_MEDICAO"
    assert state.kpi is not None
    assert state.current is None


def test_current_is_latest_valid_measurement_and_preserves_evidence():
    now = datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc)
    older = _measurement("M-1", "13.8", now - timedelta(days=7))
    newer = _measurement("M-2", "12.4", now)
    resolver = OkrMetricResolver(
        FakeFormalKpiRegistry({"KPI-LEAD-TIME": _definition()})
    )

    state = resolver.resolve(
        KeyResultContext(key_result=_kr(), measurements=(newer, older))
    )

    assert state.metric_state == "KPI_FORMAL_COM_MEDICAO"
    assert state.current == Decimal("12.4")
    assert state.current_measurement_id == "M-2"
    assert state.current_evidence_refs == ("ev:M-2",)
