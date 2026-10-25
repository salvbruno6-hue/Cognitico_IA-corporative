"""Bounded pre-finalization loop for ChatGPT-facing ELO dialogue.

This module gives the chat integration one governed chance to consult the
canonical ELO objective loop before emitting a final answer. It never loops
unboundedly, never invents authorization and never replaces Objective
Continuity. The caller supplies the canonical cycle runner and the resulting
ObjectiveLoopCycleResult is projected through the existing ELO->GPT bridge.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from elo.cognitive.objective_continuity import ObjectiveLoopCycleResult
from elo.cognitive.response.elo_gpt_dialogue import (
    AuthorizationState,
    EloDialogueReply,
    EvidenceState,
    PersistenceState,
)
from elo.cognitive.response.elo_gpt_dialogue_bridge import compose_objective_cycle_reply


TRIGGER_TYPE = "CONTINUE_OBJECTIVE"
MAX_REPLAYS_PER_TURN = 1


@dataclass(frozen=True, slots=True)
class EloPreFinalizationRequest:
    objective_id: str
    workstream_id: str
    expected_checkpoint_version: int
    chat_draft: str


@dataclass(frozen=True, slots=True)
class EloNextTrigger:
    trigger_type: str
    objective_id: str
    workstream_id: str
    checkpoint_version: int
    next_action: str
    progress_token: str


@dataclass(frozen=True, slots=True)
class EloPreFinalizationResult:
    final_message: str
    elo_reply: EloDialogueReply
    next_trigger: EloNextTrigger | None
    replay_count: int


class EloChatPreFinalizationLoop:
    """Consult ELO exactly once before ChatGPT finalizes a turn."""

    def __init__(
        self,
        cycle_runner: Callable[[EloPreFinalizationRequest], ObjectiveLoopCycleResult],
    ) -> None:
        self._cycle_runner = cycle_runner

    def run(
        self,
        request: EloPreFinalizationRequest,
        *,
        persistence_state: PersistenceState,
        authorization_state: AuthorizationState,
        continuation_permitted: bool,
        evidence_state: EvidenceState | None = None,
    ) -> EloPreFinalizationResult:
        self._validate_request(request)

        # Strictly one canonical replay per ChatGPT turn.
        result = self._cycle_runner(request)
        self._validate_checkpoint_binding(request, result)

        reply = compose_objective_cycle_reply(
            result,
            persistence_state=persistence_state,
            authorization_state=authorization_state,
            continuation_permitted=continuation_permitted,
            evidence_state=evidence_state,
        )

        next_trigger = None
        if reply.should_continue_automatically:
            next_trigger = EloNextTrigger(
                trigger_type=TRIGGER_TYPE,
                objective_id=result.checkpoint.objective_id,
                workstream_id=result.checkpoint.workstream_id,
                checkpoint_version=result.checkpoint.state_version,
                next_action=reply.next_action,
                progress_token=reply.progress_token,
            )

        # ELO is authoritative for this bounded turn; the draft remains context,
        # not the source of truth for the final operational response.
        final_message = reply.message
        return EloPreFinalizationResult(
            final_message=final_message,
            elo_reply=reply,
            next_trigger=next_trigger,
            replay_count=MAX_REPLAYS_PER_TURN,
        )

    @staticmethod
    def _validate_request(request: EloPreFinalizationRequest) -> None:
        if not request.objective_id.strip() or not request.workstream_id.strip():
            raise ValueError("objective_id and workstream_id are required")
        if request.expected_checkpoint_version < 1:
            raise ValueError("expected_checkpoint_version must be >= 1")

    @staticmethod
    def _validate_checkpoint_binding(
        request: EloPreFinalizationRequest,
        result: ObjectiveLoopCycleResult,
    ) -> None:
        checkpoint = result.checkpoint
        if checkpoint.objective_id != request.objective_id:
            raise ValueError("ELO result objective_id does not match pre-finalization request")
        if checkpoint.workstream_id != request.workstream_id:
            raise ValueError("ELO result workstream_id does not match pre-finalization request")
        if checkpoint.state_version <= request.expected_checkpoint_version:
            raise ValueError("ELO result did not advance beyond the requested checkpoint")
