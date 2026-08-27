from elo.cognitive.learning.performance_evidence import PerformanceEvidence, aggregate, to_routing_metadata


def evidence(tenant: str, quality: float = .9, context: str = "budget"):
    return PerformanceEvidence(
        tenant_id=tenant,
        capability="retrieval",
        context_key=context,
        model_id="model-a",
        tool_id="supabase",
        verified=True,
        quality=quality,
        reliability=.95,
        latency_ms=100,
        cost=.1,
        provenance="execution-trace:1",
    )


def test_aggregate_keeps_tenants_and_contexts_isolated():
    result = aggregate([evidence("a"), evidence("b"), evidence("a", context="contract")])
    assert {(item.tenant_id, item.context_key) for item in result} == {
        ("a", "budget"), ("a", "contract"), ("b", "budget")
    }


def test_unverified_execution_is_rejected():
    item = evidence("a")
    object.__setattr__(item, "verified", False)
    try:
        aggregate([item])
    except ValueError as exc:
        assert "unverified" in str(exc)
    else:
        raise AssertionError("unverified evidence must be rejected")


def test_minimum_observations_gate_prevents_weak_routing_evidence():
    assert aggregate([evidence("a")], minimum_observations=2) == []
    result = aggregate([evidence("a"), evidence("a")], minimum_observations=2)
    assert result[0].observations == 2
    assert 0.0 < result[0].confidence < 1.0


def test_routing_metadata_preserves_scope_and_candidate_state():
    result = aggregate([evidence("a"), evidence("a")])[0]
    metadata = to_routing_metadata(result)
    assert metadata["tenant_id"] == "a"
    assert metadata["context_key"] == "budget"
    assert metadata["promotion_state"] == "candidate"
