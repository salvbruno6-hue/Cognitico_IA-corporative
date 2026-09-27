"""CONTEXTUALIZE — enriquece o contexto com conhecimento do ELO.

Refs: ADR-0014, ELO-SO-DOSSIER-PROTOCOL.
"""
from __future__ import annotations

from ..crl import CRLContext
from ..knowledge.so_resolver import SOResolver
from ..store.memory_store import PrecedentStore


def contextualize_handler(ctx: CRLContext) -> CRLContext:
    so_id = ctx.payload.get("so_id")
    domain = ctx.payload.get("domain", "orcamento")
    tenant_id = ctx.payload.get("tenant_id")
    context_keys = tuple(ctx.payload.get("context_keys", ()))

    if so_id:
        resolver = SOResolver()
        so_context = resolver.resolve(
            so_id,
            tenant_id=tenant_id,
            domain=domain,
        )
        ctx.stage_results["so_context"] = so_context
        ctx.stage_results["so_dossier"] = so_context["dossier"]
        ctx.stage_results["precedents"] = so_context["precedents"]
        ctx.stage_results["context_keys_resolved"] = so_context["context_keys"]
    else:
        index = PrecedentStore().load()
        precedents = index.find(
            domain=domain,
            context_keys=context_keys,
            limit=ctx.payload.get("precedent_limit", 10),
        )
        ctx.stage_results["precedents"] = [
            {
                "decision_id": p.decision_id,
                "domain": p.domain,
                "outcome_summary": p.outcome_summary,
                "context_keys": list(p.context_keys),
            }
            for p in precedents
            if tenant_id is None or getattr(p, "tenant_id", tenant_id) == tenant_id
        ]

    return ctx
