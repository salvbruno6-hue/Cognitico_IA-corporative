"""Governed application entrypoint for ELO operational capability execution.

The application boundary does not select a capability. Core must first emit a
validated capability decision after cognitive analysis. Authorization remains
an input produced by the canonical authorization boundary; this module does
not implement policy.

The flow is deliberately one-way:
    governed request
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
from elo.core.capability_resolution import CoreCapabilityDecision

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


__all__ = [
    "GovernedExecutionRequest",
    "GovernedExecutionResult",
    "GovernedExecutionUseCase",
]
