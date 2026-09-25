from elo.cognitive.learning.performance_evidence import aggregate
from elo.cognitive.routing.tool_search import progressive_tool_schema_disclosure
from elo.cognitive.routing.tool_search_outcome import (
    build_tool_search_indirect_performance_evidence,
)


def _selection():
    return progressive_tool_schema_disclosure(
        "browser navigation",
        {
            "browser_tool": "browser navigation and page lookup",
            "database_tool": "database query and records",
        },
        limit=1,
    )


def test_skill_can_be_evaluated_through_validated_downstream_experience():
    evidence = build_tool_search_indirect_performance_evidence(
        tenant_id="tenant-test",
        context_key="tool-search:browser",
        selection=_selection(),
        observer_capability="ExecutionRouter",
        experience_ref="experience:router-browser-001",
        expected_outcome="relevant browser context reaches the operational path",
        observed_outcome="relevant browser context reached the operational path",
        relationship="selected schema context was consumed by the validated router path",
        quality=1.0,
        reliability=1.0,
        latency_ms=120.0,
        cost=0.01,
    )

    assert evidence.verified is True
    assert "mode=INDIRECT_EXPERIENCE" in evidence.provenance
    assert "observer_capability=ExecutionRouter" in evidence.provenance
    assert "experience_ref=experience:router-browser-001" in evidence.provenance

    result = aggregate([evidence])
    assert len(result) == 1
    assert result[0].observations == 1
    assert result[0].evidence_state == "measured"


def test_indirect_evidence_does_not_claim_causality_or_mutate_canonical_state():
    evidence = build_tool_search_indirect_performance_evidence(
        tenant_id="tenant-test",
        context_key="tool-search:browser",
        selection=_selection(),
        observer_capability="ExecutionRouter",
        experience_ref="experience:router-browser-002",
        expected_outcome="schema context is available",
        observed_outcome="schema context is available",
        relationship="downstream validated capability observed the prepared context",
        quality=0.9,
        reliability=0.95,
        latency_ms=100.0,
        cost=0.0,
    )

    assert "relationship=" in evidence.provenance
    assert "mode=INDIRECT_EXPERIENCE" in evidence.provenance
    assert evidence.capability == "Progressive Tool Schema Disclosure"


def test_indirect_evidence_requires_explicit_observer_and_experience():
    try:
        build_tool_search_indirect_performance_evidence(
            tenant_id="tenant-test",
            context_key="tool-search:browser",
            selection=_selection(),
            observer_capability="",
            experience_ref="",
            expected_outcome="expected",
            observed_outcome="observed",
            relationship="validated downstream observation",
            quality=1.0,
            reliability=1.0,
            latency_ms=10.0,
            cost=0.0,
        )
    except ValueError as exc:
        assert "indirect evidence requires" in str(exc)
    else:
        raise AssertionError("missing observer/experience must be rejected")
