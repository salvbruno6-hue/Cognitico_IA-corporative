from elo.cognitive.routing.tool_search import progressive_tool_schema_disclosure
from elo.cognitive.routing.tool_search_outcome import (
    build_tool_search_performance_evidence,
)
from elo.cognitive.learning.performance_evidence import aggregate


def _selection():
    return progressive_tool_schema_disclosure(
        "browser navigation",
        {
            "browser_tool": "browser navigation and page lookup",
            "database_tool": "database query and records",
        },
        limit=1,
    )


def test_operational_outcome_reuses_existing_performance_evidence():
    evidence = build_tool_search_performance_evidence(
        tenant_id="tenant-test",
        context_key="tool-search:browser",
        selection=_selection(),
        quality=1.0,
        reliability=1.0,
        latency_ms=120.0,
        cost=0.01,
        provenance="controlled-operational-observation",
    )

    assert evidence.capability == "Progressive Tool Schema Disclosure"
    assert evidence.verified is True
    result = aggregate([evidence])
    assert len(result) == 1
    assert result[0].observations == 1
    assert result[0].evidence_state == "measured"
    assert result[0].promotion_state == "candidate"


def test_outcome_adapter_does_not_authorize_or_mutate_canonical_state():
    evidence = build_tool_search_performance_evidence(
        tenant_id="tenant-test",
        context_key="tool-search:browser",
        selection=_selection(),
        quality=0.9,
        reliability=0.95,
        latency_ms=100.0,
        cost=0.0,
        provenance="runtime-observation",
    )

    assert evidence.verified is True
    assert evidence.provenance == "runtime-observation"
