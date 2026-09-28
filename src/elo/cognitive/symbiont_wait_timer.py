"""Non-blocking timer contract for governed Symbiont waits.

The timer records when an external condition may be checked again. It never
sleeps, executes the awaited action, decides gate outcomes, or creates a
scheduler authority. A caller may invoke the perception bridge when the timer
is ready.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Mapping

from elo.cognitive.symbiont_execution import ExecutionState, SymbiontExecutionStore

WAIT_BOUNDARY_TYPE = "symbiont_wait"


@dataclass(frozen=True, slots=True)
class WaitTimer:
    kind: str
    reference: str
    wake_at: float
    interval_seconds: float
    attempt: int

    @property
    def ready(self) -> bool:
        return self.ready_at(time.time())

    def ready_at(self, now: float) -> bool:
        return now >= self.wake_at

    def remaining_seconds(self, now: float | None = None) -> float:
        current = time.time() if now is None else now
        return max(0.0, self.wake_at - current)


def arm_wait_timer(
    store: SymbiontExecutionStore,
    execution_id: str,
    *,
    kind: str,
    reference: str,
    delay_seconds: float,
    attempt: int = 1,
    now: float | None = None,
) -> ExecutionState:
    """Persist a future eligibility time without blocking the worker."""
    if not kind.strip() or not reference.strip():
        raise ValueError("wait kind and reference are required")
    if delay_seconds <= 0:
        raise ValueError("delay_seconds must be positive")
    if attempt < 1:
        raise ValueError("attempt must be >= 1")

    current = time.time() if now is None else now
    wake_at = current + delay_seconds
    boundary = json.dumps(
        {
            "type": WAIT_BOUNDARY_TYPE,
            "kind": kind,
            "reference": reference,
            "wake_at": wake_at,
            "interval_seconds": delay_seconds,
            "attempt": attempt,
        },
        sort_keys=True,
    )
    state = store.get_execution(execution_id)
    return store.advance(
        execution_id,
        status="WAITING",
        current_stage=state.current_stage,
        next_action=state.next_action,
        last_step=state.last_completed_step or "WAIT",
        operation_key_value=state.last_completed_operation or "none",
        iteration=state.iteration,
        boundary=boundary,
        human_required=False,
    )


def read_wait_timer(state: ExecutionState) -> WaitTimer | None:
    if not state.boundary:
        return None
    try:
        payload: Mapping[str, Any] = json.loads(state.boundary)
    except (TypeError, ValueError, json.JSONDecodeError):
        return None
    if payload.get("type") != WAIT_BOUNDARY_TYPE:
        return None
    try:
        return WaitTimer(
            kind=str(payload["kind"]),
            reference=str(payload["reference"]),
            wake_at=float(payload["wake_at"]),
            interval_seconds=float(payload["interval_seconds"]),
            attempt=int(payload["attempt"]),
        )
    except (KeyError, TypeError, ValueError):
        return None


def timer_ready(state: ExecutionState, *, now: float | None = None) -> bool:
    timer = read_wait_timer(state)
    if timer is None:
        return False
    current = time.time() if now is None else now
    return timer.ready_at(current)


__all__ = [
    "WAIT_BOUNDARY_TYPE",
    "WaitTimer",
    "arm_wait_timer",
    "read_wait_timer",
    "timer_ready",
]
