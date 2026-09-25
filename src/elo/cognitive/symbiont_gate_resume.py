"""Controlled bridge from external-gate perception to existing Symbiont resume.

The bridge does not execute a second loop. It only invokes the existing
SymbiontResumer after deterministic external-gate completion.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from elo.cognitive.symbiont_execution import ExecutionState, SymbiontExecutionStore, SymbiontResumer
from elo.cognitive.symbiont_gate_perception import ExternalGateObservation, perceive_external_gate


@dataclass(frozen=True, slots=True)
class GateResumeResult:
    state: ExecutionState
    resumed: bool


def perceive_and_resume(
    store: SymbiontExecutionStore,
    resumer: SymbiontResumer,
    execution_id: str,
    *,
    observe: Callable[[str], ExternalGateObservation],
    worker_id: str,
    max_steps: int = 100,
) -> GateResumeResult:
    before = store.get_execution(execution_id)
    after = perceive_external_gate(store, execution_id, observe=observe)

    if before.status != "WAITING_FOR_EXTERNAL_GATE" or after.status != "ACTIVE":
        return GateResumeResult(state=after, resumed=False)

    resumed = resumer.resume(
        execution_id,
        worker_id=worker_id,
        max_steps=max_steps,
    )
    return GateResumeResult(state=resumed, resumed=True)


__all__ = ["GateResumeResult", "perceive_and_resume"]
