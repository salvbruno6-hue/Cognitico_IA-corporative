from src.elo.agent_intake.hermes_routing_boundary import RoutingSignal,RoutingDisposition,assess_routing
def _signal(**kw):
 b=dict(route_id="route-1",tenant_scope="multiteiner",source_refs=("hermes:routing:1",),primary_provider="provider-a",fallback_providers=("provider-b",),credential_pool_strategy="bounded",provenance_verified=True,explicit_policy=True);b.update(kw);return RoutingSignal(**b)
def test_verified_policy_is_candidate_only():
 a=assess_routing(_signal());assert a.disposition is RoutingDisposition.CANDIDATE and a.canonical_authority is False and a.execution_permitted is False and a.governance_bypass_permitted is False
def test_no_policy_is_observation(): assert assess_routing(_signal(explicit_policy=False)).disposition is RoutingDisposition.OBSERVATION
def test_missing_provenance_rejected(): assert assess_routing(_signal(provenance_verified=False)).disposition is RoutingDisposition.REJECTED
def test_second_authority_rejected(): assert assess_routing(_signal(canonical_routing_authority=True)).disposition is RoutingDisposition.REJECTED
def test_bypass_rejected(): assert assess_routing(_signal(governance_bypass=True)).disposition is RoutingDisposition.REJECTED
