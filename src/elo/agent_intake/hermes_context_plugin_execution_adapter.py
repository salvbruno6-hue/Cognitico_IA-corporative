"""Governed execution adapter for the EXT-CONTEXT-PLUGIN-HERMES candidate.

This module does not authorize, promote, persist learning, or replace ELO Context.
It executes the existing bounded Hermes context-plugin behavior only through the
canonical ExecutionBoundary.
"""
from __future__ import annotations
from collections.abc import Mapping
from dataclasses import dataclass
from elo.core.context_resolution import ContextQuery, ContextResolutionEngine
from elo.core.execution_boundary import ExecutionAdapter, ExecutionOutcome, ExecutionRequest, execute_governed
from elo.agent_intake.hermes_context_plugin_adapter import ContextPluginAdapter
from elo.agent_intake.hermes_context_plugin_boundary import ContextEnginePluginSignal

@dataclass(frozen=True)
class ContextPluginExecutionResult:
    outcome: ExecutionOutcome
    adapted: bool
    signal_id: str
    plugin_id: str
    canonical_authority: bool

class ContextPluginExecutionAdapter(ExecutionAdapter):
    """Execute one already-authorized Hermes context-plugin operation."""
    def __init__(self, *, signal: ContextEnginePluginSignal,
                 context_engine: ContextResolutionEngine | None = None,
                 question: str) -> None:
        self.signal = signal
        self.context_engine = context_engine or ContextResolutionEngine()
        self.question = question.strip()

    def execute(self, request: ExecutionRequest) -> Mapping[str, str]:
        if request.action_id != "EXT-CONTEXT-PLUGIN-HERMES":
            raise ValueError("unsupported_execution_action")
        if not self.question:
            raise ValueError("context_question_required")
        query = ContextQuery(
            question=self.question,
            tenant_id=request.tenant_id,
            domain="planning",
            request_id=request.request_id,
            correlation_id=request.correlation_id,
            principal_id=request.principal_id,
        )
        pack = self.context_engine.resolve(query)
        result = ContextPluginAdapter(self.context_engine).adapt(pack, self.signal)
        if not result.adapted:
            raise ValueError(
                f"context_plugin_not_adapted:{result.assessment.disposition.value}"
            )
        return {
            "execution_entrypoint": "elo.context.resolve",
            "context_plugin_adapted": "true",
            "context_plugin_signal_id": self.signal.signal_id,
            "context_plugin_id": self.signal.plugin_id,
            "canonical_context_authority": str(result.assessment.canonical_authority).lower(),
            "context_source_count": str(len(result.pack.scoped_sources())),
        }

def execute_context_plugin(request: ExecutionRequest, *,
                           signal: ContextEnginePluginSignal,
                           question: str,
                           context_engine: ContextResolutionEngine | None = None
                           ) -> ContextPluginExecutionResult:
    """Execute the candidate through the canonical governed execution boundary."""
    adapter = ContextPluginExecutionAdapter(
        signal=signal, context_engine=context_engine, question=question
    )
    outcome = execute_governed(request, adapter)
    provenance = dict(outcome.provenance)
    return ContextPluginExecutionResult(
        outcome=outcome,
        adapted=provenance.get("context_plugin_adapted") == "true",
        signal_id=signal.signal_id,
        plugin_id=signal.plugin_id,
        canonical_authority=provenance.get("canonical_context_authority") == "true",
    )

__all__ = ["ContextPluginExecutionAdapter", "ContextPluginExecutionResult", "execute_context_plugin"]
