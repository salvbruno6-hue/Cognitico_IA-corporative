"""Application-facing bridge for the governed ELO chat pre-finalization loop.

This module is deliberately thin. It reuses ObjectiveContinuityAdapter and the
ELO->GPT pre-finalization policy already owned by the cognitive layer. It does
not create a second objective, authorization or persistence authority.

The reference runtime accepts only a durable SQLite path. Production deployments
must replace this reference store behind the same Symbiont execution contract
with a durable backend suitable for the hosting topology.
"""
from __future__ import annotations

import os
from dataclasses import asdict, dataclass

from elo.cognitive.objective_continuity import ObjectiveContinuityAdapter
from elo.cognitive.response.elo_chat_prefinalization import (
    EloChatPreFinalizationLoop,
    EloPreFinalizationRequest,
)
from elo.cognitive.response.elo_gpt_dialogue import (
    AuthorizationState,
    EvidenceState,
    PersistenceState,
)
from elo.cognitive.symbiont_execution import SymbiontExecutionStore
from elo.contracts.okr import Objective


STORE_PATH_ENV = "ELO_SYMBIONT_EXECUTION_STORE_PATH"


@dataclass(frozen=True, slots=True)
class ChatPreFinalizationCommand:
    tenant_id: str
    objective_id: str
    objective_title: str
    workstream_id: str
    expected_checkpoint_version: int | None
    chat_draft: str
    progress_token: str
    evidence_refs: tuple[str, ...]
    proposed_next_action: str
    objective_evidence_refs: tuple[str, ...]
    authorization_state: AuthorizationState
    continuation_permitted: bool
    objective_satisfied: bool = False
    within_scope: bool = True
    authority_available: bool = True
    risk_level: str = "LOW"
    evidence_state: EvidenceState = EvidenceState.OBSERVED
    max_cycles: int = 12


def _durable_store_path() -> str:
    path = os.environ.get(STORE_PATH_ENV, "").strip()
    if not path or path == ":memory:":
        raise RuntimeError(
            "durable Symbiont execution store is not configured; "
            f"set {STORE_PATH_ENV} to a persistent runtime path"
        )
    return path


def run_chat_prefinalization(command: ChatPreFinalizationCommand) -> dict[str, object]:
    if command.authorization_state is not AuthorizationState.VALID and command.continuation_permitted:
        raise ValueError("automatic continuation requires canonical authorization state VALID")
    if not command.objective_evidence_refs:
        raise ValueError("objective_evidence_refs are required")
    if not command.evidence_refs:
        raise ValueError("cycle evidence_refs are required")

    objective = Objective(
        tenant_id=command.tenant_id,
        objective_id=command.objective_id,
        title=command.objective_title,
        evidence_refs=command.objective_evidence_refs,
    )
    store = SymbiontExecutionStore(_durable_store_path())
    try:
        adapter = ObjectiveContinuityAdapter(store)
        checkpoint = adapter.start_or_resume(
            objective,
            workstream_id=command.workstream_id,
            initial_action="CHECK_ELO_BEFORE_FINAL",
            max_cycles=command.max_cycles,
        )
        expected = command.expected_checkpoint_version or checkpoint.state_version
        if checkpoint.state_version != expected:
            raise ValueError(
                f"stale objective checkpoint: expected {expected}, observed {checkpoint.state_version}"
            )

        request = EloPreFinalizationRequest(
            objective_id=command.objective_id,
            workstream_id=command.workstream_id,
            expected_checkpoint_version=expected,
            chat_draft=command.chat_draft,
        )

        def cycle_runner(prefinalization_request: EloPreFinalizationRequest):
            return adapter.record_cycle(
                objective,
                workstream_id=command.workstream_id,
                expected_state_version=prefinalization_request.expected_checkpoint_version,
                progress_token=command.progress_token,
                evidence_refs=command.evidence_refs,
                proposed_next_action=command.proposed_next_action,
                objective_satisfied=command.objective_satisfied,
                within_scope=command.within_scope,
                authority_available=command.authority_available,
                risk_level=command.risk_level,
            )

        result = EloChatPreFinalizationLoop(cycle_runner).run(
            request,
            persistence_state=PersistenceState.PERSISTED,
            authorization_state=command.authorization_state,
            continuation_permitted=command.continuation_permitted,
            evidence_state=command.evidence_state,
        )
        return {
            "final_message": result.final_message,
            "decision": result.elo_reply.decision,
            "next_action": result.elo_reply.next_action,
            "progress_token": result.elo_reply.progress_token,
            "should_continue_automatically": result.elo_reply.should_continue_automatically,
            "human_required": result.elo_reply.human_required,
            "evidence_refs": list(result.elo_reply.evidence_refs),
            "scenario_code": result.elo_reply.scenario_code,
            "replay_count": result.replay_count,
            "next_trigger": asdict(result.next_trigger) if result.next_trigger else None,
        }
    finally:
        store.close()


__all__ = ["ChatPreFinalizationCommand", "STORE_PATH_ENV", "run_chat_prefinalization"]
