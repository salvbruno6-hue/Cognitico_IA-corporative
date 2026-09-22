"""ANALYZE — aplica regras do cânone ao contexto."""
from __future__ import annotations
from ..crl import CRLContext

def analyze_handler(ctx: CRLContext) -> CRLContext:
    precedents = ctx.stage_results.get("precedents", ())
    ctx.stage_results["analysis"] = {"precedent_count": len(precedents), "domain": ctx.payload.get("domain"), "sector": ctx.payload.get("sector")}
    return ctx
