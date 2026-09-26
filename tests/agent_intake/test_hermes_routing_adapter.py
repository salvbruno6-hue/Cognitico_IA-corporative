from elo.agent_intake.hermes_routing_adapter import adapt_routing
from elo.agent_intake.hermes_routing_boundary import RoutingDisposition, RoutingSignal


def signal(**overrides):
    values = dict(
        route_id="route-test-1",
        tenant_scope="multiteiner",
        source_refs=("controlled-eval:route/1",),
        primary_provider="provider-a",
        fallback_providers=("provider-b",),
        credential_pool_strategy="bounded-pool-v1",
        provenance_verified=True,
        explicit_policy=True,
        canonical_routing_authority=False,
        governance_bypass=False,
    )
    values.update(overrides)
    return RoutingSignal(**values)


def test_adapts_policy_route_to_bounded_plan():
    contract = adapt_routing(signal())
    assert contract is not None
    assert contract.disposition is RoutingDisposition.CANDIDATE
    assert contract.execution_permitted is False
    assert contract.canonical_authority is False
    assert contract.governance_bypass_permitted is False


def test_rejects_canonical_routing_authority():
    assert adapt_routing(signal(canonical_routing_authority=True)) is None


def test_rejects_governance_bypass():
    assert adapt_routing(signal(governance_bypass=True)) is None
