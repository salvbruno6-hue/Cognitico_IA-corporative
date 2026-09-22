"""ANALYZE — sintetiza análise externa contra contexto ELO.

Refs: ADR-0014.
"""
from __future__ import annotations

from ..crl import CRLContext
from ..synthesis.engine import SynthesisEngine
from ..store.memory_store import DecisionStore


def analyze_handler(ctx: CRLContext) -> CRLContext:
    external_analysis = ctx.payload.get("chatgpt_analysis", "")
    so_context = ctx.stage_results.get("so_context") or {}

    engine = SynthesisEngine()
    delta = engine.synthesize(
        external_analysis=external_analysis,
        so_context=so_context,
    )

    ctx.stage_results["analysis"] = delta.to_dict()
    ctx.stage_results["delta"] = delta

    lifecycle = ctx.stage_results.get("lifecycle")
    if lifecycle is not None:
        DecisionStore().save_analysis(
            decision_id=lifecycle.decision.decision_id,
            external_analysis=external_analysis,
            delta=delta.to_dict(),
        )

    return ctx
