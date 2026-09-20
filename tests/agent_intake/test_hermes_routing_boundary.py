from src.elo.agent_intake.hermes_routing_boundary import (
    RoutingSignal, RoutingDisposition, assess_routing,
)

def _signal(**kw):
    base = dict(route_id="route-1", tenant_scope="multiteiner",
                source_refs=("hermes:routing:1",), primary_provider="openrouter",
                fallback_providers=("anthropic",),
                credential_pool_strategy="round_robin",
                provenance_verified=True, explicit_policy=True)
    base.update(kw)
    return RoutingSignal(**base)

def test_verified_policy_is_candidate_only():
    a = assess_routing(_signal())
    assert a.disposition is RoutingDisposition.CANDIDATE
    assert a.canonical_authority is False
    assert a.execution_permitted is False
    assert a.governance_bypass_permitted is False

def test_no_explicit_policy_is_observation():
    a = assess_routing(_signal(explicit_policy=False))
    assert a.disposition is RoutingDisposition.OBSERVATION

def test_missing_provenance_is_rejected():
    a = assess_routing(_signal(provenance_verified=False))
    assert a.disposition is RoutingDisposition.REJECTED

def test_second_routing_authority_is_rejected():
    a = assess_routing(_signal(canonical_routing_authority=True))
    assert a.disposition is RoutingDisposition.REJECTED

def test_governance_bypass_is_rejected():
    a = assess_routing(_signal(governance_bypass=True))
    assert a.disposition is RoutingDisposition.REJECTED