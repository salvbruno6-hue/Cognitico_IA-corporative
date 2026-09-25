"""Governed perception of external gates for Symbiont continuation.

This is a read/reconcile adapter, not a scheduler and not a new authority.
It reuses SymbiontExecutionStore and resumes only when the observed external
gate is deterministically complete.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable

from elo.cognitive.symbiont_execution import (
    ExecutionState,
    SymbiontExecutionStore,
)


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
) -> ExecutionState:
    """Persist a wait state without scheduling or requesting human action."""
    state = store.get_execution(execution_id)
    boundary = json.dumps(
        {"type": "external_gate", "gate_id": gate_id},
        sort_keys=True,
    )
    return store.advance(
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


def perceive_external_gate(
    store: SymbiontExecutionStore,
    execution_id: str,
    *,
    observe: GateObserver,
) -> ExecutionState:
    """Perceive/reconcile one gate; resume only after deterministic completion."""
    state = store.get_execution(execution_id)

    if state.status != WAITING_FOR_EXTERNAL_GATE:
        return state

    if not state.boundary:
        return store.advance(
            execution_id,
            status="BLOCKED",
            current_stage=state.current_stage,
            next_action="BLOCKED",
            last_step=state.last_completed_step or "WAIT_FOR_EXTERNAL_GATE",
            operation_key_value=state.last_completed_operation or "none",
            iteration=state.iteration,
            boundary="waiting state has no external gate reference",
            human_required=True,
        )

    boundary = json.loads(state.boundary)
    if boundary.get("type") != "external_gate" or not boundary.get("gate_id"):
        return store.advance(
            execution_id,
            status="BLOCKED",
            current_stage=state.current_stage,
            next_action="BLOCKED",
            last_step=state.last_completed_step or "WAIT_FOR_EXTERNAL_GATE",
            operation_key_value=state.last_completed_operation or "none",
            iteration=state.iteration,
            boundary="invalid external gate boundary",
            human_required=True,
        )

    observation = observe(str(boundary["gate_id"]))

    if not observation.completed:
        return state

    next_action = state.next_action
    evidence_ref = observation.evidence_ref
    resume_boundary = json.dumps(
        {
            "type": "external_gate_completed",
            "gate_id": observation.gate_id,
            "evidence_ref": evidence_ref,
        },
        sort_keys=True,
    )
    return store.advance(
        execution_id,
        status="ACTIVE",
        current_stage=state.current_stage,
        next_action=next_action,
        last_step="EXTERNAL_GATE_RECONCILED",
        operation_key_value=state.last_completed_operation or "none",
        iteration=state.iteration + 1,
        boundary=resume_boundary,
        human_required=False,
    )


__all__ = [
    "ExternalGateObservation",
    "WAITING_FOR_EXTERNAL_GATE",
    "perceive_external_gate",
    "wait_for_external_gate",
]
