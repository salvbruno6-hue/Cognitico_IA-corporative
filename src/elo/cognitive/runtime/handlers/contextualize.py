"""CONTEXTUALIZE — enriquece o contexto com conhecimento do ELO.

Refs: ADR-0014, ELO-SO-DOSSIER-PROTOCOL.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from elo.agent_intake.hermes_context_plugin_adapter import ContextPluginAdapter
from elo.agent_intake.hermes_context_plugin_boundary import ContextEnginePluginSignal
from elo.core.context_resolution import ContextQuery, ContextResolutionEngine

from ..crl import CRLContext
from ..knowledge.so_resolver import SOResolver
from ..store.memory_store import PrecedentStore


def _apply_hermes_context_plugin(ctx: CRLContext, *, tenant_id: str | None, domain: str) -> None:
    """Optionally enrich the real Context runtime with an explicitly activated Hermes signal.

    The existing ELO Context path remains the default. Hermes supplies only a
    bounded candidate signal; ContextResolutionEngine remains the authority.
    """
    raw = ctx.payload.get("hermes_context_plugin")
    if raw is None:
        return
    if not isinstance(raw, Mapping):
        raise ValueError("hermes_context_plugin must be a mapping")
    if not tenant_id:
        raise ValueError("tenant_id is required for Hermes context-plugin runtime")

    signal = ContextEnginePluginSignal(
        signal_id=str(raw.get("signal_id", "")),
        tenant_scope=str(raw.get("tenant_scope", "")),
        plugin_id=str(raw.get("plugin_id", "")),
        engine_name=str(raw.get("engine_name", "")),
        source_refs=tuple(str(item) for item in (raw.get("source_refs", ()) or ())),
        explicit_activation=bool(raw.get("explicit_activation", False)),
        exclusive_provider=bool(raw.get("exclusive_provider", True)),
        lifecycle_events=tuple(str(item) for item in (raw.get("lifecycle_events", ()) or ())),
        provenance_verified=bool(raw.get("provenance_verified", False)),
    )

    if signal.tenant_scope != tenant_id:
        raise ValueError("Hermes context-plugin tenant does not match ELO context tenant")

    question = str(
        ctx.payload.get("context_question")
        or ctx.payload.get("intent")
        or ctx.request_id
    ).strip()
    if not question:
        raise ValueError("context question is required for Hermes context-plugin runtime")

    engine = ContextResolutionEngine()
    pack = engine.resolve(
        ContextQuery(
            question=question,
            tenant_id=tenant_id,
            domain=domain,
            request_id=ctx.request_id,
            correlation_id=str(ctx.payload.get("correlation_id") or ctx.request_id),
        )
    )
    result = ContextPluginAdapter(engine).adapt(pack, signal)
    ctx.stage_results["hermes_context_plugin"] = {
        "signal_id": signal.signal_id,
        "plugin_id": signal.plugin_id,
        "adapted": result.adapted,
        "disposition": result.assessment.disposition.value,
        "evidence_refs": result.assessment.evidence_refs,
        "canonical_authority": result.assessment.canonical_authority,
    }
    if result.adapted:
        ctx.stage_results["hermes_context_pack"] = result.pack


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

    _apply_hermes_context_plugin(ctx, tenant_id=tenant_id, domain=domain)
    return ctx
