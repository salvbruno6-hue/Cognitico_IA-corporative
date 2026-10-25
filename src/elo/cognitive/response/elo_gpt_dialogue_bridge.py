"""Bridge canonical Objective Continuity results into GPT-facing replies.

This bridge consumes the real `ObjectiveLoopCycleResult` produced by the
canonical objective-continuity owner. It does not execute a cycle, authorize an
action, persist state, or decide whether the ELO may continue. Those facts must
already exist when this bridge is called.
"""

from __future__ import annotations

from elo.cognitive.objective_continuity import ObjectiveLoopCycleResult
from elo.cognitive.response.elo_gpt_dialogue import (
    AuthorizationState,
    EloDialogueFacts,
    EloDialogueReply,
    EloDialogueResponsePolicy,
    EvidenceState,
    ExecutionState,
    PersistenceState,
)


def compose_objective_cycle_reply(
    result: ObjectiveLoopCycleResult,
    *,
    persistence_state: PersistenceState,
    authorization_state: AuthorizationState,
    continuation_permitted: bool,
    human_required: bool | None = None,
    evidence_state: EvidenceState | None = None,
) -> EloDialogueReply:
    """Project one real ELO objective cycle into the reply ChatGPT should emit."""

    checkpoint = result.checkpoint
    progress_token = (checkpoint.last_progress_token or "").strip()
    if not progress_token:
        raise ValueError("objective cycle reply requires a persisted progress_token")

    canonical_human_required = checkpoint.status == "HUMAN_APPROVAL_REQUIRED"
    if human_required is None:
        human_required = canonical_human_required
    elif bool(human_required) != canonical_human_required:
        raise ValueError("human_required does not match canonical checkpoint status")

    resolved_evidence_state = evidence_state or (
        EvidenceState.OBSERVED if checkpoint.evidence_refs else EvidenceState.INSUFFICIENT
    )

    facts = EloDialogueFacts(
        objective_id=checkpoint.objective_id,
        workstream_id=checkpoint.workstream_id,
        checkpoint_version=checkpoint.state_version,
        state=f"{checkpoint.status}:{checkpoint.stage}",
        decision=result.decision.value,
        next_action=checkpoint.next_action,
        progress_token=progress_token,
        justification=result.reason,
        evidence_refs=checkpoint.evidence_refs,
        persistence_state=persistence_state,
        authorization_state=authorization_state,
        execution_state=_execution_state(checkpoint.status),
        evidence_state=resolved_evidence_state,
        continuation_permitted=continuation_permitted,
        human_required=human_required,
    )
    return EloDialogueResponsePolicy().compose(facts)


def _execution_state(status: str) -> ExecutionState:
    normalized = status.strip().upper()
    if normalized == "FAILED":
        return ExecutionState.FAILED
    if normalized in {"BLOCKED", "HUMAN_APPROVAL_REQUIRED"}:
        return ExecutionState.BLOCKED
    if normalized == "COMPLETED":
        return ExecutionState.EXECUTED
    return ExecutionState.PENDING
