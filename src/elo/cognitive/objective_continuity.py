"""Persistent objective/workstream continuity over the existing Symbiont runtime.

This module does not create a second objective authority, supervisor, scheduler,
or execution engine. Strategic objective identity remains owned by the OKR
contract/repository; durable execution state remains owned by
``SymbiontExecutionStore``.

The adapter binds one objective/workstream to a stable execution id, preserves
progress checkpoints across process/chat restarts, rejects stale replay, and
turns repeated lack of objective-relevant progress into CORRECT, REPLAN and
finally ESCALATE decisions.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Sequence

from elo.contracts.okr import Objective
from elo.cognitive.symbiont_execution import (
    ExecutionState,
    SymbiontExecutionStore,
    operation_key,
)


class ObjectiveLoopDecision(StrEnum):
    CONTINUE = "CONTINUE"
    CORRECT = "CORRECT"
    REPLAN = "REPLAN"
    ESCALATE = "ESCALATE"
    COMPLETE = "COMPLETE"


@dataclass(frozen=True, slots=True)
class ObjectiveLoopCheckpoint:
    execution_id: str
    tenant_id: str
    objective_id: str
    objective_title: str
    workstream_id: str
    status: str
    stage: str
    next_action: str
    iteration: int
    state_version: int
    last_progress_token: str | None
    no_progress_streak: int
    last_decision: ObjectiveLoopDecision | None
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ObjectiveLoopCycleResult:
    checkpoint: ObjectiveLoopCheckpoint
    decision: ObjectiveLoopDecision
    reason: str
    no_progress_streak: int


def objective_execution_id(*, tenant_id: str, objective_id: str, workstream_id: str) -> str:
    values = (tenant_id.strip(), objective_id.strip(), workstream_id.strip())
    if not all(values):
        raise ValueError("tenant_id, objective_id and workstream_id are required")
    digest = sha256("|".join(values).encode("utf-8")).hexdigest()[:24]
    return f"objective-loop:{digest}"


class ObjectiveContinuityAdapter:
    """Bind governed objectives to the canonical persistent execution runtime."""

    OWNER = "strategic-objective-domain"
    CANDIDATE_PREFIX = "objective:"
    CAPABILITY_PREFIX = "objective-workstream:"

    def __init__(self, store: SymbiontExecutionStore) -> None:
        self.store = store

    def start_or_resume(
        self,
        objective: Objective,
        *,
        workstream_id: str,
        initial_action: str,
        max_cycles: int = 12,
    ) -> ObjectiveLoopCheckpoint:
        workstream = workstream_id.strip()
        action = initial_action.strip()
        if not workstream or not action:
            raise ValueError("workstream_id and initial_action are required")
        if max_cycles < 2:
            raise ValueError("max_cycles must be >= 2")
        if not objective.evidence_refs:
            raise ValueError("objective continuity requires an evidence-backed objective")

        execution_id = objective_execution_id(
            tenant_id=objective.tenant_id,
            objective_id=objective.objective_id,
            workstream_id=workstream,
        )
        try:
            state = self.store.get_execution(execution_id)
        except KeyError:
            state = self.store.create_execution(
                execution_id=execution_id,
                candidate_id=f"{self.CANDIDATE_PREFIX}{objective.objective_id}",
                capability_id=f"{self.CAPABILITY_PREFIX}{workstream}",
                owner=self.OWNER,
                current_stage=action,
                next_action=action,
                max_attempts=max_cycles,
            )
        self._validate_binding(state, objective=objective, workstream_id=workstream)
        return self.checkpoint(objective, workstream_id=workstream)

    def checkpoint(
        self,
        objective: Objective,
        *,
        workstream_id: str,
    ) -> ObjectiveLoopCheckpoint:
        execution_id = objective_execution_id(
            tenant_id=objective.tenant_id,
            objective_id=objective.objective_id,
            workstream_id=workstream_id,
        )
        state = self.store.get_execution(execution_id)
        self._validate_binding(state, objective=objective, workstream_id=workstream_id)

        payload: dict[str, object] = {}
        if state.last_completed_operation:
            operation = self.store.get_operation(state.last_completed_operation)
            if operation and operation.result_json:
                payload = json.loads(operation.result_json)

        decision_raw = str(payload.get("decision") or "").strip()
        last_decision = ObjectiveLoopDecision(decision_raw) if decision_raw else None
        refs = tuple(str(ref) for ref in payload.get("evidence_refs", []) if str(ref).strip())
        progress = str(payload.get("progress_token") or "").strip() or None
        streak = int(payload.get("no_progress_streak") or 0)

        return ObjectiveLoopCheckpoint(
            execution_id=state.execution_id,
            tenant_id=objective.tenant_id,
            objective_id=objective.objective_id,
            objective_title=objective.title,
            workstream_id=workstream_id.strip(),
            status=state.status,
            stage=state.current_stage,
            next_action=state.next_action,
            iteration=state.iteration,
            state_version=state.state_version,
            last_progress_token=progress,
            no_progress_streak=streak,
            last_decision=last_decision,
            evidence_refs=refs,
        )

    def record_cycle(
        self,
        objective: Objective,
        *,
        workstream_id: str,
        expected_state_version: int,
        progress_token: str,
        evidence_refs: Sequence[str],
        proposed_next_action: str,
        objective_satisfied: bool = False,
        within_scope: bool = True,
        authority_available: bool = True,
        risk_level: str = "LOW",
        correct_after: int = 1,
        replan_after: int = 2,
        escalate_after: int = 4,
    ) -> ObjectiveLoopCycleResult:
        if not (0 < correct_after <= replan_after < escalate_after):
            raise ValueError("progress thresholds must satisfy correct <= replan < escalate")
        progress = progress_token.strip()
        next_action = proposed_next_action.strip()
        refs = tuple(dict.fromkeys(ref.strip() for ref in evidence_refs if ref and ref.strip()))
        if not progress or not next_action:
            raise ValueError("progress_token and proposed_next_action are required")
        if not refs:
            raise ValueError("each objective loop cycle requires evidence_refs")

        checkpoint = self.checkpoint(objective, workstream_id=workstream_id)
        if checkpoint.state_version != expected_state_version:
            raise ValueError("stale objective checkpoint replay blocked")
        state = self.store.get_execution(checkpoint.execution_id)
        if state.status in {"COMPLETED", "BLOCKED", "FAILED", "HUMAN_APPROVAL_REQUIRED"}:
            raise ValueError(f"objective loop is terminal: {state.status}")

        if checkpoint.last_progress_token is not None and progress == checkpoint.last_progress_token:
            streak = checkpoint.no_progress_streak + 1
        else:
            streak = 0

        decision, reason = self._decide(
            state=state,
            objective_satisfied=objective_satisfied,
            within_scope=within_scope,
            authority_available=authority_available,
            risk_level=risk_level,
            no_progress_streak=streak,
            correct_after=correct_after,
            replan_after=replan_after,
            escalate_after=escalate_after,
        )

        op_key = operation_key(
            state.execution_id,
            state.iteration,
            state.current_stage,
            state.next_action,
        )
        operation = self.store.create_operation(
            op_key=op_key,
            execution_id=state.execution_id,
            iteration=state.iteration,
            stage=state.current_stage,
            operation_type=state.next_action,
        )

        payload = {
            "objective_id": objective.objective_id,
            "workstream_id": workstream_id.strip(),
            "progress_token": progress,
            "no_progress_streak": streak,
            "decision": decision.value,
            "reason": reason,
            "evidence_refs": list(refs),
        }

        # If a process died after persisting the operation result but before
        # advancing the execution state, the result is replayed, not re-created.
        if operation.status == "COMPLETED" and operation.result_json:
            payload = json.loads(operation.result_json)
            decision = ObjectiveLoopDecision(str(payload["decision"]))
            reason = str(payload["reason"])
            streak = int(payload.get("no_progress_streak") or 0)
        else:
            self.store.mark_in_progress(op_key)
            effect = "objective-cycle:" + sha256(
                f"{op_key}|{progress}|{decision.value}".encode("utf-8")
            ).hexdigest()[:24]
            self.store.complete_operation(op_key, result=payload, effect=effect)

        self._advance(state, op_key=op_key, decision=decision, proposed_next_action=next_action)
        updated = self.checkpoint(objective, workstream_id=workstream_id)
        return ObjectiveLoopCycleResult(
            checkpoint=updated,
            decision=decision,
            reason=reason,
            no_progress_streak=streak,
        )

    @staticmethod
    def _decide(
        *,
        state: ExecutionState,
        objective_satisfied: bool,
        within_scope: bool,
        authority_available: bool,
        risk_level: str,
        no_progress_streak: int,
        correct_after: int,
        replan_after: int,
        escalate_after: int,
    ) -> tuple[ObjectiveLoopDecision, str]:
        if objective_satisfied:
            return ObjectiveLoopDecision.COMPLETE, "objective acceptance criteria satisfied"
        if not within_scope:
            return ObjectiveLoopDecision.ESCALATE, "next action would leave approved objective scope"
        if not authority_available:
            return ObjectiveLoopDecision.ESCALATE, "required authority is unavailable"
        if risk_level.strip().upper() in {"HIGH", "CRITICAL", "ALTO", "CRITICO"}:
            return ObjectiveLoopDecision.ESCALATE, "risk exceeds bounded autonomous execution"
        if state.iteration >= state.max_attempts:
            return ObjectiveLoopDecision.ESCALATE, "objective loop autonomy cycle budget exhausted"
        if no_progress_streak >= escalate_after:
            return ObjectiveLoopDecision.ESCALATE, "persistent no-progress after correction/replanning"
        if no_progress_streak >= replan_after:
            return ObjectiveLoopDecision.REPLAN, "current approach is not producing objective-relevant progress"
        if no_progress_streak >= correct_after:
            return ObjectiveLoopDecision.CORRECT, "local correction required before repeating the action"
        return ObjectiveLoopDecision.CONTINUE, "objective-relevant progress observed"

    def _advance(
        self,
        state: ExecutionState,
        *,
        op_key: str,
        decision: ObjectiveLoopDecision,
        proposed_next_action: str,
    ) -> None:
        if decision is ObjectiveLoopDecision.COMPLETE:
            self.store.advance(
                state.execution_id,
                status="COMPLETED",
                current_stage=state.current_stage,
                next_action="COMPLETED",
                last_step=state.current_stage,
                operation_key_value=op_key,
                iteration=state.iteration,
            )
            return
        if decision is ObjectiveLoopDecision.ESCALATE:
            self.store.advance(
                state.execution_id,
                status="HUMAN_APPROVAL_REQUIRED",
                current_stage=state.current_stage,
                next_action="HUMAN_APPROVAL_REQUIRED",
                last_step=state.current_stage,
                operation_key_value=op_key,
                iteration=state.iteration,
                boundary="OBJECTIVE_LOOP_ESCALATION",
                human_required=True,
            )
            return

        next_action = {
            ObjectiveLoopDecision.CONTINUE: proposed_next_action,
            ObjectiveLoopDecision.CORRECT: "CORRECT",
            ObjectiveLoopDecision.REPLAN: "REPLAN",
        }[decision]
        self.store.advance(
            state.execution_id,
            status="ACTIVE",
            current_stage=next_action,
            next_action=next_action,
            last_step=state.current_stage,
            operation_key_value=op_key,
            iteration=state.iteration + 1,
        )

    @classmethod
    def _validate_binding(
        cls,
        state: ExecutionState,
        *,
        objective: Objective,
        workstream_id: str,
    ) -> None:
        if state.candidate_id != f"{cls.CANDIDATE_PREFIX}{objective.objective_id}":
            raise ValueError("objective execution binding mismatch")
        if state.capability_id != f"{cls.CAPABILITY_PREFIX}{workstream_id.strip()}":
            raise ValueError("objective workstream binding mismatch")
        if state.owner != cls.OWNER:
            raise ValueError("objective continuity owner mismatch")


__all__ = [
    "ObjectiveContinuityAdapter",
    "ObjectiveLoopCheckpoint",
    "ObjectiveLoopCycleResult",
    "ObjectiveLoopDecision",
    "objective_execution_id",
]
