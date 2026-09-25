"""Evidence adapters for progressive tool-schema disclosure.

The indirect adapter allows a validated downstream capability or experience
to corroborate the evaluated skill without requiring the skill itself to own
production traffic. It reuses PerformanceEvidence and does not create a new
evidence, learning, routing, or promotion authority.
"""

from __future__ import annotations

from elo.cognitive.learning.performance_evidence import PerformanceEvidence
from elo.cognitive.routing.tool_search import ToolSchemaSelection


CAPABILITY = "Progressive Tool Schema Disclosure"


def _validate_selection(selection: ToolSchemaSelection) -> None:
    if not selection.bounded:
        raise ValueError("tool-schema selection must be bounded")
    if selection.canonical_mutation:
        raise ValueError("canonical mutation is not valid for performance evidence")


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
    """Convert a verified direct operational observation into evidence."""
    _validate_selection(selection)

    evidence = PerformanceEvidence(
        tenant_id=tenant_id,
        capability=CAPABILITY,
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


def build_tool_search_indirect_performance_evidence(
    *,
    tenant_id: str,
    context_key: str,
    selection: ToolSchemaSelection,
    observer_capability: str,
    experience_ref: str,
    expected_outcome: str,
    observed_outcome: str,
    relationship: str,
    quality: float,
    reliability: float,
    latency_ms: float,
    cost: float,
) -> PerformanceEvidence:
    """Corroborate the skill through an already validated capability experience.

    The observer capability supplies the observed result; this adapter only
    attributes that observation to the evaluated skill when the caller
    explicitly supplies the relationship and experience reference. It does
    not infer causality, execute tools, persist learning, or authorize
    promotion.
    """
    _validate_selection(selection)

    required = (
        observer_capability,
        experience_ref,
        expected_outcome,
        observed_outcome,
        relationship,
    )
    if not all(value.strip() for value in required):
        raise ValueError("indirect evidence requires observer, experience, outcomes and relationship")

    provenance = (
        f"mode=INDIRECT_EXPERIENCE;"
        f"observer_capability={observer_capability.strip()};"
        f"experience_ref={experience_ref.strip()};"
        f"relationship={relationship.strip()};"
        f"expected_outcome={expected_outcome.strip()};"
        f"observed_outcome={observed_outcome.strip()}"
    )

    evidence = PerformanceEvidence(
        tenant_id=tenant_id,
        capability=CAPABILITY,
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
