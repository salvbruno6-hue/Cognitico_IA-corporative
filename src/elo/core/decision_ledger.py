"""Decision Ledger projection over the canonical DecisionLifecycle.

The ledger is an audit projection, not a second decision state machine. Durable
implementations may provide a sink backed by the existing ELO audit authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from .decision_outcome_loop import DecisionLifecycle, DecisionTransition


class DecisionLedgerSink(Protocol):
    """Persistence boundary supplied by an existing audit implementation."""

    def append(self, record: "DecisionLedgerRecord") -> None: ...


@dataclass(frozen=True)
class DecisionLedgerRecord:
    decision_id: str
    from_state: str
    to_state: str
    occurred_at: datetime
    evidence_ids: tuple[str, ...] = ()
    actor: str | None = None
    correlation_id: str | None = None
    request_id: str | None = None
    source: str = "elo.core.decision_outcome_loop"


class DecisionLedger:
    """Read/append projection; lifecycle remains the sole transition authority."""

    def __init__(self, sink: DecisionLedgerSink | None = None) -> None:
        self._sink = sink
        self._records: list[DecisionLedgerRecord] = []

    @property
    def records(self) -> tuple[DecisionLedgerRecord, ...]:
        return tuple(self._records)

    def append_transition(
        self,
        transition: DecisionTransition,
        *,
        correlation_id: str | None = None,
        request_id: str | None = None,
    ) -> DecisionLedgerRecord:
        record = DecisionLedgerRecord(
            decision_id=transition.decision_id,
            from_state=transition.from_state.value,
            to_state=transition.to_state.value,
            occurred_at=transition.occurred_at,
            evidence_ids=transition.evidence_ids,
            actor=transition.actor,
            correlation_id=correlation_id,
            request_id=request_id,
        )
        self._records.append(record)
        if self._sink is not None:
            self._sink.append(record)
        return record

    def append_lifecycle(
        self,
        lifecycle: DecisionLifecycle,
        *,
        correlation_id: str | None = None,
        request_id: str | None = None,
    ) -> tuple[DecisionLedgerRecord, ...]:
        start = len(self._records)
        for transition in lifecycle.history:
            if not any(
                record.decision_id == transition.decision_id
                and record.occurred_at == transition.occurred_at
                and record.to_state == transition.to_state.value
                for record in self._records
            ):
                self.append_transition(
                    transition,
                    correlation_id=correlation_id,
                    request_id=request_id,
                )
        return tuple(self._records[start:])

    def for_decision(self, decision_id: str) -> tuple[DecisionLedgerRecord, ...]:
        return tuple(r for r in self._records if r.decision_id == decision_id)

    def assert_matches_lifecycle(self, lifecycle: DecisionLifecycle) -> None:
        expected = tuple(
            (t.decision_id, t.from_state.value, t.to_state.value, t.occurred_at)
            for t in lifecycle.history
        )
        actual = tuple(
            (r.decision_id, r.from_state, r.to_state, r.occurred_at)
            for r in self.for_decision(lifecycle.decision.decision_id)
        )
        if actual != expected:
            raise ValueError("decision ledger diverges from DecisionLifecycle")
