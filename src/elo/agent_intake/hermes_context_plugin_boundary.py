"""Candidate-only boundary for Hermes context-engine plugins."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

CAPABILITY_ID = "EXT-CONTEXT-PLUGIN-HERMES"

class PluginDisposition(str, Enum):
    OBSERVATION = "OBSERVATION"
    CANDIDATE = "CANDIDATE"
    REJECTED = "REJECTED"

@dataclass(frozen=True)
class ContextEnginePluginSignal:
    signal_id: str
    tenant_scope: str
    plugin_id: str
    engine_name: str
    source_refs: Tuple[str, ...]
    explicit_activation: bool = False
    exclusive_provider: bool = True
    lifecycle_events: Tuple[str, ...] = ()
    provenance_verified: bool = False

@dataclass(frozen=True)
class ContextEnginePluginAssessment:
    signal_id: str
    plugin_id: str
    disposition: PluginDisposition
    evidence_refs: Tuple[str, ...]
    canonical_authority: bool = False
    activation_permitted: bool = False

def assess_context_engine_plugin(signal: ContextEnginePluginSignal) -> ContextEnginePluginAssessment:
    if not signal.signal_id or not signal.tenant_scope or not signal.plugin_id or not signal.engine_name:
        return ContextEnginePluginAssessment(signal.signal_id, signal.plugin_id, PluginDisposition.REJECTED, tuple(signal.source_refs))
    if not signal.source_refs or not signal.provenance_verified:
        return ContextEnginePluginAssessment(signal.signal_id, signal.plugin_id, PluginDisposition.REJECTED, tuple(signal.source_refs))
    if not signal.explicit_activation:
        return ContextEnginePluginAssessment(signal.signal_id, signal.plugin_id, PluginDisposition.OBSERVATION, tuple(signal.source_refs))
    return ContextEnginePluginAssessment(signal.signal_id, signal.plugin_id, PluginDisposition.CANDIDATE, tuple(signal.source_refs))
