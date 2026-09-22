"""EXECUTE — avança o ciclo para EXECUTED."""
from __future__ import annotations
from elo.core.decision_outcome_loop import DecisionState
from ..crl import CRLContext
from ..store.memory_store import DecisionStore
from .base import require

def execute_handler(ctx: CRLContext) -> CRLContext:
    lifecycle = require(ctx, "lifecycle")
    lifecycle.transition(DecisionState.EXECUTED)
    DecisionStore().save(lifecycle)
    ctx.stage_results["lifecycle"] = lifecycle
    return ctx
