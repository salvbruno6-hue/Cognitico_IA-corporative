"""Process-aware contracts for the original Hermes candidate loop.

This is validation metadata, not a second authority. It describes how each
existing candidate probe must expose its process evidence to the shared loop.
The candidate implementations and the canonical ELO owners remain authoritative.
"""
from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class HermesProcessContract:
    candidate_id: str
    metric: str
    direction: str
    implementation_first: bool = True

    def validate_evidence(self, evidence: object) -> None:
        candidate_id = getattr(evidence, "candidate_id", None)
        if candidate_id != self.candidate_id:
            raise ValueError(
                f"{self.candidate_id}: evidence candidate_id mismatch: {candidate_id!r}"
            )

        baseline = getattr(evidence, "baseline", None)
        adapted = getattr(evidence, "adapted", None)
        directions = getattr(evidence, "metric_directions", None)
        if not isinstance(baseline, dict) or self.metric not in baseline:
            raise ValueError(f"{self.candidate_id}: baseline missing metric {self.metric}")
        if not isinstance(adapted, dict) or self.metric not in adapted:
            raise ValueError(f"{self.candidate_id}: adapted missing metric {self.metric}")
        if not isinstance(directions, dict) or directions.get(self.metric) != self.direction:
            raise ValueError(
                f"{self.candidate_id}: metric direction for {self.metric} "
                f"must be {self.direction}"
            )

        if not bool(getattr(evidence, "repeatable", False)):
            raise ValueError(f"{self.candidate_id}: repeatability evidence is required")
        provenance = getattr(evidence, "provenance_refs", ())
        if not provenance:
            raise ValueError(f"{self.candidate_id}: provenance evidence is required")
        if not bool(getattr(evidence, "boundary_integrity", False)):
            raise ValueError(f"{self.candidate_id}: governance boundary evidence is required")


HERMES_13_PROCESS_CONTRACTS = {
    "EXT-CONTEXT-PLUGIN-HERMES": HermesProcessContract(
        "EXT-CONTEXT-PLUGIN-HERMES", "context_task_success_rate", "maximize"
    ),
    "EXT-WORKTREE-HERMES": HermesProcessContract(
        "EXT-WORKTREE-HERMES", "collision_free_task_rate", "maximize"
    ),
    "EXT-MULTIAGENT-HERMES": HermesProcessContract(
        "EXT-MULTIAGENT-HERMES", "context_isolation_rate", "maximize"
    ),
    "EXT-CRON-HERMES": HermesProcessContract(
        "EXT-CRON-HERMES", "idempotency_collision_free_rate", "maximize"
    ),
    "EXT-MEMPROVIDER-HERMES": HermesProcessContract(
        "EXT-MEMPROVIDER-HERMES", "provider_identity_preservation_rate", "maximize"
    ),
    "EXT-ROUTE-HERMES": HermesProcessContract(
        "EXT-ROUTE-HERMES", "unsafe_route_admission_block_rate", "maximize"
    ),
    "EXT-PROFILE-HERMES": HermesProcessContract(
        "EXT-PROFILE-HERMES", "collision_free_profile_task_rate", "maximize"
    ),
    "EXT-BATCH-HERMES": HermesProcessContract(
        "EXT-BATCH-HERMES", "collision_free_batch_task_rate", "maximize"
    ),
    "EXT-LEARN-HERMES": HermesProcessContract(
        "EXT-LEARN-HERMES", "unsafe_skill_admission_block_rate", "maximize"
    ),
    "EXT-LEARNING-GRAPH-HERMES": HermesProcessContract(
        "EXT-LEARNING-GRAPH-HERMES", "duplicate_relation_block_rate", "maximize"
    ),
    "EXT-CONTEXTREF-HERMES": HermesProcessContract(
        "EXT-CONTEXTREF-HERMES",
        "unsafe_malformed_reference_admission_rate",
        "minimize",
    ),
    "EXT-CHECKPOINT-HERMES": HermesProcessContract(
        "EXT-CHECKPOINT-HERMES", "unsafe_replay_block_rate", "maximize",
        implementation_first=False,
    ),
    "EXT-HOOK-HERMES": HermesProcessContract(
        "EXT-HOOK-HERMES", "lifecycle_guardrail_detection_rate", "maximize"
    ),
}


def get_process_contract(candidate_id: str) -> HermesProcessContract:
    try:
        return HERMES_13_PROCESS_CONTRACTS[candidate_id]
    except KeyError as exc:
        raise ValueError(f"Unknown Hermes 13 candidate: {candidate_id}") from exc


__all__ = ["HermesProcessContract", "HERMES_13_PROCESS_CONTRACTS", "get_process_contract"]
