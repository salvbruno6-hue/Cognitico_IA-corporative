"""Canonical ELO orchestration cycle.

This module coordinates the application flow without owning the Cognitive Core,
canonical domain data, memory, or execution adapters.

Execution authority is supplied by a decision produced by the canonical
authorization boundary. The orchestrator deliberately does not interpret
roles, capabilities, sessions, scopes, or bearer credentials.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from typing import Protocol, TYPE_CHECKING

from elo.evidence import Evidence, EvidenceRepository

if TYPE_CHECKING:
    from elo.cognitive.reasoning.capability_selection import CapabilityDecision, CapabilityRequirement, CapabilitySelector
    from elo.cognitive.routing.execution_routing import ExecutionRouter, ModelCandidate, ToolCandidate
    from elo.cognitive.routing.intelligence_router import IntelligenceRouter, IntelligenceRequest
    from elo.core.capability_registry import CapabilityRegistry
    from elo.core.execution_boundary import ExecutionOutcome, ExecutionRequest, ExecutionAdapter
    from elo.cognitive.symbiont_capability_governance import GlobalCapabilityVisibility


class OrchestrationStage(StrEnum):
    OBSERVE = "OBSERVE"
    CONTEXTUALIZE = "CONTEXTUALIZE"
    ANALYZE = "ANALYZE"
    PROJECT = "PROJECT"
    DECIDE = "DECIDE"
    HANDOFF = "HANDOFF"
    EXECUTE = "EXECUTE"
    MONITOR = "MONITOR"
    OUTCOME_FEEDBACK = "OUTCOME_FEEDBACK"
    LEARN = "LEARN"
    EVOLVE = "EVOLVE"


@dataclass(frozen=True)
class AuthorizationDecision:
    """Immutable result supplied by the canonical ELO authorization authority."""

    authorized: bool
    authority: str
    identity_id: str
    role: str
    evidence_ref: str
    session_id: str = ""
    binding_id: str = ""
    grant_id: str = ""
    operation: str = "execute"
    resource_id: str = ""
    expires_at: str = ""

    def is_canonical(self) -> bool:
        return (
            self.authority == "elo-authz"
            and self.authorized
            and bool(self.identity_id)
            and bool(self.role)
            and bool(self.evidence_ref.strip())
        )

    def is_transport_valid(self, *, now: datetime | None = None) -> bool:
        if not self.is_canonical():
            return False
        if not self.session_id or not self.binding_id or not self.grant_id:
            return False
        if self.operation != "execute" or not self.resource_id or not self.expires_at:
            return False
        try:
            expiry = datetime.fromisoformat(self.expires_at.replace("Z", "+00:00"))
        except ValueError:
            return False
        reference = now or datetime.now(timezone.utc)
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        return expiry > reference


@dataclass(frozen=True)
class OrchestrationRequest:
    tenant_id: str
    principal_id: str
    domain: str
    objective: str
    evidence_ids: tuple[str, ...] = ()
    authorization: AuthorizationDecision | None = None
    request_id: str = ""
    correlation_id: str = ""
    decision_pattern_candidate_ref: str | None = None


@dataclass(frozen=True)
class OrchestrationDecision:
    stage: OrchestrationStage
    status: str
    reason: str


@dataclass(frozen=True)
class CapabilityOrientation:
    """Consultative intervention guidance derived from Symbiont visibility."""

    capability_id: str
    state: str
    action: str
    owner: str | None
    authorized: bool
    reason: str


class AuthorizationBoundary(Protocol):
    def authorize_execution(self, request: OrchestrationRequest) -> AuthorizationDecision:
        """Return the typed decision produced by the canonical authority."""


class Orchestrator(Protocol):
    def advise_capability(
        self,
        visibility: "GlobalCapabilityVisibility",
        capability_id: str,
        *,
        authorized_actions: frozenset[str] = frozenset(),
    ) -> CapabilityOrientation:
        """Return bounded capability guidance from explicit Symbiont visibility."""

    def decide_execution(self, request: OrchestrationRequest) -> OrchestrationDecision:
        """Return EXECUTE only when canonical execution authority is present."""

    def consult_forge(self, request: OrchestrationRequest, forge):
        """Consult catalog-governed Forge knowledge without learning or execution."""
        import re
        from elo.cognitive.response.intelligent_orchestration_response import OrchestrationResponseComposer

        if not request.tenant_id or not request.objective:
            raise ValueError("tenant_id and objective are required")

        match = re.search(r"\b(?:MLT\.)?M\d{2}\b", request.objective, flags=re.IGNORECASE)
        evidence_ids: list[str] = []
        evidence_by_source: dict[str, list[str]] = {}

        def save_forge_evidence(
            *,
            table: str,
            domain: str,
            claim: str,
            record_id: str = "",
            fields=(),
            value=None,
            absence_type=None,
            query_scope=None,
        ) -> None:
            evidence = Evidence.from_forge(
                tenant_id=request.tenant_id,
                source_table=table,
                source_domain=domain,
                source_record_id=record_id,
                source_fields=fields,
                claim=claim,
                value=value,
                absence_type=absence_type,
                query_scope={
                    "request_id": request.request_id,
                    "correlation_id": request.correlation_id,
                    **dict(query_scope or {}),
                },
            )
            self._evidence_repository.save(evidence)
            evidence_ids.append(evidence.evidence_id)
            evidence_by_source.setdefault(table, []).append(evidence.evidence_id)

        if match:
            reference = match.group(0).upper()
            context = forge.governed_model_context(reference, request.objective)
            entity = context.get("entity") or {}
            model = context.get("model") or {}
            save_forge_evidence(
                table="modelos",
                domain="produtos",
                record_id=str(entity.get("model_id") or reference),
                fields=("codigo", "nome", "ativo"),
                claim=f"Forge confirmou o modelo {model.get('codigo') or reference}.",
                value={key: model.get(key) for key in ("codigo", "nome", "ativo")},
            )
        else:
            context = forge.governed_demand_context(request.objective)

        discovery = context.get("governed_discovery") or {}
        linked = discovery.get("linked_records") or {}

        if not match:
            save_forge_evidence(
                table="cross_domain_demand_and_impacts",
                domain=request.domain or "forge",
                claim="Forge consultou fontes governadas para demanda e impactos entre domínios.",
                value={
                    "scope": discovery.get("scope"),
                    "source_count": len(discovery.get("sources_considered") or []),
                    "linked_record_count": sum(len(rows) for rows in linked.values()),
                },
                query_scope={"scope": "cross_domain_demand_and_impacts"},
            )

        for table, rows in linked.items():
            domain = request.domain or "forge"
            if isinstance(rows, list) and rows:
                for row in rows[:25]:
                    save_forge_evidence(
                        table=str(table),
                        domain=domain,
                        record_id=str(row.get("id") or row.get("demanda_id") or ""),
                        fields=tuple(row.keys()),
                        claim=f"Registro observado em {table} no escopo da consulta governada.",
                        value=row,
                    )
            else:
                save_forge_evidence(
                    table=str(table),
                    domain=domain,
                    claim=f"Nenhum registro foi recuperado em {table} no escopo consultado.",
                    absence_type="no_matching_record_found",
                    query_scope={"scope": "governed_consultation"},
                )

        for item in discovery.get("not_linked") or discovery.get("not_scoped") or []:
            table = str(item.get("table_name") or "")
            if not table:
                continue
            save_forge_evidence(
                table=table,
                domain=str(item.get("dominio_codigo") or request.domain or "forge"),
                claim=(
                    f"Forge não estabeleceu relação segura entre {table} "
                    f"e {match.group(0).upper() if match else 'a consulta recebida'}."
                ),
                absence_type="no_safe_relationship",
                query_scope={"reason": item.get("reason")},
            )

        context = {
            **context,
            "evidence_by_source": evidence_by_source,
        }
        return OrchestrationResponseComposer(
            evidence_repository=self._evidence_repository
        ).compose_forge(
            request=request,
            forge_context=context,
            evidence_ids=tuple(evidence_ids),
        )

    def compose_response(
        self,
        request: OrchestrationRequest,
        selection,
        outcome,
    ):
        """Compose a rich human-facing response from already-produced facts."""


class GovernedOrchestrator:
    """Deterministic coordinator over existing ELO authorities.

    Capability selection, routing, authorization and execution remain owned by
    their canonical components. This class only composes those boundaries.

    Shared read-side dependencies are injected at this composition boundary so
    downstream response layers cannot silently create isolated in-memory
    repositories and lose canonical evidence continuity.
    """

    def __init__(self, *, evidence_repository: EvidenceRepository | None = None) -> None:
        self._evidence_repository = evidence_repository or EvidenceRepository()

    def advise_capability(
        self,
        visibility: "GlobalCapabilityVisibility",
        capability_id: str,
        *,
        authorized_actions: frozenset[str] = frozenset(),
    ) -> CapabilityOrientation:
        from elo.cognitive.symbiont_capability_governance import CapabilityVisibilityState

        record = next(
            (item for item in visibility.records if item.capability_id == capability_id),
            None,
        )
        if record is None:
            action = "INVESTIGATE"
            return CapabilityOrientation(
                capability_id=capability_id,
                state="UNKNOWN",
                action=action,
                owner=None,
                authorized=action in authorized_actions,
                reason="capability is absent from the supplied Symbiont visibility snapshot",
            )

        actions = {
            CapabilityVisibilityState.REGISTERED_VISIBLE: "USE_CANONICAL",
            CapabilityVisibilityState.EXISTING_BUT_UNWIRED: "CONNECT_CANONICAL",
            CapabilityVisibilityState.IMPLEMENTED_NOT_REGISTERED: "REGISTER_CAPABILITY",
            CapabilityVisibilityState.REGISTERED_WITHOUT_IMPLEMENTATION_VIEW: "RECONCILE_IMPLEMENTATION_VIEW",
            CapabilityVisibilityState.UNRESOLVED_OWNER: "RESOLVE_OWNER",
        }
        action = actions[record.state]
        return CapabilityOrientation(
            capability_id=record.capability_id,
            state=record.state.value,
            action=action,
            owner=record.owner,
            authorized=action in authorized_actions,
            reason=(
                "use the existing canonical capability"
                if action == "USE_CANONICAL"
                else "follow the explicit Symbiont visibility gap; authorization remains external"
            ),
        )

    def decide_execution(self, request: OrchestrationRequest) -> OrchestrationDecision:
        if not request.tenant_id or not request.principal_id:
            return OrchestrationDecision(OrchestrationStage.HANDOFF, "BLOCKED", "tenant_id and principal_id are required")
        if not request.domain or not request.objective:
            return OrchestrationDecision(OrchestrationStage.HANDOFF, "BLOCKED", "domain and objective are required")
        if not request.evidence_ids:
            return OrchestrationDecision(OrchestrationStage.HANDOFF, "INCONCLUSIVE", "execution requires governed evidence")
        if request.authorization is None:
            return OrchestrationDecision(OrchestrationStage.HANDOFF, "RECOMMENDATION", "canonical authorization decision is absent")
        if not request.authorization.is_canonical():
            return OrchestrationDecision(OrchestrationStage.HANDOFF, "RECOMMENDATION", "authorization provenance is not canonical")
        if not request.authorization.authorized:
            return OrchestrationDecision(OrchestrationStage.HANDOFF, "RECOMMENDATION", "canonical authorization decision was not granted")
        return OrchestrationDecision(
            OrchestrationStage.EXECUTE,
            "AUTHORIZED",
            "canonical authorization decision and governed evidence are present",
        )

    def execute_capability(
        self,
        request: OrchestrationRequest,
        *,
        requirement: "CapabilityRequirement",
        selector: "CapabilitySelector",
        execution_router: "ExecutionRouter",
        intelligence_router: "IntelligenceRouter",
        models=None,
        tools=None,
        preferred_models=None,
        hermes_routing_signal=None,
        runtime_commit: str | None = None,
        runtime_trace: str | None = None,
        execution_id: str | None = None,
    ):
        """Connect Registry/Selector → Router → ExecutionBoundary → runtime.

        This method is composition only. It does not authorize, select a
        provider policy, or create a new execution authority.

        The current IntelligenceRouter executes model/provider routes. A
        tool-only route is therefore rejected explicitly rather than being
        reported as a successful runtime connection.
        """
        from elo.core.execution_boundary import ExecutionRequest, execute_governed

        selection: CapabilityDecision = selector.select(requirement)
        if selection.status != "SELECTED" or not selection.capability_name:
            return selection, None

        orchestration = self.decide_execution(request)
        if orchestration.stage is not OrchestrationStage.EXECUTE:
            return selection, None

        if request.authorization is None or not request.authorization.is_transport_valid():
            return selection, None

        route = execution_router.route(
            selection.capability_name,
            models=models,
            tools=tools,
            preferred_models=preferred_models,
        )

        if not route.model_id:
            raise LookupError(
                f"selected route has no executable model/provider path for capability: "
                f"{selection.capability_name}"
            )

        if not request.request_id or not request.correlation_id:
            raise ValueError("request_id and correlation_id are required for governed execution")
        resolved_execution_id = execution_id or request.request_id
        if resolved_execution_id != request.request_id:
            raise ValueError("execution_id must match request_id for governed execution provenance")

        from elo.cognitive.routing.intelligence_router import IntelligenceRequest

        intelligence_request = IntelligenceRequest(
            request_id=request.request_id,
            tenant_id=request.tenant_id,
            specialist_id=selection.capability_name,
            capability=selection.capability_name,
            instructions=request.objective,
            metadata={"domain": request.domain, "principal_id": request.principal_id},
        )

        class RoutedExecutionAdapter:
            def execute(self, execution_request):
                response = intelligence_router.execute_routed(
                    intelligence_request,
                    route,
                    hermes_routing_signal=hermes_routing_signal,
                    runtime_commit=runtime_commit,
                    runtime_trace=runtime_trace,
                    execution_id=resolved_execution_id,
                    decision_pattern_candidate_ref=request.decision_pattern_candidate_ref,
                )
                return {
                    "provider": response.provider,
                    "model": response.model,
                    "request_id": response.request_id,
                }

        execution_request = ExecutionRequest(
            request_id=request.request_id,
            tenant_id=request.tenant_id,
            principal_id=request.principal_id,
            action_id=route.model_id,
            authorization_id=request.authorization.grant_id,
            evidence_ids=request.evidence_ids,
            correlation_id=request.correlation_id,
            decision_pattern_candidate_ref=request.decision_pattern_candidate_ref,
        )
        outcome = execute_governed(execution_request, RoutedExecutionAdapter())
        return selection, outcome

    def consult_forge(self, request: OrchestrationRequest, forge):
        """Consult catalog-governed Forge knowledge without learning or execution."""
        import re
        from elo.cognitive.response.intelligent_orchestration_response import OrchestrationResponseComposer

        if not request.tenant_id or not request.objective:
            raise ValueError("tenant_id and objective are required")
        match = re.search(r"\b(?:MLT\.)?M\d{2}\b", request.objective, flags=re.IGNORECASE)
        if match:
            reference = match.group(0).upper()
            context = forge.governed_model_context(reference, request.objective)
        else:
            context = forge.governed_demand_context(request.objective)
        evidence_ids = []
        entity = context.get("entity") or {}
        model = context.get("model") or {}
        if entity:
            evidence_ids.append(self._evidence_repository.save(Evidence.create(
                tenant_id=request.tenant_id, domain=request.domain or "forge",
                source_type="supabase_elo_forge", source_id=str(entity.get("model_id") or entity.get("requested_reference")),
                claim=f"Forge confirmou o modelo {model.get('codigo') or entity.get('requested_reference')}",
                content_ref=f"supabase_elo_forge:modelos:{entity.get('model_id') or entity.get('requested_reference')}",
                quality="OBSERVED", relevance=1.0,
                provenance={"catalog":"elo_aprendizado_fontes", "read_only":True, "learning_performed":False},
            )).evidence_id)
        else:
            evidence_ids.append(self._evidence_repository.save(Evidence.create(
                tenant_id=request.tenant_id, domain=request.domain or "forge",
                source_type="supabase_elo_forge", source_id="cross_domain_demand_and_impacts",
                claim="Forge consultou fontes governadas para demanda e impactos entre domínios.",
                content_ref="supabase_elo_forge:cross_domain_demand_and_impacts",
                quality="OBSERVED", relevance=1.0,
                provenance={"catalog":"elo_aprendizado_fontes", "read_only":True, "learning_performed":False, "scope":"cross_domain_demand_and_impacts"},
            )).evidence_id)
        discovery = context.get("governed_discovery") or {}
        for table, rows in (discovery.get("linked_records") or {}).items():
            evidence_ids.append(self._evidence_repository.save(Evidence.create(
                tenant_id=request.tenant_id, domain=request.domain or "forge",
                source_type="supabase_elo_forge", source_id=table,
                claim=f"Forge recuperou {len(rows)} registro(s) da fonte governada {table}.",
                content_ref=f"supabase_elo_forge:{table}", quality="OBSERVED", relevance=0.8,
                provenance={"catalog":"elo_aprendizado_fontes", "table_name":table, "read_only":True, "learning_performed":False},
            )).evidence_id)
        for item in discovery.get("not_linked") or []:
            table = str(item.get("table_name") or "")
            if not table: continue
            evidence_ids.append(self._evidence_repository.save(Evidence.create(
                tenant_id=request.tenant_id, domain=request.domain or "forge",
                source_type="supabase_elo_forge", source_id=table,
                claim=f"Forge não estabeleceu relação segura entre {table} e {reference}.",
                content_ref=f"supabase_elo_forge:{table}:unlinked", quality="OBSERVED", relevance=0.5,
                provenance={"catalog":"elo_aprendizado_fontes", "table_name":table, "read_only":True, "absence_of_safe_link":True, "learning_performed":False},
            )).evidence_id)
        return OrchestrationResponseComposer(evidence_repository=self._evidence_repository).compose_forge(
            request=request, forge_context=context, evidence_ids=tuple(evidence_ids)
        )
    def compose_response(self, request: OrchestrationRequest, selection, outcome):
        """Return rich human-facing output without changing execution authority."""
        from elo.cognitive.response.intelligent_orchestration_response import (
            OrchestrationResponseComposer,
        )

        return OrchestrationResponseComposer(
            evidence_repository=self._evidence_repository,
        ).compose(
            request=request,
            selection=selection,
            outcome=outcome,
        )
