"""FOLLOW-UP — indexa precedente se ciclo fechado."""
from __future__ import annotations
from elo.core.decision_outcome_loop import DecisionState
from ..crl import CRLContext
from ..store.memory_store import PrecedentStore
from .base import require

def follow_up_handler(ctx: CRLContext) -> CRLContext:
    lifecycle = require(ctx, "lifecycle")
    if lifecycle.state != DecisionState.CLOSED: return ctx
    index = PrecedentStore().load()
    index.add(lifecycle, domain=require(ctx, "domain"), context_keys=tuple(ctx.payload.get("context_keys", ())), outcome_summary=ctx.payload.get("outcome_summary", "closed"))
    PrecedentStore().save(index)
    return ctx
