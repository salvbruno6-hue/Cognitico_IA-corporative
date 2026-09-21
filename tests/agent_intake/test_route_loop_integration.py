from elo.agent_intake.hermes_routing_boundary import RoutingDisposition, RoutingSignal, assess_routing
from elo.agent_intake.route_loop_integration import run_route_loop_probe
from elo.agent_intake.implementation_loop import ImplementationStage

def test_route_boundary_rejects_authority_or_bypass():
    base = dict(route_id="r1", tenant_scope="t1", source_refs=("ref:1",),
                primary_provider="a", fallback_providers=("b",),
                credential_pool_strategy="bounded", provenance_verified=True,
                explicit_policy=True)
    assert assess_routing(RoutingSignal(**base)).disposition is RoutingDisposition.CANDIDATE
    assert assess_routing(RoutingSignal(**base, canonical_routing_authority=True)).disposition is RoutingDisposition.REJECTED
    assert assess_routing(RoutingSignal(**base, governance_bypass=True)).disposition is RoutingDisposition.REJECTED

def test_route_loop_has_positive_repeatable_gain_and_stops_at_review():
    decision, evidence = run_route_loop_probe(repeats=5)
    assert evidence.baseline["successful_policy_routed_execution_rate"] == 0.0
    assert evidence.adapted["successful_policy_routed_execution_rate"] == 1.0
    assert evidence.repeatable is True
    assert evidence.boundary_integrity is True
    assert evidence.is_complete() is True
    assert decision.stage is ImplementationStage.ELO_REVIEW
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
