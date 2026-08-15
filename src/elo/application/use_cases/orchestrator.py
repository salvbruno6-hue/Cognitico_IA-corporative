"""Canonical ELO orchestration cycle.

This module coordinates the application flow without owning the Cognitive Core,
canonical domain data, memory, or execution adapters.
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
    execution_authorized: bool = False


@dataclass(frozen=True)
class OrchestrationDecision:
    stage: OrchestrationStage
    status: str
    reason: str


class Orchestrator(Protocol):
    """Application boundary for the closed ELO observation loop."""

    def decide_execution(self, request: OrchestrationRequest) -> OrchestrationDecision:
        """Return EXECUTE only when explicit execution authority is present."""


class GovernedOrchestrator:
    """Minimal deterministic coordinator for the ELO application boundary."""

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
        if not request.execution_authorized:
            return OrchestrationDecision(
                OrchestrationStage.HANDOFF,
                "RECOMMENDATION",
                "execution authority was not granted",
            )
        return OrchestrationDecision(
            OrchestrationStage.EXECUTE,
            "AUTHORIZED",
            "explicit execution authority and governed evidence are present",
        )
