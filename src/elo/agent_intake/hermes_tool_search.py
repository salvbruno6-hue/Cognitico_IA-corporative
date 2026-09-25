"""Governed implementation for progressive tool-schema disclosure.

The implementation belongs to the existing ELO Model/Tool Routing owner.
It performs bounded, deterministic schema selection only. It does not invoke
Hermes tools, execute selected tools, mutate canonical memory, or grant
promotion authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


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


@dataclass(frozen=True, slots=True)
class ToolSchemaSelection:
    query: str
    selected_tools: tuple[str, ...]
    disclosed_schemas: tuple[tuple[str, str], ...]
    representation_chars: int
    bounded: bool = True
    executed: bool = False
    canonical_mutation: bool = False


def observe_tool_search(
    *,
    deferred_tools: Iterable[str],
    listing_budget_tokens: int,
    default_limit: int,
    max_limit: int,
    source_revision: str,
) -> ToolSearchCandidate:
    """Normalize tool-search metadata without invoking discovery."""
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


def progressive_tool_schema_disclosure(
    query: str,
    tool_schemas: Mapping[str, str],
    *,
    limit: int = 5,
) -> ToolSchemaSelection:
    """Select only relevant schemas from an existing allowlisted catalog.

    Relevance is deterministic: a tool is selected when any non-empty query
    token occurs in its name or schema text. Results preserve catalog order and
    are bounded by the supplied limit. No selected tool is invoked.
    """
    normalized_query = " ".join(str(query).lower().split())
    if not normalized_query:
        raise ValueError("query must be non-empty")
    if limit < 1:
        raise ValueError("limit must be positive")

    tokens = tuple(token for token in normalized_query.split() if token)
    selected: list[tuple[str, str]] = []
    for name, schema in tool_schemas.items():
        normalized_name = str(name).lower()
        normalized_schema = str(schema).lower()
        if any(token in normalized_name or token in normalized_schema for token in tokens):
            selected.append((str(name), str(schema)))
            if len(selected) >= limit:
                break

    disclosed = tuple(selected)
    selected_tools = tuple(name for name, _ in disclosed)
    representation_chars = sum(len(name) + len(schema) for name, schema in disclosed)
    return ToolSchemaSelection(
        query=normalized_query,
        selected_tools=selected_tools,
        disclosed_schemas=disclosed,
        representation_chars=representation_chars,
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


__all__ = [
    "ToolSearchCandidate",
    "ToolSchemaSelection",
    "observe_tool_search",
    "progressive_tool_schema_disclosure",
    "candidate_metadata",
]
