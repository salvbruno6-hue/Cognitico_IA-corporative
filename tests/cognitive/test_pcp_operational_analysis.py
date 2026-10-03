from datetime import date

from elo.cognitive.pcp_operational_analysis import (
    capacity_load, coverage, demand_gap, first_pass_yield,
    identify_bottleneck, lead_time_days, material_gap, net_demand,
    on_time, wip_delta,
)


def test_demand_and_net_demand():
    assert demand_gap(100, 80).value == 20
    assert net_demand(100, 20, 30).value == 50


def test_capacity_and_bottleneck():
    assert capacity_load(90, 100).value == 0.9
    result = identify_bottleneck([
        {"id": "CT-1", "carga": 90, "capacidade": 100},
        {"id": "CT-2", "carga": 120, "capacidade": 100},
    ])
    assert result.inputs["recurso"] == "CT-2"
    assert result.value == 1.2


def test_material_and_coverage():
    assert material_gap(100, 40, 20).value == 40
    assert coverage(40, 10).value == 4


def test_flow_and_lead_time():
    assert wip_delta(12, 9).value == 3
    assert lead_time_days(date(2026, 9, 1), date(2026, 9, 6)).value == 5


def test_delivery_and_quality_kpis():
    assert on_time(date(2026, 9, 10), date(2026, 9, 9)).value == 1
    assert on_time(date(2026, 9, 10), date(2026, 9, 11)).value == 0
    assert first_pass_yield(8, 10).value == 0.8


def test_missing_data_is_not_invented():
    assert demand_gap(100, None).status == "NAO_LOCALIZADO"
    assert capacity_load(10, 0).status == "NAO_LOCALIZADO"
    assert material_gap(10, None, 2).status == "NAO_LOCALIZADO"
    assert lead_time_days(None, date(2026, 9, 6)).status == "NAO_LOCALIZADO"
