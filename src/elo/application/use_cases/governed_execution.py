"""Governed application entrypoint for ELO operational capability execution.

The application boundary does not select a capability. Core must first emit a
validated capability decision after cognitive analysis. Authorization remains
an input produced by the canonical authorization boundary; this module does
not implement policy.

The flow is deliberately one-way:
    governed web request
        -> Core cognitive-analysis condition
        -> Core capability decision
        -> orchestration decision
        -> capability selection
        -> native operational execution
        -> optional historical evidence

No canonical learning promotion or Core mutation occurs here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from elo.agent_intake.operational_capability_runtime import (
    OperationalCapabilityRuntime,
    OperationalExecution,
)
from elo.core.capability_resolution import CoreCapabilityDecision, resolve_capability

from ..web_request_boundary import WebRequest
from .orchestrator import (
    AuthorizationDecision,
    GovernedOrchestrator,
    OrchestrationDecision,
    OrchestrationRequest,
    OrchestrationStage,
)


@dataclass(frozen=True, slots=True)
class GovernedExecutionRequest:
    """Application request carrying a capability decision produced by Core."""

    tenant_id: str
    principal_id: str
    domain: str
    objective: str
    core_capability_decision: CoreCapabilityDecision
    evidence_ids: tuple[str, ...]
    authorization: AuthorizationDecision
    payload: dict[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class GovernedExecutionResult:
    decision: OrchestrationDecision
    execution: OperationalExecution | None = None


class GovernedExecutionUseCase:
    """Execute an active ELO capability only after Core resolution and authorization."""

    def __init__(
        self,
        *,
        orchestrator: GovernedOrchestrator | None = None,
        runtime: OperationalCapabilityRuntime | None = None,
    ) -> None:
        self._orchestrator = orchestrator or GovernedOrchestrator()
        self._runtime = runtime or OperationalCapabilityRuntime()

    def execute(self, request: GovernedExecutionRequest) -> GovernedExecutionResult:
        core_decision = request.core_capability_decision
        if not core_decision.executable:
            return GovernedExecutionResult(
                decision=OrchestrationDecision(
                    stage=OrchestrationStage.HANDOFF,
                    status="RECOMMENDATION",
                    reason="Core did not resolve an executable capability",
                )
            )

        orchestration = self._orchestrator.decide_execution(
            OrchestrationRequest(
                tenant_id=request.tenant_id,
                principal_id=request.principal_id,
                domain=request.domain,
                objective=request.objective,
                evidence_ids=request.evidence_ids + tuple(
                    str(item.get("source", ""))
                    for item in core_decision.evidence
                    if item.get("source")
                ),
                authorization=request.authorization,
            )
        )
        if orchestration.stage != OrchestrationStage.EXECUTE:
            return GovernedExecutionResult(decision=orchestration)

        execution = self._runtime.execute(
            core_decision.capability_id,
            request.payload,
        )
        return GovernedExecutionResult(
            decision=orchestration,
            execution=execution,
        )

    def execute_from_core_analysis(
        self,
        *,
        web_request: WebRequest,
        analysis_condition: str,
        authorization: AuthorizationDecision,
        domain: str = "capability",
        payload: dict[str, Any] | None = None,
    ) -> GovernedExecutionResult:
        """Bridge an accepted web request to Core resolution and governed execution.

        ``analysis_condition`` is explicitly the condition already produced by
        the cognitive-analysis stage. The application never receives or chooses
        a capability identifier; Core resolves that identifier from its existing
        governed conditional-pointer matrix.
        """
        core_decision = resolve_capability(
            request_id=web_request.request_id,
            tenant_scope=web_request.tenant_id,
            condition=analysis_condition,
            analysis_evidence=web_request.evidence_ids,
        )
        request = GovernedExecutionRequest(
            tenant_id=web_request.tenant_id,
            principal_id=web_request.principal_id,
            domain=domain,
            objective=web_request.intent,
            core_capability_decision=core_decision,
            evidence_ids=web_request.evidence_ids,
            authorization=authorization,
            payload=payload,
        )
        return self.execute(request)


__all__ = [
    "GovernedExecutionRequest",
    "GovernedExecutionResult",
    "GovernedExecutionUseCase",
]
