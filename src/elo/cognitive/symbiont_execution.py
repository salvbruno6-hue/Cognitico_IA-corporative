"""Persistent, idempotent continuation contract for governed Symbiont execution.

This module adds no new cognitive authority. It provides durable execution state,
operation idempotency and reconciliation so the existing ELO Cognitivo can resume
a governed task without depending on conversational continuation.

The reference adapter uses SQLite; production storage may be replaced behind the
same contract.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Mapping


class ResumeStatus(str, Enum):
    CONTINUED = "CONTINUED"
    ALREADY_RUNNING = "ALREADY_RUNNING"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"
    HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
    FAILED = "FAILED"


TERMINAL_STATUSES = {
    ResumeStatus.COMPLETED.value,
    ResumeStatus.BLOCKED.value,
    ResumeStatus.HUMAN_APPROVAL_REQUIRED.value,
    ResumeStatus.FAILED.value,
}


@dataclass(frozen=True, slots=True)
class ExecutionState:
    execution_id: str
    candidate_id: str
    capability_id: str
    owner: str
    status: str
    current_stage: str
    iteration: int
    last_completed_step: str | None
    last_completed_operation: str | None
    state_version: int
    next_action: str
    retry_count: int
    max_attempts: int
    boundary: str | None
    human_required: bool
    canonical_mutation: bool
    production_authorized: bool
    promotion_authorized: bool
    created_at: float
    updated_at: float


@dataclass(frozen=True, slots=True)
class Operation:
    operation_key: str
    execution_id: str
    iteration: int
    stage: str
    operation_type: str
    status: str
    effect_key: str | None
    result_json: str | None
    attempt_count: int
    created_at: float
    updated_at: float


@dataclass(frozen=True, slots=True)
class ActionResult:
    status: str
    next_action: str
    result: Mapping[str, Any]
    evidence_ref: str | None = None
    effect_key: str | None = None
    boundary: str | None = None
    human_required: bool = False


@dataclass(frozen=True, slots=True)
class Reconciliation:
    found_effect: bool
    ambiguous: bool = False
    effect_key: str | None = None
    result: Mapping[str, Any] | None = None


def operation_key(
    execution_id: str,
    iteration: int,
    stage: str,
    operation_type: str,
) -> str:
    raw = "|".join(
        (execution_id.strip(), str(iteration), stage.strip(), operation_type.strip())
    )
    return "op_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def effect_key(
    op_key: str,
    input_fingerprint: str,
    environment: str,
    tool_version: str,
) -> str:
    raw = "|".join((op_key, input_fingerprint, environment, tool_version))
    return "effect_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


class SymbiontExecutionStore:
    """Durable operational state; not a replacement for ELO cognitive memory."""

    def __init__(self, path: str = ":memory:") -> None:
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS symbiont_executions (
                execution_id TEXT PRIMARY KEY,
                candidate_id TEXT NOT NULL,
                capability_id TEXT NOT NULL,
                owner TEXT NOT NULL,
                status TEXT NOT NULL,
                current_stage TEXT NOT NULL,
                iteration INTEGER NOT NULL,
                last_completed_step TEXT,
                last_completed_operation TEXT,
                state_version INTEGER NOT NULL,
                next_action TEXT NOT NULL,
                retry_count INTEGER NOT NULL,
                max_attempts INTEGER NOT NULL,
                boundary TEXT,
                human_required INTEGER NOT NULL,
                canonical_mutation INTEGER NOT NULL,
                production_authorized INTEGER NOT NULL,
                promotion_authorized INTEGER NOT NULL,
                lease_owner TEXT,
                lease_until REAL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS symbiont_operations (
                operation_key TEXT PRIMARY KEY,
                execution_id TEXT NOT NULL,
                iteration INTEGER NOT NULL,
                stage TEXT NOT NULL,
                operation_type TEXT NOT NULL,
                status TEXT NOT NULL,
                effect_key TEXT,
                result_json TEXT,
                attempt_count INTEGER NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                FOREIGN KEY(execution_id) REFERENCES symbiont_executions(execution_id)
            )
            """
        )
        self.connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_sym_ops_execution "
            "ON symbiont_operations(execution_id, iteration)"
        )
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def create_execution(
        self,
        *,
        execution_id: str,
        candidate_id: str,
        capability_id: str,
        owner: str,
        current_stage: str,
        next_action: str,
        max_attempts: int = 3,
    ) -> ExecutionState:
        if not all(
            value.strip()
            for value in (
                execution_id,
                candidate_id,
                capability_id,
                owner,
                current_stage,
                next_action,
            )
        ):
            raise ValueError("execution identity and next_action are required")
        if max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        now = time.time()
        self.connection.execute(
            """
            INSERT INTO symbiont_executions
            VALUES (?, ?, ?, ?, 'ACTIVE', ?, 1, NULL, NULL, 1, ?, 0, ?,
                    NULL, 0, 0, 0, 0, NULL, NULL, ?, ?)
            """,
            (
                execution_id,
                candidate_id,
                capability_id,
                owner,
                current_stage,
                next_action,
                max_attempts,
                now,
                now,
            ),
        )
        self.connection.commit()
        return self.get_execution(execution_id)

    def get_execution(self, execution_id: str) -> ExecutionState:
        row = self.connection.execute(
            "SELECT * FROM symbiont_executions WHERE execution_id=?",
            (execution_id,),
        ).fetchone()
        if row is None:
            raise KeyError(f"execution not found: {execution_id}")
        return ExecutionState(
            execution_id=row["execution_id"],
            candidate_id=row["candidate_id"],
            capability_id=row["capability_id"],
            owner=row["owner"],
            status=row["status"],
            current_stage=row["current_stage"],
            iteration=row["iteration"],
            last_completed_step=row["last_completed_step"],
            last_completed_operation=row["last_completed_operation"],
            state_version=row["state_version"],
            next_action=row["next_action"],
            retry_count=row["retry_count"],
            max_attempts=row["max_attempts"],
            boundary=row["boundary"],
            human_required=bool(row["human_required"]),
            canonical_mutation=bool(row["canonical_mutation"]),
            production_authorized=bool(row["production_authorized"]),
            promotion_authorized=bool(row["promotion_authorized"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def acquire_lease(self, execution_id: str, lease_owner: str, ttl_seconds: float = 30.0) -> bool:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        now = time.time()
        lease_until = now + ttl_seconds
        cursor = self.connection.execute(
            """
            UPDATE symbiont_executions
               SET lease_owner=?, lease_until=?, updated_at=?
             WHERE execution_id=?
               AND (lease_until IS NULL OR lease_until < ? OR lease_owner=?)
            """,
            (lease_owner, lease_until, now, execution_id, now, lease_owner),
        )
        self.connection.commit()
        return cursor.rowcount == 1

    def release_lease(self, execution_id: str, lease_owner: str) -> None:
        self.connection.execute(
            """
            UPDATE symbiont_executions
               SET lease_owner=NULL, lease_until=NULL, updated_at=?
             WHERE execution_id=? AND lease_owner=?
            """,
            (time.time(), execution_id, lease_owner),
        )
        self.connection.commit()

    def get_operation(self, op_key: str) -> Operation | None:
        row = self.connection.execute(
            "SELECT * FROM symbiont_operations WHERE operation_key=?",
            (op_key,),
        ).fetchone()
        if row is None:
            return None
        return Operation(
            operation_key=row["operation_key"],
            execution_id=row["execution_id"],
            iteration=row["iteration"],
            stage=row["stage"],
            operation_type=row["operation_type"],
            status=row["status"],
            effect_key=row["effect_key"],
            result_json=row["result_json"],
            attempt_count=row["attempt_count"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def create_operation(
        self,
        *,
        op_key: str,
        execution_id: str,
        iteration: int,
        stage: str,
        operation_type: str,
    ) -> Operation:
        now = time.time()
        self.connection.execute(
            """
            INSERT OR IGNORE INTO symbiont_operations
            VALUES (?, ?, ?, ?, ?, 'PENDING', NULL, NULL, 0, ?, ?)
            """,
            (op_key, execution_id, iteration, stage, operation_type, now, now),
        )
        self.connection.commit()
        operation = self.get_operation(op_key)
        if operation is None:
            raise RuntimeError("operation creation failed")
        return operation

    def mark_in_progress(self, op_key: str) -> Operation:
        now = time.time()
        self.connection.execute(
            """
            UPDATE symbiont_operations
               SET status='IN_PROGRESS', attempt_count=attempt_count+1, updated_at=?
             WHERE operation_key=?
            """,
            (now, op_key),
        )
        self.connection.commit()
        return self.get_operation(op_key)  # type: ignore[return-value]

    def complete_operation(
        self,
        op_key: str,
        *,
        result: Mapping[str, Any],
        effect: str | None,
    ) -> Operation:
        now = time.time()
        self.connection.execute(
            """
            UPDATE symbiont_operations
               SET status='COMPLETED', effect_key=?, result_json=?, updated_at=?
             WHERE operation_key=?
            """,
            (effect, json.dumps(dict(result), sort_keys=True), now, op_key),
        )
        self.connection.commit()
        return self.get_operation(op_key)  # type: ignore[return-value]

    def mark_retryable(self, op_key: str) -> Operation:
        self.connection.execute(
            "UPDATE symbiont_operations SET status='FAILED_RETRYABLE', updated_at=? WHERE operation_key=?",
            (time.time(), op_key),
        )
        self.connection.commit()
        return self.get_operation(op_key)  # type: ignore[return-value]

    def mark_failed(self, op_key: str) -> Operation:
        self.connection.execute(
            "UPDATE symbiont_operations SET status='FAILED_FINAL', updated_at=? WHERE operation_key=?",
            (time.time(), op_key),
        )
        self.connection.commit()
        return self.get_operation(op_key)  # type: ignore[return-value]

    def advance(
        self,
        execution_id: str,
        *,
        status: str,
        current_stage: str,
        next_action: str,
        last_step: str,
        operation_key_value: str,
        iteration: int,
        boundary: str | None = None,
        human_required: bool = False,
    ) -> ExecutionState:
        now = time.time()
        self.connection.execute(
            """
            UPDATE symbiont_executions
               SET status=?, current_stage=?, next_action=?, last_completed_step=?,
                   last_completed_operation=?, iteration=?, state_version=state_version+1,
                   boundary=?, human_required=?, updated_at=?
             WHERE execution_id=?
            """,
            (
                status,
                current_stage,
                next_action,
                last_step,
                operation_key_value,
                iteration,
                boundary,
                int(human_required),
                now,
                execution_id,
            ),
        )
        self.connection.commit()
        return self.get_execution(execution_id)


Executor = Callable[[ExecutionState, Operation], ActionResult]
Reconciler = Callable[[Operation], Reconciliation]


class SymbiontResumer:
    """Idempotent continuation engine for the existing ELO Cognitivo."""

    def __init__(
        self,
        store: SymbiontExecutionStore,
        *,
        executor: Executor,
        reconciler: Reconciler,
        lease_ttl_seconds: float = 30.0,
    ) -> None:
        self.store = store
        self.executor = executor
        self.reconciler = reconciler
        self.lease_ttl_seconds = lease_ttl_seconds

    def resume(self, execution_id: str, *, worker_id: str, max_steps: int = 100) -> ExecutionState:
        if max_steps < 1:
            raise ValueError("max_steps must be >= 1")
        if not self.store.acquire_lease(execution_id, worker_id, self.lease_ttl_seconds):
            return self.store.get_execution(execution_id)

        try:
            for _ in range(max_steps):
                state = self.store.get_execution(execution_id)

                if state.status in TERMINAL_STATUSES:
                    return state

                if state.canonical_mutation or state.promotion_authorized:
                    return self.store.advance(
                        execution_id,
                        status=ResumeStatus.HUMAN_APPROVAL_REQUIRED.value,
                        current_stage=state.current_stage,
                        next_action="HUMAN_APPROVAL_REQUIRED",
                        last_step=state.last_completed_step or "BOUNDARY_CHECK",
                        operation_key_value=state.last_completed_operation or "none",
                        iteration=state.iteration,
                        boundary="promotion_or_canonical_authority boundary",
                        human_required=True,
                    )

                if not state.next_action.strip():
                    return self.store.advance(
                        execution_id,
                        status=ResumeStatus.BLOCKED.value,
                        current_stage=state.current_stage,
                        next_action="BLOCKED",
                        last_step=state.last_completed_step or "STATE_VALIDATION",
                        operation_key_value=state.last_completed_operation or "none",
                        iteration=state.iteration,
                        boundary="active execution has no next_action",
                        human_required=True,
                    )

                op_key = operation_key(
                    execution_id,
                    state.iteration,
                    state.current_stage,
                    state.next_action,
                )
                operation = self.store.get_operation(op_key)
                if operation is None:
                    operation = self.store.create_operation(
                        op_key=op_key,
                        execution_id=execution_id,
                        iteration=state.iteration,
                        stage=state.current_stage,
                        operation_type=state.next_action,
                    )

                if operation.status == "COMPLETED":
                    result = json.loads(operation.result_json or "{}")
                    action = ActionResult(
                        status="COMPLETED",
                        next_action=str(result.get("next_action", "CONTINUE")),
                        result=result,
                        evidence_ref=result.get("evidence_ref"),
                        effect_key=operation.effect_key,
                    )
                else:
                    if operation.status == "IN_PROGRESS":
                        reconciliation = self.reconciler(operation)
                        if reconciliation.ambiguous:
                            return self.store.advance(
                                execution_id,
                                status=ResumeStatus.HUMAN_APPROVAL_REQUIRED.value,
                                current_stage=state.current_stage,
                                next_action="HUMAN_APPROVAL_REQUIRED",
                                last_step=state.last_completed_step or "RECONCILE",
                                operation_key_value=op_key,
                                iteration=state.iteration,
                                boundary="operation effect cannot be deterministically reconciled",
                                human_required=True,
                            )
                        if reconciliation.found_effect:
                            result = dict(reconciliation.result or {})
                            self.store.complete_operation(
                                op_key,
                                result=result,
                                effect=reconciliation.effect_key,
                            )
                            continue
                        self.store.mark_retryable(op_key)

                    if operation.status == "FAILED_FINAL":
                        return self.store.advance(
                            execution_id,
                            status=ResumeStatus.BLOCKED.value,
                            current_stage=state.current_stage,
                            next_action="BLOCKED",
                            last_step=state.last_completed_step or "FAILED_FINAL",
                            operation_key_value=op_key,
                            iteration=state.iteration,
                            boundary="operation reached final failure",
                            human_required=True,
                        )

                    operation = self.store.mark_in_progress(op_key)
                    action = self.executor(state, operation)

                    if action.human_required:
                        self.store.complete_operation(
                            op_key,
                            result=dict(action.result),
                            effect=action.effect_key,
                        )
                        return self.store.advance(
                            execution_id,
                            status=ResumeStatus.HUMAN_APPROVAL_REQUIRED.value,
                            current_stage=state.current_stage,
                            next_action="HUMAN_APPROVAL_REQUIRED",
                            last_step=state.last_completed_step or state.current_stage,
                            operation_key_value=op_key,
                            iteration=state.iteration,
                            boundary=action.boundary,
                            human_required=True,
                        )

                    self.store.complete_operation(
                        op_key,
                        result={**dict(action.result), "next_action": action.next_action,
                                "evidence_ref": action.evidence_ref},
                        effect=action.effect_key,
                    )

                next_iteration = state.iteration + 1
                if action.status in {"BLOCKED", "FAILED"}:
                    final_status = ResumeStatus.BLOCKED.value if action.status == "BLOCKED" else ResumeStatus.FAILED.value
                    return self.store.advance(
                        execution_id,
                        status=final_status,
                        current_stage=state.current_stage,
                        next_action=action.next_action,
                        last_step=state.current_stage,
                        operation_key_value=op_key,
                        iteration=state.iteration,
                        boundary=action.boundary,
                        human_required=True,
                    )

                if action.status == "COMPLETED" and action.next_action in {"COMPLETED", "DONE"}:
                    return self.store.advance(
                        execution_id,
                        status=ResumeStatus.COMPLETED.value,
                        current_stage=state.current_stage,
                        next_action="COMPLETED",
                        last_step=state.current_stage,
                        operation_key_value=op_key,
                        iteration=state.iteration,
                    )

                self.store.advance(
                    execution_id,
                    status="ACTIVE",
                    current_stage=action.next_action,
                    next_action=action.next_action,
                    last_step=state.current_stage,
                    operation_key_value=op_key,
                    iteration=next_iteration,
                )

            return self.store.get_execution(execution_id)
        finally:
            self.store.release_lease(execution_id, worker_id)


__all__ = [
    "ActionResult",
    "ExecutionState",
    "Operation",
    "Reconciliation",
    "ResumeStatus",
    "SymbiontExecutionStore",
    "SymbiontResumer",
    "effect_key",
    "operation_key",
]
