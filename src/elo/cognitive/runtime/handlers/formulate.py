"""FORMULATE — monta o decision_brief no contexto."""
from __future__ import annotations
from ..crl import CRLContext
from ..store.memory_store import DecisionStore

def formulate_handler(ctx: CRLContext) -> CRLContext:
    brief = {"problem": ctx.payload.get("question"), "evidence": list(ctx.payload.get("evidence_ids", ())), "alternatives": ctx.payload.get("alternatives", []), "recommendation": ctx.payload.get("recommendation"), "confidence": ctx.payload.get("confidence", 0.0), "risks": ctx.payload.get("risks", [])}
    ctx.stage_results["decision_brief"] = brief
    lifecycle = ctx.stage_results.get("lifecycle")
    if lifecycle is not None: DecisionStore().save(lifecycle)
    return ctx
