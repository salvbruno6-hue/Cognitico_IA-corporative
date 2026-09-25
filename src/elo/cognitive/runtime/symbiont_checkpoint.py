"""Checkpoint adapter between the canonical CRL and Symbiont execution state.

This module is an adapter only. It does not create a second runtime, supervisor,
memory authority, or state machine. The canonical execution state remains owned
by SymbiontExecutionStore; the CRL remains the cognitive runtime authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from elo.cognitive.symbiont_execution import (
    ActionResult,
    ExecutionState,
    Operation,
    Reconciliation,
    SymbiontExecutionStore,
    SymbiontResumer,
    operation_key,
)


@dataclass(frozen=True, slots=True)
class CRLCheckpoint:
    """Read-only projection used by a CRL handler."""

    execution_id: str
    stage: str
    next_action: str
    iteration: int
    operation_key: str
    state_version: int


def checkpoint_for_crl(
    store: SymbiontExecutionStore,
    execution_id: str,
) -> CRLCheckpoint:
    """Project persistent Symbiont state for the existing CRL."""
    state = store.get_execution(execution_id)
    op_key = operation_key(
        state.execution_id,
        state.iteration,
        state.current_stage,
        state.next_action,
    )
    return CRLCheckpoint(
        execution_id=state.execution_id,
        stage=state.current_stage,
        next_action=state.next_action,
        iteration=state.iteration,
        operation_key=op_key,
        state_version=state.state_version,
    )


def advance_crl_checkpoint(
    store: SymbiontExecutionStore,
    state: ExecutionState,
    operation: Operation,
    action: ActionResult,
) -> ExecutionState:
    """Persist a CRL operation result through the existing Symbiont contract.

    This function deliberately does not authorize production, promotion or
    canonical mutation.
    """
    store.complete_operation(
        operation.operation_key,
        result={
            **dict(action.result),
            "next_action": action.next_action,
            "evidence_ref": action.evidence_ref,
        },
        effect=action.effect_key,
    )

    if action.human_required:
        return store.advance(
            state.execution_id,
            status="HUMAN_APPROVAL_REQUIRED",
            current_stage=state.current_stage,
            next_action="HUMAN_APPROVAL_REQUIRED",
            last_step=state.last_completed_step or state.current_stage,
            operation_key_value=operation.operation_key,
            iteration=state.iteration,
            boundary=action.boundary,
            human_required=True,
        )

    if action.status == "BLOCKED":
        return store.advance(
            state.execution_id,
            status="BLOCKED",
            current_stage=state.current_stage,
            next_action=action.next_action,
            last_step=state.current_stage,
            operation_key_value=operation.operation_key,
            iteration=state.iteration,
            boundary=action.boundary,
            human_required=True,
        )

    if action.status == "FAILED":
        return store.advance(
            state.execution_id,
            status="FAILED",
            current_stage=state.current_stage,
            next_action=action.next_action,
            last_step=state.current_stage,
            operation_key_value=operation.operation_key,
            iteration=state.iteration,
            boundary=action.boundary,
            human_required=True,
        )

    if action.next_action in {"DONE", "COMPLETED"}:
        return store.advance(
            state.execution_id,
            status="COMPLETED",
            current_stage=state.current_stage,
            next_action="COMPLETED",
            last_step=state.current_stage,
            operation_key_value=operation.operation_key,
            iteration=state.iteration,
        )

    return store.advance(
        state.execution_id,
        status="ACTIVE",
        current_stage=action.next_action,
        next_action=action.next_action,
        last_step=state.current_stage,
        operation_key_value=operation.operation_key,
        iteration=state.iteration + 1,
    )


__all__ = ["CRLCheckpoint", "advance_crl_checkpoint", "checkpoint_for_crl"]
