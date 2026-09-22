"""CONTEXTUALIZE — busca precedentes similares."""
from __future__ import annotations
from ..crl import CRLContext
from ..store.memory_store import PrecedentStore
from .base import require

def contextualize_handler(ctx: CRLContext) -> CRLContext:
    domain = require(ctx, "domain")
    context_keys = tuple(ctx.payload.get("context_keys", ()))
    index = PrecedentStore().load()
    precedents = index.find(domain=domain, context_keys=context_keys, limit=ctx.payload.get("precedent_limit", 10))
    ctx.stage_results["precedents"] = precedents
    return ctx
