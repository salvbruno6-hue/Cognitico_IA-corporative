"""Controlled, side-effect-free measurement for the Hermes tool-search candidate.

This measures representation footprint only. It does not invoke Hermes, tools,
MCP, memory, or business operations. A positive footprint result is evidence
for further evaluation, not a promotion decision.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ToolSearchFootprint:
    eager_chars: int
    progressive_chars: int
    reduction_chars: int
    reduction_ratio: float
    selected_tool_present: bool


def measure_footprint(
    *,
    eager_schemas: tuple[str, ...],
    deferred_schemas: tuple[str, ...],
    selected_tool_schema: str,
) -> ToolSearchFootprint:
    eager_chars = sum(len(schema) for schema in eager_schemas)
    progressive_catalog_chars = sum(len(schema) for schema in deferred_schemas)
    progressive_chars = progressive_catalog_chars + len(selected_tool_schema)
    reduction_chars = eager_chars - progressive_chars
    reduction_ratio = reduction_chars / eager_chars if eager_chars else 0.0
    selected_tool_present = selected_tool_schema in deferred_schemas
    return ToolSearchFootprint(
        eager_chars=eager_chars,
        progressive_chars=progressive_chars,
        reduction_chars=reduction_chars,
        reduction_ratio=reduction_ratio,
        selected_tool_present=selected_tool_present,
    )


__all__ = ["ToolSearchFootprint", "measure_footprint"]
