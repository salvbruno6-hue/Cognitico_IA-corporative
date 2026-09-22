"""DECIDE — avança o ciclo para APPROVED."""
from __future__ import annotations
from elo.core.decision_outcome_loop import DecisionState
from ..crl import CRLContext
from ..store.memory_store import DecisionStore
from .base import require

def decide_handler(ctx: CRLContext) -> CRLContext:
    lifecycle = require(ctx, "lifecycle")
    lifecycle.transition(DecisionState.APPROVED, evidence_ids=tuple(ctx.payload.get("evidence_ids", ())), actor=ctx.payload.get("approver"))
    DecisionStore().save(lifecycle)
    ctx.stage_results["lifecycle"] = lifecycle
    return ctx
