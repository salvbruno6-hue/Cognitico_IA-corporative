"""Canonical CognitiveCore implementation for the ELO prototype."""

from __future__ import annotations

import os
from typing import Any

from elo.interface.contracts import CognitiveRequest

from .agents.hermes_contract import HermesExecutionRequest
from elo.core.interaction_runtime import build_interaction
from elo.core.temporal_memory import TemporalConversationMemory
from elo.application.use_cases.orchestrator import GovernedOrchestrator, OrchestrationRequest
from elo.application.use_cases.okr_capability import StrategicOkrCapability, build_okr_capability_probe
from elo.application.queries.okr import OkrQueryService
from elo.application.queries.okr_evidence import OkrEvidenceResolver
from elo.application.queries.okr_metric import OkrMetricResolver
from elo.cognitive.reasoning.capability_selection import CapabilityRequirement, CapabilitySelector
from elo.core.capability_registry import CapabilityRegistry
from elo.evidence import EvidenceRepository
from elo.infrastructure.supabase_kpi_registry import SupabaseFormalKpiRegistryReader
from elo.infrastructure.supabase_okr_repository import SupabaseOkrReadRepository
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
        strategic_okr_capability: StrategicOkrCapability | None = None,
    ) -> None:
        self._hermes_bridge = hermes_bridge or SymbiontHermesBridge()
        self._temporal_memory = temporal_memory or TemporalConversationMemory()
        self._evidence_repository = EvidenceRepository()
        self._orchestrator = GovernedOrchestrator(evidence_repository=self._evidence_repository)
        self._strategic_okr_capability = strategic_okr_capability or self._build_strategic_okr_capability()
        probes = ()
        if self._strategic_okr_capability is not None:
            probes = (build_okr_capability_probe(health_check=lambda: True),)
        self._capability_registry = CapabilityRegistry(probes)
        self._capability_selector = CapabilitySelector(self._capability_registry)

    def process(self, request: CognitiveRequest) -> dict[str, Any]:
        if not request.tenant_id:
            raise ValueError("tenant_id is required")

        context = request.context or {}

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

        okr_objective_id = str(context.get("okr_objective_id") or "").strip()
        if okr_objective_id:
            return self._consult_strategic_okr(request, objective_id=okr_objective_id)

        forge_enabled = bool(
            context.get(
                "forge_enabled",
                bool(
                    os.getenv("ELO_FORGE_SUPABASE_URL")
                    or os.getenv("SUPABASE_URL")
                ),
            )
        )
        if forge_enabled:
            from elo.infrastructure.forge_runtime import load_forge_adapter

            forge = load_forge_adapter()
            orchestration_request = OrchestrationRequest(
                tenant_id=request.tenant_id,
                principal_id=request.principal_id or request.user_id or "",
                domain=request.domain or "conversational",
                objective=request.message,
                request_id=request.request_id,
                correlation_id=request.correlation_id or request.request_id,
            )
            consultation = self._orchestrator.consult_forge(
                orchestration_request,
                forge,
            )
            return {
                "response": {
                    "type": "forge_grounded_analysis",
                    "content": consultation.response,
                    "status": consultation.status,
                },
                "confidence": 1.0 if consultation.evidence_state == "OBSERVED" else 0.0,
                "domain": request.domain,
                "forge": {
                    "capability": consultation.capability,
                    "stage": consultation.stage,
                    "evidence_state": consultation.evidence_state,
                    "evidence_ids": list(consultation.evidence_refs),
                    "next_action": consultation.next_action,
                },
                "provenance": {
                    "request_id": request.request_id,
                    "correlation_id": request.correlation_id,
                    "tenant_id": request.tenant_id,
                    "domain": request.domain,
                    "principal_id": request.principal_id,
                    "provider": "supabase_elo_forge",
                    "evidence_refs": list(consultation.evidence_refs),
                    "policy_decision": "READ_ONLY_GOVERNED_SOURCE_SELECTION",
                    "validation_status": "evidence_observed",
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

    def _consult_strategic_okr(self, request: CognitiveRequest, *, objective_id: str) -> dict[str, Any]:
        if self._strategic_okr_capability is None:
            raise RuntimeError("strategic_okr runtime is unavailable")

        requirement = CapabilityRequirement(
            capability="objective_context",
            preferred_kinds=("domain",),
            min_score=0.3,
        )
        selection = self._capability_selector.select(requirement)
        if selection.status != "SELECTED" or selection.capability_name != "strategic_okr":
            raise RuntimeError("strategic_okr capability is not registered as available")

        orchestration_request = OrchestrationRequest(
            tenant_id=request.tenant_id,
            principal_id=request.principal_id or request.user_id or "",
            domain=request.domain or "strategic",
            objective=request.message,
            request_id=request.request_id,
            correlation_id=request.correlation_id or request.request_id,
        )
        result = self._strategic_okr_capability.consult_objective(
            request=orchestration_request,
            objective_id=objective_id,
        )
        if result is None:
            return {
                "response": {
                    "type": "strategic_okr",
                    "content": "Objetivo não encontrado no tenant autorizado.",
                    "status": "NOT_FOUND",
                },
                "confidence": 0.0,
                "domain": request.domain,
                "okr": {"objective_id": objective_id, "capability": "strategic_okr"},
                "provenance": {
                    "request_id": request.request_id,
                    "correlation_id": request.correlation_id,
                    "tenant_id": request.tenant_id,
                    "provider": "governed_orchestrator:strategic_okr",
                    "evidence_refs": [],
                    "policy_decision": "READ_ONLY_GOVERNED_SOURCE_SELECTION",
                    "validation_status": "not_found",
                },
            }

        snapshot, response = result
        return {
            "response": {
                "type": "strategic_okr",
                "content": response.response,
                "status": response.status,
            },
            "confidence": 1.0 if response.evidence_state == "OBSERVED" else 0.5 if response.evidence_state == "PARTIAL" else 0.0,
            "domain": request.domain,
            "okr": {
                "objective_id": snapshot.objective_id,
                "objective_health": snapshot.objective_health,
                "capability": response.capability,
                "evidence_state": response.evidence_state,
                "evidence_ids": list(response.evidence_refs),
                "next_action": response.next_action,
            },
            "provenance": {
                "request_id": request.request_id,
                "correlation_id": request.correlation_id,
                "tenant_id": request.tenant_id,
                "domain": request.domain,
                "principal_id": request.principal_id,
                "provider": "governed_orchestrator:strategic_okr",
                "evidence_refs": list(response.evidence_refs),
                "policy_decision": "READ_ONLY_GOVERNED_SOURCE_SELECTION",
                "validation_status": response.evidence_state,
            },
        }

    def _build_strategic_okr_capability(self) -> StrategicOkrCapability | None:
        url = (os.getenv("ELO_FORGE_SUPABASE_URL") or os.getenv("SUPABASE_URL") or "").strip()
        service_role_key = (os.getenv("SUPABASE_SERVICE_ROLE_KEY") or "").strip()
        if not url or not service_role_key:
            return None
        repository = SupabaseOkrReadRepository(url, service_role_key)
        kpi_registry = SupabaseFormalKpiRegistryReader(url, service_role_key)
        return StrategicOkrCapability(
            queries=OkrQueryService(repository),
            metrics=OkrMetricResolver(kpi_registry),
            evidence=OkrEvidenceResolver(self._evidence_repository),
        )

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
