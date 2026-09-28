"""Persistent Hermes -> Symbiont -> external-gate continuation.

This adapter composes the existing Symbiont execution store, resumer, wait timer
and gate perception contracts. It owns no new state machine or authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from elo.cognitive.symbiont_execution import (
    ActionResult,
    Reconciliation,
    SymbiontExecutionStore,
    SymbiontResumer,
)
from elo.cognitive.symbiont_gate_perception import (
    ExternalGateObservation,
    WAITING_FOR_EXTERNAL_GATE,
    perceive_external_gate,
    wait_for_external_gate,
)


@dataclass(frozen=True, slots=True)
class HermesGateContinuation:
    execution_id: str
    candidate_id: str
    status: str
    next_state: str
    evidence: object
    waiting_for_gate: bool
    resumed: bool


Probe = Callable[[], tuple[object, object]]
GateObserver = Callable[[str], ExternalGateObservation]


class HermesSymbiontGateSession:
    """Keep one governed execution alive across an external-gate wait."""

    def __init__(
        self,
        candidate_id: str,
        probe: Probe,
        *,
        implementation_first: bool = True,
        store: SymbiontExecutionStore | None = None,
    ) -> None:
        self.candidate_id = candidate_id
        self.probe = probe
        self.implementation_first = implementation_first
        self.store = store or SymbiontExecutionStore()
        self._owns_store = store is None
        self.execution_id = f"hermes-symbiont:{candidate_id}"
        self._captured: dict[str, object] = {}
        self.store.create_execution(
            execution_id=self.execution_id,
            candidate_id=candidate_id,
            capability_id=candidate_id,
            owner="ELO Cognitive / Symbiont",
            current_stage="IMPLEMENTATION",
            next_action="EXECUTE_CANDIDATE",
            max_attempts=1,
        )
        self.resumer = SymbiontResumer(
            self.store,
            executor=self._execute_candidate,
            reconciler=lambda operation: Reconciliation(found_effect=False),
        )

    def _execute_candidate(self, state, operation) -> ActionResult:
        if state.next_action != "EXECUTE_CANDIDATE":
            return ActionResult(
                status="CONTINUE",
                next_action=state.next_action,
                result={
                    "candidate_id": self.candidate_id,
                    "continuation": "existing_candidate_state",
                },
            )

        first, second = self.probe()
        implementation = first if self.implementation_first else second
        evidence = second if self.implementation_first else first
        self._captured["implementation"] = implementation
        self._captured["evidence"] = evidence

        if bool(getattr(implementation, "canonical_mutation", False)):
            return ActionResult(
                status="BLOCKED",
                next_action="HUMAN_APPROVAL_REQUIRED",
                result={"candidate_id": self.candidate_id, "reason": "canonical mutation attempted"},
                boundary="Hermes candidate attempted canonical mutation inside Symbiont",
                human_required=True,
            )

        next_state = getattr(implementation, "next_state", None)
        if next_state is None:
            result = getattr(implementation, "result", None)
            next_state = "ELO_REVIEW" if result == "READY_FOR_ELO_REVIEW" else str(result or "ELO_REVIEW")

        return ActionResult(
            status="CONTINUE",
            next_action=str(next_state),
            result={"candidate_id": self.candidate_id, "next_state": str(next_state)},
        )

    def start(self) -> HermesGateContinuation:
        state = self.resumer.resume(
            self.execution_id,
            worker_id=f"hermes-gate:{self.candidate_id}",
            max_steps=1,
        )
        implementation = self._captured.get("implementation")
        if implementation is None:
            raise RuntimeError(f"Symbiont did not execute Hermes candidate: {self.candidate_id}")
        return HermesGateContinuation(
            execution_id=self.execution_id,
            candidate_id=self.candidate_id,
            status=state.status,
            next_state=str(getattr(implementation, "next_state", None) or state.next_action),
            evidence=self._captured.get("evidence"),
            waiting_for_gate=False,
            resumed=False,
        )

    def wait_for_gate(self, gate_id: str, *, delay_seconds: float = 30.0, now: float | None = None) -> HermesGateContinuation:
        state = wait_for_external_gate(
            self.store,
            self.execution_id,
            gate_id=gate_id,
            delay_seconds=delay_seconds,
            now=now,
        )
        return HermesGateContinuation(
            execution_id=self.execution_id,
            candidate_id=self.candidate_id,
            status=state.status,
            next_state=state.next_action,
            evidence=self._captured.get("evidence"),
            waiting_for_gate=state.status == WAITING_FOR_EXTERNAL_GATE,
            resumed=False,
        )

    def perceive_and_resume(
        self,
        *,
        observe: GateObserver,
        now: Callable[[], float] | None = None,
        max_steps: int = 1,
    ) -> HermesGateContinuation:
        before = self.store.get_execution(self.execution_id)
        after = perceive_external_gate(
            self.store,
            self.execution_id,
            observe=observe,
            **({"now": now} if now is not None else {}),
        )
        if before.status != WAITING_FOR_EXTERNAL_GATE or after.status != "ACTIVE":
            return HermesGateContinuation(
                execution_id=self.execution_id,
                candidate_id=self.candidate_id,
                status=after.status,
                next_state=after.next_action,
                evidence=self._captured.get("evidence"),
                waiting_for_gate=after.status == WAITING_FOR_EXTERNAL_GATE,
                resumed=False,
            )

        resumed = self.resumer.resume(
            self.execution_id,
            worker_id=f"hermes-gate:{self.candidate_id}",
            max_steps=max_steps,
        )
        return HermesGateContinuation(
            execution_id=self.execution_id,
            candidate_id=self.candidate_id,
            status=resumed.status,
            next_state=resumed.next_action,
            evidence=self._captured.get("evidence"),
            waiting_for_gate=False,
            resumed=True,
        )

    def close(self) -> None:
        if self._owns_store:
            self.store.close()


__all__ = ["HermesGateContinuation", "HermesSymbiontGateSession"]
