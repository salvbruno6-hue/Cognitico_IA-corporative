"""Operational tool-schema disclosure through the canonical runtime router.

This adapter does not introduce a second routing authority. It prepares the
bounded schema context used by an existing runtime before execution.
"""

from __future__ import annotations

from elo.cognitive.routing.execution_routing import ExecutionRouter
from elo.cognitive.routing.tool_search import ToolSchemaSelection


def prepare_tool_schema_context(
    execution_router: ExecutionRouter,
    *,
    query: str,
    tool_schemas: dict[str, str],
    limit: int = 5,
) -> ToolSchemaSelection:
    """Select bounded schema context for an operational runtime request.

    The existing ExecutionRouter remains the sole routing authority. This
    operation only prepares schema context; it never invokes a tool and never
    mutates canonical memory.
    """
    return execution_router.search_tool_schemas(query, tool_schemas, limit=limit)
