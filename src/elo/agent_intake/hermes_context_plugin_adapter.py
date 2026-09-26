"""Bounded Hermes context-plugin adapter for controlled ELO evaluation.

The adapter enriches an existing ContextPack with a verified plugin source.
It never becomes context authority, does not activate an external runtime,
and cannot promote or mutate canonical state.
"""
from __future__ import annotations

from dataclasses import dataclass

from elo.core.context_resolution import ContextPack, ContextResolutionEngine, ContextSource

from .hermes_context_plugin_boundary import (
    ContextEnginePluginAssessment,
    ContextEnginePluginSignal,
    PluginDisposition,
    assess_context_engine_plugin,
)

@dataclass(frozen=True)
class ContextPluginAdapterResult:
    pack: ContextPack
    assessment: ContextEnginePluginAssessment
    adapted: bool

class ContextPluginAdapter:
    """Adapt verified plugin metadata into the existing ELO Context pack."""

    def __init__(self, engine: ContextResolutionEngine | None = None) -> None:
        self._engine = engine or ContextResolutionEngine()

    def adapt(
        self,
        pack: ContextPack,
        signal: ContextEnginePluginSignal,
    ) -> ContextPluginAdapterResult:
        assessment = assess_context_engine_plugin(signal)
        if assessment.disposition is not PluginDisposition.CANDIDATE:
            return ContextPluginAdapterResult(pack, assessment, False)

        source = ContextSource(
            source_id=f"hermes-plugin:{signal.plugin_id}:{signal.signal_id}",
            source_type="context-plugin",
            authority="ELO Context",
            tenant_id=signal.tenant_scope,
            domain=pack.query.domain,
            provenance={
                "plugin_id": signal.plugin_id,
                "engine_name": signal.engine_name,
                "source_refs": ",".join(signal.source_refs),
                "activation": "explicit",
                "provenance_verified": "true",
            },
        )
        adapted_pack = self._engine.enrich(
            pack,
            sources=(source,),
            uncertainties=("plugin adapter evidence is controlled evaluation only",),
        )
        return ContextPluginAdapterResult(adapted_pack, assessment, True)

__all__ = ["ContextPluginAdapter", "ContextPluginAdapterResult"]
