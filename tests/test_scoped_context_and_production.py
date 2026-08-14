from elo.core.context_resolution import ContextEvidence, ContextPack, ContextQuery, ContextSource
from elo.core.production_flow import ProductionEvent, ProductionFlow, ProductionStage


def test_evidence_requires_exact_tenant_and_unit_scope():
    query = ContextQuery(
        "estado da Multiteiner Caxias",
        entity="Multiteiner",
        scope="Duque de Caxias",
        tenant_id="multiteiner",
    )
    pack = ContextPack(
        query=query,
        sources=(
            ContextSource("good", "project", "authorized", "Duque de Caxias", "multiteiner"),
            ContextSource("wrong-unit", "project", "authorized", "São Paulo", "multiteiner"),
            ContextSource("wrong-tenant", "project", "authorized", "Duque de Caxias", "other"),
        ),
        evidence=(
            ContextEvidence("good", "pedido Caxias", 0.9, tenant_id="multiteiner", scope="Duque de Caxias"),
            ContextEvidence("wrong-unit", "pedido SP", 0.95, tenant_id="multiteiner", scope="São Paulo"),
            ContextEvidence("wrong-tenant", "pedido outra empresa", 0.99, tenant_id="other", scope="Duque de Caxias"),
        ),
    )
    assert [item.source_id for item in pack.scoped_evidence()] == ["good"]
    assert pack.requires_specialist()


def test_high_confidence_wrong_scope_cannot_enable_specialist():
    query = ContextQuery("estado da Multiteiner Caxias", "Multiteiner", "Duque de Caxias", tenant_id="multiteiner")
    pack = ContextPack(
        query=query,
        sources=(ContextSource("wrong", "project", "authorized", "São Paulo", "multiteiner"),),
        evidence=(ContextEvidence("wrong", "evidência errada", 1.0, tenant_id="multiteiner", scope="São Paulo"),),
    )
    assert not pack.sufficient_evidence()
    assert not pack.requires_specialist()


def test_production_flow_can_complete_and_be_scoped():
    events = (
        ProductionEvent("1", ProductionStage.DEMAND, tenant_id="multiteiner", unit_scope="Duque de Caxias"),
        ProductionEvent("2", ProductionStage.PLANNING, tenant_id="multiteiner", unit_scope="Duque de Caxias"),
        ProductionEvent("3", ProductionStage.EXECUTION, tenant_id="multiteiner", unit_scope="Duque de Caxias", deviation="material shortage"),
        ProductionEvent("4", ProductionStage.OUTCOME, tenant_id="multiteiner", unit_scope="Duque de Caxias"),
        ProductionEvent("5", ProductionStage.EXECUTION, tenant_id="other", unit_scope="Duque de Caxias"),
    )
    flow = ProductionFlow("PF-001", events)
    assert flow.lifecycle_complete()
    assert len(flow.deviations()) == 1
    scoped = flow.scoped(tenant_id="multiteiner", unit_scope="Duque de Caxias")
    assert len(scoped.events) == 4
    assert all(event.tenant_id == "multiteiner" for event in scoped.events)
