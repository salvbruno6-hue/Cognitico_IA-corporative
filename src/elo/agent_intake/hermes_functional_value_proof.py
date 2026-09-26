"""Structured functional-value evidence for governed Hermes handoff."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

EvidenceLevel = Literal["CONTRACT_ONLY","IMPLEMENTATION_BOUNDARY","FUNCTIONAL_CONTROLLED_GAIN","OPERATIONAL_OUTCOME"]
Attribution = Literal["CANDIDATE_ATTRIBUTED","OWNER_ATTRIBUTED","BOUNDARY_ATTRIBUTED","NO_INCREMENTAL_GAIN"]

@dataclass(frozen=True, slots=True)
class FunctionalValueEvidence:
    candidate_id: str
    level: EvidenceLevel
    baseline: float
    adapted: float
    metric: str
    direction: str
    repeatable: bool
    regressions: tuple[str, ...]
    attribution: Attribution
    proof_scope: str
    provenance_refs: tuple[str, ...]
    production_proven: bool = False

    @property
    def gain(self) -> float:
        return round((self.baseline - self.adapted) if self.direction == "minimize" else (self.adapted - self.baseline), 6)

    @property
    def functional_gain_proven(self) -> bool:
        return (
            self.level in {"FUNCTIONAL_CONTROLLED_GAIN", "OPERATIONAL_OUTCOME"}
            and self.gain > 0 and self.repeatable and not self.regressions
            and self.attribution == "CANDIDATE_ATTRIBUTED"
            and bool(self.metric) and bool(self.proof_scope)
            and bool(self.provenance_refs)
        )

def classify(candidate_id: str, *, baseline: float, adapted: float, metric: str,
             direction: str, repeatable: bool, regressions: tuple[str, ...],
             attribution: Attribution, proof_scope: str,
             provenance_refs: tuple[str, ...], production_proven: bool = False,
             contract_only: bool = False) -> FunctionalValueEvidence:
    positive = ((direction == "minimize" and adapted < baseline) or
                (direction != "minimize" and adapted > baseline))
    if production_proven:
        level: EvidenceLevel = "OPERATIONAL_OUTCOME"
    elif not contract_only and repeatable and not regressions and positive and attribution == "CANDIDATE_ATTRIBUTED" and provenance_refs:
        level = "FUNCTIONAL_CONTROLLED_GAIN"
    elif contract_only:
        level = "CONTRACT_ONLY"
    else:
        level = "IMPLEMENTATION_BOUNDARY"
    return FunctionalValueEvidence(candidate_id, level, baseline, adapted, metric, direction,
                                   repeatable, regressions, attribution, proof_scope,
                                   provenance_refs, production_proven)

CURRENT_EVIDENCE = (
    classify("EXT-CONTEXT-PLUGIN-HERMES", baseline=0.0, adapted=1.0, metric="task_success_rate", direction="maximize", repeatable=True, regressions=(), attribution="CANDIDATE_ATTRIBUTED", proof_scope="controlled context-resolution task; plugin context source changes task success", provenance_refs=("controlled-eval:context-plugin/1","controlled-eval:context-plugin/2")),
    classify("EXT-HOOK-HERMES", baseline=0.0, adapted=1.0, metric="lifecycle_guardrail_detection_rate", direction="maximize", repeatable=True, regressions=(), attribution="CANDIDATE_ATTRIBUTED", proof_scope="controlled lifecycle guardrail detection task", provenance_refs=("controlled-eval:hook/1","controlled-eval:hook/2","controlled-eval:hook/3","controlled-eval:hook/4","controlled-eval:hook/5")),
    classify("EXT-CHECKPOINT-HERMES", baseline=0.0, adapted=1.0, metric="state_recovery_success_rate", direction="maximize", repeatable=True, regressions=(), attribution="OWNER_ATTRIBUTED", proof_scope="existing ELO State Recovery owner; Hermes candidate-specific effect is not isolated", provenance_refs=("controlled-eval:checkpoint/owner-recovery",)),
    classify("EXT-PROMPT-CACHE-HERMES", baseline=0.40, adapted=1.0, metric="cache_boundary_integrity_rate", direction="maximize", repeatable=True, regressions=(), attribution="BOUNDARY_ATTRIBUTED", proof_scope="cache decision fixtures; no real cache or user task execution", provenance_refs=("controlled-eval:prompt-cache/boundary",), contract_only=True),
    classify("EXT-WORKTREE-HERMES", baseline=0.0, adapted=1.0, metric="bounded_workspace_integrity_rate", direction="maximize", repeatable=True, regressions=(), attribution="BOUNDARY_ATTRIBUTED", proof_scope="isolated workspace contract integrity", provenance_refs=("controlled-eval:worktree/boundary",), contract_only=True),
    classify("EXT-MULTIAGENT-HERMES", baseline=0.0, adapted=1.0, metric="bounded_delegation_contract_integrity_rate", direction="maximize", repeatable=True, regressions=(), attribution="BOUNDARY_ATTRIBUTED", proof_scope="delegation contract only; no child execution", provenance_refs=("controlled-eval:multiagent/boundary",), contract_only=True),
    classify("EXT-CRON-HERMES", baseline=0.0, adapted=1.0, metric="bounded_schedule_registration_integrity_rate", direction="maximize", repeatable=True, regressions=(), attribution="BOUNDARY_ATTRIBUTED", proof_scope="schedule contract only; no scheduler runtime", provenance_refs=("controlled-eval:cron/boundary",), contract_only=True),
    classify("EXT-MEMPROVIDER-HERMES", baseline=0.0, adapted=1.0, metric="bounded_memory_provider_request_integrity_rate", direction="maximize", repeatable=True, regressions=(), attribution="BOUNDARY_ATTRIBUTED", proof_scope="retrieval request contract only; no provider runtime", provenance_refs=("controlled-eval:memprovider/boundary",), contract_only=True),
    classify("EXT-ROUTE-HERMES", baseline=0.0, adapted=1.0, metric="bounded_routing_plan_integrity_rate", direction="maximize", repeatable=True, regressions=(), attribution="BOUNDARY_ATTRIBUTED", proof_scope="routing plan contract only; no live provider selection", provenance_refs=("controlled-eval:route/boundary",), contract_only=True),
    classify("EXT-PROFILE-HERMES", baseline=0.0, adapted=1.0, metric="bounded_profile_isolation_integrity_rate", direction="maximize", repeatable=True, regressions=(), attribution="BOUNDARY_ATTRIBUTED", proof_scope="isolated profile descriptor only; no runtime activation", provenance_refs=("controlled-eval:profile/boundary",), contract_only=True),
    classify("EXT-BATCH-HERMES", baseline=0.0, adapted=1.0, metric="bounded_batch_intake_integrity_rate", direction="maximize", repeatable=True, regressions=(), attribution="BOUNDARY_ATTRIBUTED", proof_scope="bounded batch intake contract only; no execution", provenance_refs=("controlled-eval:batch/boundary",), contract_only=True),
    classify("EXT-LEARN-HERMES", baseline=0.0, adapted=1.0, metric="bounded_skill_learning_candidate_integrity_rate", direction="maximize", repeatable=True, regressions=(), attribution="BOUNDARY_ATTRIBUTED", proof_scope="candidate skill admission only; no autonomous promotion", provenance_refs=("controlled-eval:learn/boundary",), contract_only=True),
    classify("EXT-LEARNING-GRAPH-HERMES", baseline=1.0, adapted=1.0, metric="relation_validation_rate", direction="maximize", repeatable=True, regressions=(), attribution="NO_INCREMENTAL_GAIN", proof_scope="relation validation already accepts valid evidence-linked relations", provenance_refs=("controlled-eval:learning-graph/no-gain",), contract_only=True),
    classify("EXT-CONTEXTREF-HERMES", baseline=1.0, adapted=1.0, metric="reference_parse_success_rate", direction="maximize", repeatable=True, regressions=(), attribution="NO_INCREMENTAL_GAIN", proof_scope="parser recognition unchanged before and after", provenance_refs=("controlled-eval:contextref/no-gain",), contract_only=True),
)

HOOK_EVIDENCE = next(item for item in CURRENT_EVIDENCE if item.candidate_id == "EXT-HOOK-HERMES")

def functional_candidates() -> tuple[FunctionalValueEvidence, ...]:
    return tuple(item for item in CURRENT_EVIDENCE if item.functional_gain_proven)

__all__ = ["Attribution","EvidenceLevel","FunctionalValueEvidence","CURRENT_EVIDENCE","classify","functional_candidates","HOOK_EVIDENCE"]
