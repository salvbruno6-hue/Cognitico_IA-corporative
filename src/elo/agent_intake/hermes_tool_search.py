"""Candidate-only contract for Hermes progressive tool-schema disclosure.

The contract records tool-search configuration as evidence. It never searches,
loads, invokes, enables, or executes a Hermes tool and never mutates ELO memory.
The existing ELO Model/Tool Routing owner remains authoritative.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class ToolSearchCandidate:
    candidate_id: str
    deferred_tools: tuple[str, ...]
    listing_budget_tokens: int
    default_limit: int
    max_limit: int
    source_revision: str
    candidate_only: bool = True
    canonical_mutation: bool = False


def observe_tool_search(
    *,
    deferred_tools: Iterable[str],
    listing_budget_tokens: int,
    default_limit: int,
    max_limit: int,
    source_revision: str,
) -> ToolSearchCandidate:
    """Normalize Hermes tool-search metadata without invoking discovery."""
    tools = tuple(str(item).strip() for item in deferred_tools if str(item).strip())
    if len(tools) != len(set(tools)):
        raise ValueError("deferred_tools contains duplicates")
    if listing_budget_tokens < 0:
        raise ValueError("listing_budget_tokens must be non-negative")
    if default_limit < 1:
        raise ValueError("default_limit must be positive")
    if max_limit < default_limit:
        raise ValueError("max_limit must be >= default_limit")
    return ToolSearchCandidate(
        candidate_id="EXT-TOOL-SEARCH-HERMES",
        deferred_tools=tools,
        listing_budget_tokens=listing_budget_tokens,
        default_limit=default_limit,
        max_limit=max_limit,
        source_revision=source_revision,
    )


def candidate_metadata(candidate: ToolSearchCandidate) -> dict[str, object]:
    """Return governance metadata; no execution or promotion is implied."""
    return {
        "candidate_id": candidate.candidate_id,
        "candidate_only": candidate.candidate_only,
        "canonical_mutation": candidate.canonical_mutation,
        "authority": "ELO Model/Tool Routing",
        "source": "hermes",
    }


__all__ = ["ToolSearchCandidate", "observe_tool_search", "candidate_metadata"]
