"""Controlled confrontation between the PCP analytical kernel and the existing virtual diagnosis.

The scenario is repository-owned simulation data. This test does not treat simulated
results as operational evidence and does not promote learning.
"""

from datetime import date

from elo.cognitive.pcp_symbiont_integration import (
    bottleneck,
    net_material_requirement,
    potential_delay,
    utilization,
)


def test_pcp_kernel_confronts_virtual_diagnosis_scope():
    # Same inputs used by elo-virtual-core/data/*.
    resource_001_capacity = 160.0
    resource_001_committed = 145.0
    demand_001_hours = 20.0
    demand_003_hours = 30.0

    # The diagnosis projects each demand independently.
    demand_001_uti = utilization(
        resource_001_committed + demand_001_hours,
        resource_001_capacity,
    )
    demand_003_uti = utilization(
        resource_001_committed + demand_003_hours,
        resource_001_capacity,
    )

    assert demand_001_uti.status == "CALCULADO"
    assert demand_001_uti.value == 165.0 / 160.0
    assert demand_003_uti.status == "CALCULADO"
    assert demand_003_uti.value == 175.0 / 160.0

    # The PCP bottleneck calculation aggregates the resource load across
    # linked demands; this is intentionally not asserted as identical to the
    # per-demand signal emitted by diagnose().
    aggregate = bottleneck(
        [
            {
                "id": "REC-001",
                "carga": resource_001_committed + demand_001_hours + demand_003_hours,
                "capacidade": resource_001_capacity,
            },
            {
                "id": "REC-002",
                "carga": 90.0 + 15.0,
                "capacidade": 160.0,
            },
        ]
    )
    assert aggregate.status == "CALCULADO"
    assert aggregate.inputs["recurso"] == "REC-001"
    assert aggregate.value == 195.0 / 160.0


def test_material_gap_is_not_promoted_to_nlm_without_safety_stock():
    # diagnose() can report the raw deficit: 8 required - 2 available = 6.
    # The PCP NLM formula additionally requires material safety stock, which
    # is absent from this controlled dataset.
    result = net_material_requirement(
        gross_need=8.0,
        material_stock=2.0,
        material_safety_stock=None,
    )

    assert result.status == "NAO_LOCALIZADO"
    assert "ESM" in result.inputs["missing"]


def test_material_delay_is_recomputed_from_dates():
    # The repository diagnosis uses the dates, not the denormalized atraso_dias
    # field. 2026-09-08 versus 2026-09-03 is a 5-day delay.
    result = potential_delay(
        projected_delivery=date(2026, 9, 8),
        need_date=date(2026, 9, 3),
    )

    assert result.status == "CALCULADO"
    assert result.value == 5
