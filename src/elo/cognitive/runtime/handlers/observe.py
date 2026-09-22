"""OBSERVE — cria a DecisionLifecycle a partir da pergunta."""
from __future__ import annotations
from elo.core.decision_outcome_loop import DecisionLifecycle
from elo.core.systemic_primitives import DecisionRecord
from ..crl import CRLContext
from ..store.memory_store import DecisionStore
from .base import require

def observe_handler(ctx: CRLContext) -> CRLContext:
    question = require(ctx, "question")
    decision_id = ctx.payload.get("decision_id", f"DEC_{ctx.request_id}")
    record = DecisionRecord(
        decision_id=decision_id,
        decision=question,
        rationale=ctx.payload.get("rationale", "runtime observed request"),
        impact=tuple(ctx.payload.get("impact", ())),
        evidence_ids=tuple(ctx.payload.get("evidence_ids", ())),
        authority=ctx.payload.get("authority"),
        expected_outcome=ctx.payload.get("expected_outcome"),
    )
    lifecycle = DecisionLifecycle(record)
    DecisionStore().save(lifecycle)
    ctx.stage_results["lifecycle"] = lifecycle
    ctx.stage_results["decision_id"] = decision_id
    return ctx
