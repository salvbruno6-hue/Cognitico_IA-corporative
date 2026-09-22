"""LEARN — Symbiont obrigatório (ADR-0015)."""
from __future__ import annotations
from elo.core.decision_outcome_loop import DecisionState
from ..crl import CRLContext
from ..store.memory_store import DecisionStore
from .base import require

def learn_handler(ctx: CRLContext) -> CRLContext:
    lifecycle = require(ctx, "lifecycle")
    evidence_ids = tuple(ctx.payload.get("evidence_ids", ()))
    adapter = ctx.payload.get("symbiont_adapter")
    observation = ctx.payload.get("symbiont_observation")
    if adapter is None or observation is None:
        lifecycle.transition(DecisionState.ESCALATED, evidence_ids=evidence_ids)
        DecisionStore().save(lifecycle)
        ctx.stage_results["lifecycle"] = lifecycle
        ctx.stage_results["escalation"] = {"stage": "learn", "reason": "symbiont_required_for_learning"}
        return ctx
    evaluation = lifecycle.handoff_to_symbiont(adapter=adapter, observation=observation, principal_id=require(ctx, "principal_id"), dataset_version=require(ctx, "dataset_version"))
    DecisionStore().save(lifecycle)
    ctx.stage_results["lifecycle"] = lifecycle
    ctx.stage_results["symbiont_evaluation"] = evaluation
    return ctx
