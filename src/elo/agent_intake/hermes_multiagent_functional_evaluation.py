"""Candidate-specific functional evaluation for EXT-MULTIAGENT-HERMES.

Measures whether bounded delegation prevents cross-task context contamination.
No child agent is spawned and no execution authority is granted.
"""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_multiagent_adapter import adapt_delegation
from .hermes_multiagent_boundary import DelegationSignal

@dataclass(frozen=True, slots=True)
class MultiagentFunctionalEvidence:
    baseline_context_isolation_rate: float
    adapted_context_isolation_rate: float
    repeatable: bool
    boundary_integrity: bool
    provenance_refs: tuple[str, ...]

def _signals(prefix: str) -> tuple[DelegationSignal, ...]:
    return tuple(
        DelegationSignal(
            delegation_id=f"{prefix}-{i}",
            tenant_scope="multiteiner",
            parent_agent_id="elo",
            child_agent_id=f"worker-{i}",
            goal_digest=f"goal-{i}",
            source_refs=(f"controlled-eval:multiagent-functional/{prefix.lower()}/{i}",),
            resource_scope=(f"task:{i}", "read-only"),
            provenance_verified=True,
            isolated_context=True,
        )
        for i in (1, 2)
    )

def _baseline(signals: tuple[DelegationSignal, ...]) -> float:
    # Baseline models the failure mode: both delegated tasks observe one shared context.
    contexts = ("shared-context", "shared-context")
    return float(len(set(contexts)) == len(signals))

def _adapted(signals: tuple[DelegationSignal, ...]) -> float:
    items = tuple(adapt_delegation(signal) for signal in signals)
    contexts = tuple(
        f"{item.tenant_scope}:{item.delegation_id}:{item.resource_scope}"
        for item in items if item is not None
    )
    return float(
        len(items) == len(signals)
        and len(set(contexts)) == len(signals)
        and all(item.isolated_context and not item.child_authority for item in items if item is not None)
    )

def evaluate_multiagent_functional_gain() -> MultiagentFunctionalEvidence:
    baseline = _signals("BASELINE")
    adapted = _signals("HERMES")
    baseline_rate = _baseline(baseline)
    adapted_rate = _adapted(adapted)
    repeatable = _adapted(_signals("REPEAT")) == adapted_rate
    items = tuple(adapt_delegation(signal) for signal in adapted)
    boundary = all(
        item is not None and item.isolated_context
        and not item.child_authority and not item.promotion_permitted
        for item in items
    )
    refs = tuple(ref for signal in adapted for ref in signal.source_refs)
    return MultiagentFunctionalEvidence(
        baseline_rate, adapted_rate, repeatable, boundary, refs
    )
