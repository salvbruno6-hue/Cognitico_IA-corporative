from dataclasses import dataclass
from typing import Iterable

from elo.cognitive.routing.tool_search import ToolSchemaSelection, progressive_tool_schema_disclosure


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


def observe_tool_search(*, deferred_tools: Iterable[str], listing_budget_tokens: int, default_limit: int, max_limit: int, source_revision: str) -> ToolSearchCandidate:
    tools = tuple(str(item).strip() for item in deferred_tools if str(item).strip())
    if len(tools) != len(set(tools)):
        raise ValueError("deferred_tools contains duplicates")
    if listing_budget_tokens < 0:
        raise ValueError("listing_budget_tokens must be non-negative")
    if default_limit < 1:
        raise ValueError("default_limit must be positive")
    if max_limit < default_limit:
        raise ValueError("max_limit must be >= default_limit")
    return ToolSearchCandidate("EXT-TOOL-SEARCH-HERMES", tools, listing_budget_tokens, default_limit, max_limit, source_revision)


def candidate_metadata(candidate: ToolSearchCandidate) -> dict[str, object]:
    return {"candidate_id": candidate.candidate_id, "candidate_only": candidate.candidate_only, "canonical_mutation": candidate.canonical_mutation, "authority": "ELO Model/Tool Routing", "source": "hermes"}


__all__ = ["ToolSearchCandidate", "ToolSchemaSelection", "observe_tool_search", "progressive_tool_schema_disclosure", "candidate_metadata"]
