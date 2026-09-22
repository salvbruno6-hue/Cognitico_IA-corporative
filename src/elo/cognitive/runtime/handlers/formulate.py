"""FORMULATE — monta o decision_brief com o delta de síntese.

Refs: ADR-0014.
"""
from __future__ import annotations

from ..crl import CRLContext
from ..store.memory_store import DecisionStore


def formulate_handler(ctx: CRLContext) -> CRLContext:
    delta = ctx.stage_results.get("delta")
    delta_dict = (
        delta.to_dict() if delta is not None
        else ctx.stage_results.get("analysis", {})
    )

    brief = {
        "problem": ctx.payload.get("question") or ctx.payload.get("so_id"),
        "so_id": ctx.payload.get("so_id"),
        "evidence": list(ctx.payload.get("evidence_ids", ())),
        "aligned": delta_dict.get("aligned", []),
        "improvements": delta_dict.get("improvements", []),
        "corrections": delta_dict.get("corrections", []),
        "conflicts": delta_dict.get("conflicts", []),
        "precedents_used": delta_dict.get("precedents_used", []),
        "handbook_used": delta_dict.get("handbook_used", []),
        "confidence": delta_dict.get("overall_confidence", 0.0),
        "recommendation": _build_recommendation(delta_dict),
    }

    ctx.stage_results["decision_brief"] = brief

    lifecycle = ctx.stage_results.get("lifecycle")
    if lifecycle is not None:
        DecisionStore().save(lifecycle)
    return ctx


def _build_recommendation(delta: dict) -> str:
    if delta.get("conflicts"):
        return "escalar_humano_conflito_politica"
    if delta.get("corrections"):
        return "corrigir_e_revalidar"
    if delta.get("improvements"):
        return "considerar_melhorias"
    if delta.get("aligned"):
        return "alinhado_prosseguir"
    return "sem_delta_significativo"
