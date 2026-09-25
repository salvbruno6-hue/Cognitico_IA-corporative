"""Operational outcome evidence adapter for progressive tool-schema disclosure.

This module does not execute tools or persist learning. It maps an already
verified runtime observation into the existing PerformanceEvidence contract.
"""
from __future__ import annotations

from elo.cognitive.learning.performance_evidence import PerformanceEvidence
from elo.cognitive.routing.tool_search import ToolSchemaSelection


def build_tool_search_performance_evidence(
    *,
    tenant_id: str,
    context_key: str,
    selection: ToolSchemaSelection,
    quality: float,
    reliability: float,
    latency_ms: float,
    cost: float,
    provenance: str,
) -> PerformanceEvidence:
    """Convert a verified operational observation into canonical evidence.

    The caller must supply measurements from an actual runtime observation.
    This function never executes a tool, fabricates measurements, persists
    memory, or authorizes promotion.
    """
    if not selection.bounded:
        raise ValueError("tool-schema selection must be bounded")
    if selection.canonical_mutation:
        raise ValueError("canonical mutation is not valid for performance evidence")

    evidence = PerformanceEvidence(
        tenant_id=tenant_id,
        capability="Progressive Tool Schema Disclosure",
        context_key=context_key,
        model_id=None,
        tool_id=None,
        verified=True,
        quality=quality,
        reliability=reliability,
        latency_ms=latency_ms,
        cost=cost,
        provenance=provenance,
    )
    evidence.validate()
    return evidence
