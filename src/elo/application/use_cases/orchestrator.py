"""Canonical ELO orchestration cycle.

This module coordinates the application flow without owning the Cognitive Core,
canonical domain data, memory, or execution adapters.

Execution authority is supplied as a decision produced by the canonical
authorization boundary. The orchestrator deliberately does not interpret
roles, capabilities, sessions, scopes, or bearer credentials.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


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
class OrchestrationRequest:
    tenant_id: str
    principal_id: str
    domain: str
    objective: str
    evidence_ids: tuple[str, ...] = ()
    authorization_decision: bool = False


@dataclass(frozen=True)
class OrchestrationDecision:
    stage: OrchestrationStage
    status: str
    reason: str


class AuthorizationBoundary(Protocol):
    """Adapter to the canonical ELO authorization authority."""

    def authorize_execution(self, request: OrchestrationRequest) -> bool:
        """Return the already-evaluated canonical authorization decision."""


class Orchestrator(Protocol):
    """Application boundary for the closed ELO observation loop."""

    def decide_execution(self, request: OrchestrationRequest) -> OrchestrationDecision:
        """Return EXECUTE only when canonical execution authority is present."""


class GovernedOrchestrator:
    """Minimal deterministic coordinator for the ELO application boundary.

    This class does not implement authorization. ``authorization_decision``
    must be produced by the canonical authorization boundary before execution
    can be selected. No role/capability/session/scope logic is duplicated here.
    """

    def decide_execution(self, request: OrchestrationRequest) -> OrchestrationDecision:
        if not request.tenant_id or not request.principal_id:
            return OrchestrationDecision(
                OrchestrationStage.HANDOFF,
                "BLOCKED",
                "tenant_id and principal_id are required",
            )
        if not request.domain or not request.objective:
            return OrchestrationDecision(
                OrchestrationStage.HANDOFF,
                "BLOCKED",
                "domain and objective are required",
            )
        if not request.evidence_ids:
            return OrchestrationDecision(
                OrchestrationStage.HANDOFF,
                "INCONCLUSIVE",
                "execution requires governed evidence",
            )
        if not request.authorization_decision:
            return OrchestrationDecision(
                OrchestrationStage.HANDOFF,
                "RECOMMENDATION",
                "canonical authorization decision was not granted",
            )
        return OrchestrationDecision(
            OrchestrationStage.EXECUTE,
            "AUTHORIZED",
            "canonical authorization decision and governed evidence are present",
        )
