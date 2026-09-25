"""Controlled observation adapter for the governed Hermes tool-search capability.

This module records runtime-shaped routing observations without executing a
selected tool, mutating canonical memory, or promoting the Hermes candidate.
Production evidence remains a separate deployment concern.
"""

from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.routing.execution_routing import ExecutionRouter
from elo.cognitive.routing.tool_search import ToolSchemaSelection

CANDIDATE_ID = "EXT-TOOL-SEARCH-HERMES"
OWNER = "ELO Model/Tool Routing"


@dataclass(frozen=True, slots=True)
class ToolSearchObservation:
    candidate_id: str
    owner: str
    query: str
    selected_tools: tuple[str, ...]
    disclosed_schema_count: int
    representation_chars: int
    bounded: bool
    executed: bool
    canonical_mutation: bool
    environment: str
    evidence_status: str = "CONTROLLED_OBSERVATION"

    @property
    def production_evidence(self) -> bool:
        return self.environment.upper() == "PRODUCTION" and self.evidence_status == "PRODUCTION_OBSERVED"


def observe_tool_search(
    router: ExecutionRouter,
    query: str,
    tool_schemas: dict[str, str],
    *,
    limit: int = 5,
    environment: str = "CONTROLLED_OBSERVATION",
) -> ToolSearchObservation:
    """Observe governed schema selection without invoking a tool.

    The adapter intentionally delegates selection to the existing
    ExecutionRouter authority. It never writes memory or executes a tool.
    """
    selection: ToolSchemaSelection = router.search_tool_schemas(
        query,
        tool_schemas,
        limit=limit,
    )
    if selection.executed:
        raise RuntimeError("tool-search observation must not execute tools")
    if selection.canonical_mutation:
        raise RuntimeError("tool-search observation must not mutate canonical memory")

    return ToolSearchObservation(
        candidate_id=CANDIDATE_ID,
        owner=OWNER,
        query=selection.query,
        selected_tools=selection.selected_tools,
        disclosed_schema_count=len(selection.disclosed_schemas),
        representation_chars=selection.representation_chars,
        bounded=selection.bounded,
        executed=selection.executed,
        canonical_mutation=selection.canonical_mutation,
        environment=environment,
    )
