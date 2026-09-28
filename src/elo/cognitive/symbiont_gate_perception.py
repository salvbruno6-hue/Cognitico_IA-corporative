"""Governed perception of external gates for Symbiont continuation.

This is a read/reconcile adapter, not a scheduler and not a new authority.
It reuses SymbiontExecutionStore and resumes only when the observed external
gate is deterministically complete and its persisted wait timer is ready.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Callable

from elo.cognitive.symbiont_execution import ExecutionState, SymbiontExecutionStore
from elo.cognitive.symbiont_wait_timer import arm_wait_timer, read_wait_timer


WAITING_FOR_EXTERNAL_GATE = "WAITING_FOR_EXTERNAL_GATE"


@dataclass(frozen=True, slots=True)
class ExternalGateObservation:
    gate_id: str
    state: str
    evidence_ref: str | None = None

    @property
    def completed(self) -> bool:
        return self.state.upper() in {"COMPLETED", "SUCCESS", "PASSED", "MERGED"}


GateObserver = Callable[[str], ExternalGateObservation]


def wait_for_external_gate(
    store: SymbiontExecutionStore,
    execution_id: str,
    *,
    gate_id: str,
    delay_seconds: float = 30.0,
    now: float | None = None,
) -> ExecutionState:
    """Persist a gate wait and its next eligible observation time."""
    if delay_seconds <= 0:
        raise ValueError("delay_seconds must be positive")

    state = store.get_execution(execution_id)
    boundary = json.dumps(
        {"type": "external_gate", "gate_id": gate_id},
        sort_keys=True,
    )
    store.advance(
        execution_id,
        status=WAITING_FOR_EXTERNAL_GATE,
        current_stage=state.current_stage,
        next_action=state.next_action,
        last_step=state.last_completed_step or "WAIT_FOR_EXTERNAL_GATE",
        operation_key_value=state.last_completed_operation or "none",
        iteration=state.iteration,
        boundary=boundary,
        human_required=False,
    )
    return arm_wait_timer(
        store,
        execution_id,
        kind="external_gate",
        reference=gate_id,
        delay_seconds=delay_seconds,
        attempt=1,
        now=now,
        waiting_status=WAITING_FOR_EXTERNAL_GATE,
    )


def perceive_external_gate(
    store: SymbiontExecutionStore,
    execution_id: str,
    *,
    observe: GateObserver,
    now: Callable[[], float] = time.time,
) -> ExecutionState:
    """Observe one gate only when its persisted wait timer is due."""
    state = store.get_execution(execution_id)

    if state.status != WAITING_FOR_EXTERNAL_GATE:
        return state

    timer = read_wait_timer(state)
    gate_id = _gate_id_from_boundary(state)
    if (
        timer is None
        or timer.kind != "external_gate"
        or not gate_id
        or timer.reference != gate_id
    ):
        return store.advance(
            execution_id,
            status="BLOCKED",
            current_stage=state.current_stage,
            next_action="BLOCKED",
            last_step=state.last_completed_step or "WAIT_FOR_EXTERNAL_GATE",
            operation_key_value=state.last_completed_operation or "none",
            iteration=state.iteration,
            boundary="waiting state has no valid external-gate timer",
            human_required=True,
        )

    if not timer.ready_at(now()):
        return state

    observation = observe(timer.reference)

    if not observation.completed:
        return arm_wait_timer(
            store,
            execution_id,
            kind=timer.kind,
            reference=timer.reference,
            delay_seconds=timer.interval_seconds,
            attempt=timer.attempt + 1,
            now=now(),
        )

    resume_boundary = json.dumps(
        {
            "type": "external_gate_completed",
            "gate_id": observation.gate_id,
            "evidence_ref": observation.evidence_ref,
        },
        sort_keys=True,
    )
    return store.advance(
        execution_id,
        status="ACTIVE",
        current_stage=state.current_stage,
        next_action=state.next_action,
        last_step="EXTERNAL_GATE_RECONCILED",
        operation_key_value=state.last_completed_operation or "none",
        iteration=state.iteration + 1,
        boundary=resume_boundary,
        human_required=False,
    )


def _gate_id_from_boundary(state: ExecutionState) -> str | None:
    try:
        payload = json.loads(state.boundary or "{}")
    except (TypeError, ValueError, json.JSONDecodeError):
        return None
    if payload.get("type") != "external_gate":
        return None
    gate_id = payload.get("gate_id")
    return str(gate_id) if gate_id else None


__all__ = [
    "ExternalGateObservation",
    "WAITING_FOR_EXTERNAL_GATE",
    "perceive_external_gate",
    "wait_for_external_gate",
]
