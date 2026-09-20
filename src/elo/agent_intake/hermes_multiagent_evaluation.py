"""Controlled evaluation of Hermes multi-agent delegation boundary."""
from __future__ import annotations
from dataclasses import dataclass

from .hermes_multiagent_boundary import (
    DelegationDisposition,
    DelegationSignal,
    assess_delegation,
)

CAPABILITY_ID = "EXT-MULTIAGENT-HERMES"
PRIMARY_METRIC = "valid_delegation_recognition_rate"
METRIC_DIRECTION = "maximize"

@dataclass(frozen=True)
class MultiagentEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _signals(prefix: str):
    return tuple(
        DelegationSignal(
            delegation_id=f"{prefix}-{i}",
            tenant_scope="multiteiner",
            parent_agent_id="elo",
            child_agent_id=f"worker-{i}",
            goal_digest=f"goal-{i}",
            source_refs=(f"hermes:delegation:{prefix.lower()}/{i}",),
            provenance_verified=True,
            isolated_context=True,
        )
        for i in range(1, 6)
    )

def _recognition_rate(signals):
    return sum(
        assess_delegation(s).disposition is DelegationDisposition.CANDIDATE
        for s in signals
    ) / len(signals)

def _boundary_integrity_rate(signals):
    return sum(
        (a := assess_delegation(s)).canonical_authority is False
        and a.execution_permitted is False
        and a.promotion_permitted is False
        for s in signals
    ) / len(signals)

def evaluate() -> MultiagentEvaluation:
    baseline = _signals("BASE")
    adapted = _signals("HERMES")
    baseline_rate = _recognition_rate(baseline)
    adapted_rate = _recognition_rate(adapted)
    integrity = _boundary_integrity_rate(adapted)
    repeatable = _recognition_rate(_signals("REPEAT")) == adapted_rate and integrity == 1.0
    result = "EVOLUTION_GATE_REQUIRED" if adapted_rate > baseline_rate and repeatable else "RETEST"
    return MultiagentEvaluation(baseline_rate, adapted_rate, integrity, repeatable, result)
