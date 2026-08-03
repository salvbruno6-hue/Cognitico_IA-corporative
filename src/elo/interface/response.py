"""Canonical cognitive response builder for the ELO interface."""

from __future__ import annotations

from time import perf_counter
from typing import Any

from .contracts import (
    AgentReference,
    CognitiveRequest,
    CognitiveResponse,
    Provenance,
    SourceReference,
    SuggestedAction,
)


class ResponseBuilder:
    """Builds interface responses from governed cognitive-core results."""

    @staticmethod
    def _confidence(result: dict[str, Any]) -> float:
        try:
            value = float(result.get("confidence", 0.0))
        except (TypeError, ValueError):
            value = 0.0
        return max(0.0, min(1.0, value))

    @staticmethod
    def _sources(result: dict[str, Any]) -> list[SourceReference]:
        sources: list[SourceReference] = []
        for index, item in enumerate(result.get("sources", []) or []):
            if isinstance(item, SourceReference):
                sources.append(item)
            elif isinstance(item, dict):
                payload = dict(item)
                payload.setdefault("source_id", str(payload.get("id", index)))
                payload.setdefault("source_type", "knowledge")
                sources.append(SourceReference.model_validate(payload))
            else:
                sources.append(
                    SourceReference(
                        source_id=str(index),
                        source_type="knowledge",
                        title=str(item),
                    )
                )
        return sources

    @staticmethod
    def _agents(result: dict[str, Any]) -> list[AgentReference]:
        agents: list[AgentReference] = []
        for item in result.get("agents_used", []) or []:
            if isinstance(item, AgentReference):
                agents.append(item)
            elif isinstance(item, dict):
                agents.append(AgentReference.model_validate(item))
            else:
                agents.append(AgentReference(agent_id=str(item)))
        return agents

    @staticmethod
    def _suggestions(result: dict[str, Any]) -> list[SuggestedAction]:
        suggestions: list[SuggestedAction] = []
        for item in result.get("suggestions", []) or []:
            if isinstance(item, SuggestedAction):
                suggestions.append(item)
            elif isinstance(item, dict):
                suggestions.append(SuggestedAction.model_validate(item))
            else:
                suggestions.append(SuggestedAction(label=str(item)))
        return suggestions

    def build(
        self,
        request: CognitiveRequest,
        session_id: str,
        result: dict[str, Any],
        *,
        started_at: float | None = None,
    ) -> CognitiveResponse:
        response_payload = result.get("response")
        if not isinstance(response_payload, dict):
            response_payload = {
                "type": result.get("type", "analysis"),
                "content": response_payload if response_payload is not None else result.get("content", ""),
                "analysis": result.get("analysis"),
                "decision": result.get("decision"),
                "risks": result.get("risks", []),
                "opportunities": result.get("opportunities", []),
                "actions": result.get("actions", []),
            }
            response_payload = {k: v for k, v in response_payload.items() if v not in (None, [], "")}

        provenance_data = result.get("provenance", {}) or {}
        provenance = Provenance(
            request_id=request.request_id,
            provider=provenance_data.get("provider"),
            model=provenance_data.get("model"),
            evidence_refs=list(provenance_data.get("evidence_refs", [])),
            policy_decision=provenance_data.get("policy_decision"),
            validation_status=provenance_data.get("validation_status"),
            metadata=dict(provenance_data.get("metadata", {})),
        )

        elapsed_ms = 0.0
        if started_at is not None:
            elapsed_ms = max(0.0, (perf_counter() - started_at) * 1000.0)

        return CognitiveResponse(
            request_id=request.request_id,
            session_id=session_id,
            domain=request.domain or result.get("domain"),
            response=response_payload,
            sources=self._sources(result),
            agents_used=self._agents(result),
            confidence=self._confidence(result),
            provenance=provenance,
            suggestions=self._suggestions(result),
            processing_time_ms=elapsed_ms,
        )
