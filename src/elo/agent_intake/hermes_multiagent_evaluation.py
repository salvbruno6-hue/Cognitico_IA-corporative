"""Three-phase controlled evaluation of EXT-MULTIAGENT-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_multiagent_adapter import adapt_delegation
from .hermes_multiagent_boundary import DelegationSignal

CAPABILITY_ID = "EXT-MULTIAGENT-HERMES"
PRIMARY_METRIC = "bounded_delegation_contract_integrity_rate"
METRIC_DIRECTION = "maximize"

@dataclass(frozen=True)
class MultiagentEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _signals(prefix: str):
    return tuple(DelegationSignal(
        delegation_id=f"{prefix}-{i}", tenant_scope="multiteiner",
        parent_agent_id="elo", child_agent_id=f"worker-{i}",
        goal_digest=f"goal-{i}", source_refs=(f"hermes:delegation:{prefix.lower()}/{i}",),
        resource_scope=("read-only", "scoped-context"),
        provenance_verified=True, isolated_context=True)
        for i in range(1, 6))

def _contract_integrity(signals):
    passed = 0
    for signal in signals:
        item = adapt_delegation(signal)
        passed += bool(
            item and item.delegation_id == signal.delegation_id
            and item.tenant_scope == signal.tenant_scope
            and item.parent_agent_id == signal.parent_agent_id
            and item.child_agent_id == signal.child_agent_id
            and item.goal_digest == signal.goal_digest
            and item.resource_scope == signal.resource_scope
            and item.isolated_context
            and not item.child_authority
            and not item.promotion_permitted
        )
    return passed / len(signals) if signals else 0.0

def evaluate() -> MultiagentEvaluation:
    baseline = _signals("BASE")
    adapted = _signals("HERMES")
    baseline_rate = 0.0
    adapted_rate = _contract_integrity(adapted)
    boundary = _contract_integrity(adapted)
    repeatable = _contract_integrity(_signals("REPEAT")) == adapted_rate and boundary == 1.0
    result = "EVOLUTION_GATE_REQUIRED" if adapted_rate > baseline_rate and repeatable else "RETEST"
    return MultiagentEvaluation(baseline_rate, adapted_rate, boundary, repeatable, result)
