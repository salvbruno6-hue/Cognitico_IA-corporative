"""Canonical ELO orchestration cycle.

This module coordinates the application flow without owning the Cognitive Core,
canonical domain data, memory, or execution adapters.

Execution authority is supplied by a decision produced by the canonical
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
class AuthorizationDecision:
    """Immutable result supplied by the canonical authorization authority.

    This value carries provenance so a bare boolean cannot be mistaken for an
    authorization result. Authorization policy remains exclusively owned by
    ``elo-authz``; this type only transports its already-evaluated result.
    """

    authorized: bool
    authority: str
    identity_id: str
    role: str

    def is_canonical(self) -> bool:
        return (
            self.authority == "elo-authz"
            and bool(self.identity_id)
            and bool(self.role)
        )


@dataclass(frozen=True)
class OrchestrationRequest:
    tenant_id: str
    principal_id: str
    domain: str
    objective: str
    evidence_ids: tuple[str, ...] = ()
    authorization: AuthorizationDecision | None = None


@dataclass(frozen=True)
class OrchestrationDecision:
    stage: OrchestrationStage
    status: str
    reason: str


class AuthorizationBoundary(Protocol):
    """Adapter to the canonical ELO authorization authority."""

    def authorize_execution(self, request: OrchestrationRequest) -> AuthorizationDecision:
        """Return the typed decision produced by the canonical authority."""


class Orchestrator(Protocol):
    """Application boundary for the closed ELO observation loop."""

    def decide_execution(self, request: OrchestrationRequest) -> OrchestrationDecision:
        """Return EXECUTE only when canonical execution authority is present."""


class GovernedOrchestrator:
    """Minimal deterministic coordinator for the ELO application boundary.

    This class does not implement authorization. ``authorization`` must be the
    typed result produced by the canonical authorization boundary before
    execution can be selected. No role/capability/session/scope logic is
    duplicated here.
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
        if request.authorization is None:
            return OrchestrationDecision(
                OrchestrationStage.HANDOFF,
                "RECOMMENDATION",
                "canonical authorization decision is absent",
            )
        if not request.authorization.is_canonical():
            return OrchestrationDecision(
                OrchestrationStage.HANDOFF,
                "RECOMMENDATION",
                "authorization provenance is not canonical",
            )
        if not request.authorization.authorized:
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
