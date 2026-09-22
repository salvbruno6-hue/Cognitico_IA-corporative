"""MONITOR — avança para OBSERVING e, se houver outcome, para EVALUATED + ATTRIBUTED."""
from __future__ import annotations
from elo.core.decision_outcome_loop import DecisionState
from elo.core.systemic_primitives import OutcomeFeedback
from ..crl import CRLContext
from ..store.memory_store import DecisionStore
from .base import require

def monitor_handler(ctx: CRLContext) -> CRLContext:
    lifecycle = require(ctx, "lifecycle")
    evidence_ids = tuple(ctx.payload.get("evidence_ids", ()))
    lifecycle.transition(DecisionState.OBSERVING)
    DecisionStore().save(lifecycle)
    outcome_data = ctx.payload.get("outcome")
    if outcome_data:
        outcome = OutcomeFeedback(decision_id=lifecycle.decision.decision_id, expected=outcome_data["expected"], observed=outcome_data["observed"], variance=outcome_data.get("variance"), evidence_ids=tuple(outcome_data.get("evidence_ids", evidence_ids)))
        lifecycle.attach_outcome(outcome)
        lifecycle.transition(DecisionState.EVALUATED, evidence_ids=evidence_ids)
        DecisionStore().save(lifecycle)
    attribution = ctx.payload.get("attribution")
    if attribution:
        lifecycle.attach_attribution(attribution)
        lifecycle.transition(DecisionState.ATTRIBUTED, evidence_ids=evidence_ids)
        DecisionStore().save(lifecycle)
    ctx.stage_results["lifecycle"] = lifecycle
    return ctx
