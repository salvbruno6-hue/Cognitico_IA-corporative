from elo.cognitive.methodology import (
    MethodEvidence,
    MethodObservation,
    discover_method,
)


def test_discovery_keeps_tenant_method_scoped():
    observations = [
        MethodObservation(
            domain="budget",
            process="estimate",
            attribute="loss_rate",
            value=0.035,
            evidence=MethodEvidence.OBSERVED,
            source="budget-001.xlsx",
            tenant_id="tenant-a",
        ),
        MethodObservation(
            domain="budget",
            process="estimate",
            attribute="unit",
            value="kg",
            evidence=MethodEvidence.OBSERVED,
            source="budget-001.xlsx",
            tenant_id="tenant-b",
        ),
    ]
    model = discover_method(observations, tenant_id="tenant-a")
    assert model.attributes() == {"loss_rate": 0.035}
    assert all(item.tenant_id == "tenant-a" for item in model.observations)


def test_external_knowledge_is_not_tenant_observation():
    observation = MethodObservation(
        domain="budget",
        process="estimate",
        attribute="loss_rate",
        value=0.05,
        evidence=MethodEvidence.EXTERNAL,
        source="external-research",
    )
    observation.validate()
    assert not observation.is_private
    assert observation.generalization_candidate()
