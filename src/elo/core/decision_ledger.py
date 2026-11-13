"""Contract boundary for the CRL decision-ledger projection.

This module deliberately does not implement persistence. The canonical decision
state remains DecisionLifecycle; durable execution/versioning remains owned by
the existing GitHub ledger. This port prevents Core code from inventing a second
decision store while giving the CRL a typed integration boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from .decision_outcome_loop import DecisionLifecycle, DecisionState, DecisionTransition


class DecisionLedgerContractError(ValueError):
    """Raised when a decision-ledger projection violates its contract."""


@dataclass(frozen=True)
class DecisionLedgerEvent:
    """Immutable projection of one lifecycle fact into the durable ledger."""

    event_id: str
    decision_id: str
    state: DecisionState
    occurred_at: datetime
    evidence_ids: tuple[str, ...] = ()
    actor: str | None = None
    source_ref: str | None = None
    request_id: str | None = None
    correlation_id: str | None = None

    def __post_init__(self) -> None:
        if not self.event_id or not self.decision_id:
            raise DecisionLedgerContractError("event_id and decision_id are required")
        if not self.evidence_ids and self.state in {
            DecisionState.EVALUATED,
            DecisionState.ATTRIBUTED,
            DecisionState.LEARNED,
            DecisionState.CLOSED,
        }:
            raise DecisionLedgerContractError(
                f"{self.state.value} ledger events require evidence"
            )


class DecisionLedgerPort(Protocol):
    """Durable-ledger adapter owned outside Core.

    Implementations may project to GitHub Issue/PR history or another already
    authorized durable ledger. They must not become a decision authority.
    """

    def append(self, event: DecisionLedgerEvent) -> None:
        """Append an idempotent lifecycle projection."""

    def read(self, decision_id: str) -> tuple[DecisionLedgerEvent, ...]:
        """Return the durable projection for one decision."""


def transition_to_event(
    transition: DecisionTransition,
    *,
    event_id: str,
    source_ref: str | None = None,
    request_id: str | None = None,
    correlation_id: str | None = None,
) -> DecisionLedgerEvent:
    """Translate an existing DOL transition without creating new state."""

    return DecisionLedgerEvent(
        event_id=event_id,
        decision_id=transition.decision_id,
        state=transition.to_state,
        occurred_at=transition.occurred_at,
        evidence_ids=transition.evidence_ids,
        actor=transition.actor,
        source_ref=source_ref,
        request_id=request_id,
        correlation_id=correlation_id,
    )


def project_lifecycle(
    lifecycle: DecisionLifecycle,
    *,
    event_id_factory: callable,
    source_ref: str | None = None,
    request_id: str | None = None,
    correlation_id: str | None = None,
) -> tuple[DecisionLedgerEvent, ...]:
    """Create ledger projections for the existing DOL history.

    No mutation occurs and no alternative lifecycle is created. The caller is
    responsible for sending these events to the already-authorized durable
    ledger adapter.
    """

    return tuple(
        transition_to_event(
            transition,
            event_id=event_id_factory(transition),
            source_ref=source_ref,
            request_id=request_id,
            correlation_id=correlation_id,
        )
        for transition in lifecycle.history
    )
