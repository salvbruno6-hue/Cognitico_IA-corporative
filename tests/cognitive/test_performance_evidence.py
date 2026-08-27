from elo.cognitive.learning.performance_evidence import PerformanceEvidence, aggregate


def evidence(tenant: str, quality: float = .9):
    return PerformanceEvidence(
        tenant_id=tenant,
        capability="retrieval",
        context_key="budget",
        model_id="model-a",
        tool_id="supabase",
        verified=True,
        quality=quality,
        reliability=.95,
        latency_ms=100,
        cost=.1,
        provenance="execution-trace:1",
    )


def test_aggregate_keeps_tenants_isolated():
    result = aggregate([evidence("a"), evidence("b")])
    assert len(result) == 2


def test_unverified_execution_is_rejected():
    item = evidence("a")
    object.__setattr__(item, "verified", False)
    try:
        aggregate([item])
    except ValueError as exc:
        assert "unverified" in str(exc)
    else:
        raise AssertionError("unverified evidence must be rejected")
