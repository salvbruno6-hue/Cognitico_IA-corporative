import pytest

from elo.agent_intake.hermes_current_extensions import build_candidate
from elo.agent_intake.hermes_tool_search import (
    candidate_metadata,
    observe_tool_search,
    progressive_tool_schema_disclosure,
)


REV = "hermes-main@2026-09-24"


def test_tool_search_reuses_existing_routing_owner():
    candidate = build_candidate("EXT-TOOL-SEARCH-HERMES")
    assert candidate.owner == "ELO Model/Tool Routing"
    assert candidate.promotion_state == "candidate_only"
    assert candidate.canonical_mutation is False


def test_tool_search_normalizes_metadata_without_execution():
    observed = observe_tool_search(
        deferred_tools=("session_search", "computer_use", "mcp_tool"),
        listing_budget_tokens=4000,
        default_limit=5,
        max_limit=25,
        source_revision=REV,
    )
    assert observed.deferred_tools == ("session_search", "computer_use", "mcp_tool")
    assert observed.listing_budget_tokens == 4000
    assert observed.default_limit == 5
    assert observed.max_limit == 25
    assert observed.source_revision == REV
    assert observed.candidate_only is True
    assert observed.canonical_mutation is False


def test_tool_search_progressively_discloses_only_relevant_schemas():
    catalog = {
        "session_search": "search session context",
        "computer_use": "browser computer interaction",
        "mcp_tool": "external tool invocation",
    }
    result = progressive_tool_schema_disclosure("browser", catalog, limit=1)
    assert result.selected_tools == ("computer_use",)
    assert result.disclosed_schemas == (("computer_use", "browser computer interaction"),)
    assert result.bounded is True
    assert result.executed is False
    assert result.canonical_mutation is False
    assert result.representation_chars == len("computer_use") + len("browser computer interaction")


def test_tool_search_respects_limit_and_catalog_order():
    catalog = {
        "alpha_tool": "alpha browser",
        "beta_tool": "beta browser",
        "gamma_tool": "gamma browser",
    }
    result = progressive_tool_schema_disclosure("browser", catalog, limit=2)
    assert result.selected_tools == ("alpha_tool", "beta_tool")


def test_tool_search_does_not_disclose_unrelated_schema():
    catalog = {
        "session_search": "search session context",
        "computer_use": "browser computer interaction",
    }
    result = progressive_tool_schema_disclosure("database", catalog)
    assert result.selected_tools == ()
    assert result.disclosed_schemas == ()
    assert result.representation_chars == 0


def test_tool_search_rejects_duplicate_deferred_tools():
    with pytest.raises(ValueError, match="duplicates"):
        observe_tool_search(
            deferred_tools=("session_search", "session_search"),
            listing_budget_tokens=4000,
            default_limit=5,
            max_limit=25,
            source_revision=REV,
        )


def test_tool_search_rejects_invalid_limits():
    with pytest.raises(ValueError, match="max_limit"):
        observe_tool_search(
            deferred_tools=("session_search",),
            listing_budget_tokens=4000,
            default_limit=5,
            max_limit=4,
            source_revision=REV,
        )


def test_tool_search_rejects_empty_query():
    with pytest.raises(ValueError, match="query"):
        progressive_tool_schema_disclosure("   ", {"session_search": "search session"})


def test_tool_search_metadata_does_not_grant_authority():
    observed = observe_tool_search(
        deferred_tools=("session_search",),
        listing_budget_tokens=4000,
        default_limit=5,
        max_limit=25,
        source_revision=REV,
    )
    metadata = candidate_metadata(observed)
    assert metadata["authority"] == "ELO Model/Tool Routing"
    assert metadata["candidate_only"] is True
    assert metadata["canonical_mutation"] is False
