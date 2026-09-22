"""Canonical CognitiveCore implementation for the ELO prototype."""

from __future__ import annotations

import os
from typing import Any

from elo.interface.contracts import CognitiveRequest

from .agents.hermes_contract import HermesExecutionRequest
from elo.core.interaction_runtime import build_interaction
from elo.core.temporal_memory import TemporalConversationMemory
from .symbiont_hermes_bridge import SymbiontHermesBridge


_RUNTIME_PROBE_MISSION = "runtime_probe"
_RUNTIME_PROBE_CAPABILITY = "hermes:runtime_probe"


class CognitiveCore:
    """Canonical cognitive core with governed conversational behavior."""

    def __init__(
        self,
        *,
        hermes_bridge: SymbiontHermesBridge | None = None,
        temporal_memory: TemporalConversationMemory | None = None,
    ) -> None:
        self._hermes_bridge = hermes_bridge or SymbiontHermesBridge()
        self._temporal_memory = temporal_memory or TemporalConversationMemory()

    def process(self, request: CognitiveRequest) -> dict[str, Any]:
        if not request.tenant_id:
            raise ValueError("tenant_id is required")

        hermes_result = self._maybe_execute_hermes(request)
        if hermes_result is not None:
            return {
                "response": {
                    "type": "hermes_execution",
                    "content": hermes_result.result.outcome,
                    "status": hermes_result.result.status,
                },
                "confidence": 1.0,
                "domain": request.domain,
                "hermes": hermes_result.result.to_dict(),
                "provenance": {
                    "request_id": request.request_id,
                    "correlation_id": request.correlation_id,
                    "tenant_id": request.tenant_id,
                    "domain": request.domain,
                    "principal_id": request.principal_id,
                    "provider": "elo-hermes-via-symbiont",
                    "evidence_refs": [request.request_id],
                    "policy_decision": "ALLOW",
                    "validation_status": "evidence_validated",
                },
            }

        context = dict(request.context)
        context.setdefault("session_id", request.session_id)
        context.setdefault("conversation_id", context.get("conversation_id") or request.session_id)

        interaction = build_interaction(
            request.message,
            context=context,
            base_result={"content": request.message},
            temporal_memory=self._temporal_memory,
        )

        if context.get("conversation_authorized", False) and context.get("conversation_id"):
            self._temporal_memory.append(
                conversation_id=str(context["conversation_id"]),
                record_id=f"temporal:{context['conversation_id']}:{request.request_id}",
                source_type="ELO_COGNITIVE_REQUEST",
                content=request.message,
                provenance={
                    "request_id": request.request_id,
                    "correlation_id": request.correlation_id or request.request_id,
                    "tenant_id": request.tenant_id,
                },
                metadata={
                    "domain": str(request.domain or ""),
                    "session_id": str(request.session_id or ""),
                },
            )

        return {
            "response": {
                "type": "analysis",
                "content": interaction.content,
                "posture": interaction.posture.value,
                "next_step": interaction.next_step,
            },
            "confidence": 1.0,
            "domain": request.domain,
            "interaction": dict(interaction.metadata),
            "provenance": {
                "request_id": request.request_id,
                "correlation_id": request.correlation_id,
                "tenant_id": request.tenant_id,
                "domain": request.domain,
                "principal_id": request.principal_id,
                "provider": "elo-deterministic-core",
                "evidence_refs": [],
                "policy_decision": "ALLOW",
                "validation_status": "validated",
            },
        }

    def _maybe_execute_hermes(self, request: CognitiveRequest):
        mission = request.context.get("hermes_mission")
        if mission is None:
            return None
        if not isinstance(mission, dict):
            raise ValueError("hermes_mission must be an object")

        mission_class = str(mission.get("mission_class", ""))
        capabilities = tuple(str(item) for item in mission.get("authorized_capabilities", ()))
        if mission_class != _RUNTIME_PROBE_MISSION:
            raise ValueError("unsupported Hermes mission class")
        if _RUNTIME_PROBE_CAPABILITY not in capabilities:
            raise ValueError("Hermes runtime probe capability was not authorized by ELO")

        endpoint = os.getenv("ELO_HERMES_ENDPOINT", "").strip()
        if not endpoint:
            raise RuntimeError("ELO_HERMES_ENDPOINT is required for Hermes execution")

        hermes_request = HermesExecutionRequest(
            request_id=request.request_id,
            intent=request.message,
            context={"domain": request.domain, "mission": _RUNTIME_PROBE_MISSION},
            tenant_scope=request.tenant_id,
            mission_class=_RUNTIME_PROBE_MISSION,
            authorized_capabilities=capabilities,
            method="runtime_probe",
            constraints={"read_only": True, "canonical_mutation": False},
            evidence_requirements=("execution", "outcome"),
            execution_policy={"bounded": True, "approval_required_for_mutation": True},
        )
        return self._hermes_bridge.execute(
            hermes_request,
            capability=_RUNTIME_PROBE_CAPABILITY,
            endpoint=endpoint,
        )


__all__ = ["CognitiveCore"]
