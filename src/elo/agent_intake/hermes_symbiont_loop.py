"""Apply the canonical Symbiont execution boundary to Hermes candidates.

This adapter does not create a second loop or authority. It places each existing
Hermes implementation probe inside the persistent Symbiont execution contract,
then returns the resulting governed state to the existing Hermes 13 aggregator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from elo.cognitive.symbiont_execution import (
    ActionResult,
    SymbiontExecutionStore,
    SymbiontResumer,
)


@dataclass(frozen=True, slots=True)
class SymbiontCandidateResult:
    candidate_id: str
    implementation: object
    evidence: object
    status: str
    next_state: str
    canonical_mutation: bool


Probe = Callable[[], tuple[object, object]]


def apply_candidate_through_symbiont(
    candidate_id: str,
    probe: Probe,
    *,
    implementation_first: bool = True,
) -> SymbiontCandidateResult:
    """Execute one existing Hermes probe through the canonical Symbiont runtime."""

    store = SymbiontExecutionStore()
    execution_id = f"hermes-symbiont:{candidate_id}"
    store.create_execution(
        execution_id=execution_id,
        candidate_id=candidate_id,
        capability_id=candidate_id,
        owner="ELO Cognitive / Symbiont",
        current_stage="IMPLEMENTATION",
        next_action="EXECUTE_CANDIDATE",
        max_attempts=1,
    )

    captured: dict[str, object] = {}

    def executor(state, operation) -> ActionResult:
        first, second = probe()
        implementation = first if implementation_first else second
        evidence = second if implementation_first else first
        captured["implementation"] = implementation
        captured["evidence"] = evidence

        canonical_mutation = bool(
            getattr(implementation, "canonical_mutation", False)
        )
        if canonical_mutation:
            return ActionResult(
                status="BLOCKED",
                next_action="HUMAN_APPROVAL_REQUIRED",
                result={
                    "candidate_id": candidate_id,
                    "reason": "canonical mutation attempted",
                },
                boundary="Hermes candidate attempted canonical mutation inside Symbiont",
                human_required=True,
            )

        next_state = getattr(implementation, "next_state", None)
        if next_state is None:
            result = getattr(implementation, "result", None)
            next_state = (
                "ELO_REVIEW"
                if result == "READY_FOR_ELO_REVIEW"
                else str(result or "ELO_REVIEW")
            )

        return ActionResult(
            status="CONTINUE",
            next_action=str(next_state),
            result={
                "candidate_id": candidate_id,
                "next_state": str(next_state),
                "evidence_present": evidence is not None,
            },
        )

    def reconciler(operation):
        return __import__(
            "elo.cognitive.symbiont_execution",
            fromlist=["Reconciliation"],
        ).Reconciliation(found_effect=False)

    try:
        resumer = SymbiontResumer(
            store,
            executor=executor,
            reconciler=reconciler,
        )
        state = resumer.resume(
            execution_id,
            worker_id=f"hermes-loop:{candidate_id}",
            max_steps=1,
        )
        implementation = captured.get("implementation")
        evidence = captured.get("evidence")
        if implementation is None:
            raise RuntimeError(
                f"Symbiont did not execute Hermes candidate: {candidate_id}"
            )

        next_state = getattr(implementation, "next_state", None)
        if next_state is None:
            result = getattr(implementation, "result", None)
            next_state = (
                "ELO_REVIEW"
                if result == "READY_FOR_ELO_REVIEW"
                else str(result or state.next_action)
            )

        return SymbiontCandidateResult(
            candidate_id=candidate_id,
            implementation=implementation,
            evidence=evidence,
            status=state.status,
            next_state=str(next_state),
            canonical_mutation=bool(
                getattr(implementation, "canonical_mutation", False)
            ),
        )
    finally:
        store.close()


__all__ = [
    "SymbiontCandidateResult",
    "apply_candidate_through_symbiont",
]
