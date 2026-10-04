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
    """Immutable result supplied by the canonical ELO authorization authority.

    This value carries provenance so a bare boolean cannot be mistaken for an
    authorization result. Authorization policy remains exclusively owned by
    ``elo-authz``; this type only transports its already-evaluated result.
    """

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
        """Preserve the base elo-authz transport contract."""
        return (
            self.authority == "elo-authz"
            and self.authorized
            and bool(self.identity_id)
            and bool(self.role)
            and bool(self.evidence_ref.strip())
        )

    def is_transport_valid(self, *, now: datetime | None = None) -> bool:
        """Validate the stronger provenance required for implementation execution."""
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


@dataclass(frozen=True)
class OrchestrationDecision:
    stage: OrchestrationStage
    status: str
    reason: str


@dataclass(frozen=True)
class CapabilityOrientation:
    """Consultative intervention guidance derived from Symbiont visibility.

    This is a recommendation contract only. It does not authorize or mutate
    canonical state; authorization is supplied by the existing boundary.
    """

    capability_id: str
    state: str
    action: str
    owner: str | None
    authorized: bool
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

    def advise_capability(
        self,
        visibility: "GlobalCapabilityVisibility",
        capability_id: str,
        *,
        authorized_actions: frozenset[str] = frozenset(),
    ) -> CapabilityOrientation:
        """Turn explicit Symbiont visibility into bounded guidance.

        The Orchestrator does not infer runtime state and does not mutate
        canonical ELO state. It maps an explicit visibility state to the
        smallest known intervention and reports whether that action was
        already authorized by the caller.
        """
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
