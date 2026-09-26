"""Functional-value evidence classification for Hermes candidates.

Separates contract integrity from candidate-attributed functional gain.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

EvidenceLevel = Literal['CONTRACT_ONLY','IMPLEMENTATION_BOUNDARY','FUNCTIONAL_CONTROLLED_GAIN','OPERATIONAL_OUTCOME']

@dataclass(frozen=True, slots=True)
class FunctionalValueEvidence:
    candidate_id: str
    level: EvidenceLevel
    baseline: float | None
    adapted: float | None
    gain: float | None
    attribution: str
    proof_scope: str
    production_proven: bool = False

    @property
    def functional_gain_proven(self) -> bool:
        return self.level in {'FUNCTIONAL_CONTROLLED_GAIN','OPERATIONAL_OUTCOME'} and self.gain is not None and self.gain > 0 and self.attribution == 'CANDIDATE_ATTRIBUTED'

def classify(candidate_id: str, *, baseline: float | None, adapted: float | None, attribution: str, proof_scope: str, contract_only: bool=False, operational: bool=False) -> FunctionalValueEvidence:
    gain = None if baseline is None or adapted is None else round(adapted - baseline, 6)
    if operational and gain is not None and gain > 0: level = 'OPERATIONAL_OUTCOME'
    elif not contract_only and gain is not None and gain > 0 and attribution == 'CANDIDATE_ATTRIBUTED': level = 'FUNCTIONAL_CONTROLLED_GAIN'
    elif contract_only: level = 'CONTRACT_ONLY'
    else: level = 'IMPLEMENTATION_BOUNDARY'
    return FunctionalValueEvidence(candidate_id, level, baseline, adapted, gain, attribution, proof_scope, operational)

CURRENT_EVIDENCE = (
    classify('EXT-CONTEXT-PLUGIN-HERMES', baseline=0.0, adapted=1.0, attribution='CANDIDATE_ATTRIBUTED', proof_scope='controlled context-resolution task; plugin context source changes task success'),
    classify('EXT-CHECKPOINT-HERMES', baseline=0.0, adapted=1.0, attribution='OWNER_ATTRIBUTED', proof_scope='recovery harness invokes existing ELO State Recovery; candidate-specific effect is not isolated'),
    classify('EXT-PROMPT-CACHE-HERMES', baseline=0.40, adapted=1.0, attribution='BOUNDARY_ATTRIBUTED', proof_scope='cache decision fixtures; no real cache or user task execution', contract_only=True),
    classify('EXT-WORKTREE-HERMES', baseline=0.0, adapted=1.0, attribution='BOUNDARY_ATTRIBUTED', proof_scope='isolated workspace contract integrity', contract_only=True),
    classify('EXT-MULTIAGENT-HERMES', baseline=0.0, adapted=1.0, attribution='BOUNDARY_ATTRIBUTED', proof_scope='delegation contract only; no child execution', contract_only=True),
    classify('EXT-CRON-HERMES', baseline=0.0, adapted=1.0, attribution='BOUNDARY_ATTRIBUTED', proof_scope='schedule contract only; no scheduler runtime', contract_only=True),
    classify('EXT-MEMPROVIDER-HERMES', baseline=0.0, adapted=1.0, attribution='BOUNDARY_ATTRIBUTED', proof_scope='retrieval request contract only; no provider runtime', contract_only=True),
    classify('EXT-ROUTE-HERMES', baseline=0.0, adapted=1.0, attribution='BOUNDARY_ATTRIBUTED', proof_scope='routing plan contract only; no live provider selection', contract_only=True),
    classify('EXT-PROFILE-HERMES', baseline=0.0, adapted=1.0, attribution='BOUNDARY_ATTRIBUTED', proof_scope='isolated profile descriptor only; no runtime activation', contract_only=True),
    classify('EXT-BATCH-HERMES', baseline=0.0, adapted=1.0, attribution='BOUNDARY_ATTRIBUTED', proof_scope='bounded batch intake contract only; no execution', contract_only=True),
    classify('EXT-LEARN-HERMES', baseline=0.0, adapted=1.0, attribution='BOUNDARY_ATTRIBUTED', proof_scope='candidate skill admission only; no autonomous promotion', contract_only=True),
    classify('EXT-LEARNING-GRAPH-HERMES', baseline=1.0, adapted=1.0, attribution='NO_INCREMENTAL_GAIN', proof_scope='relation validation already accepts valid evidence-linked relations', contract_only=True),
    classify('EXT-CONTEXTREF-HERMES', baseline=1.0, adapted=1.0, attribution='NO_INCREMENTAL_GAIN', proof_scope='parser recognition unchanged before and after', contract_only=True),
)

def functional_candidates() -> tuple[FunctionalValueEvidence, ...]:
    return tuple(item for item in CURRENT_EVIDENCE if item.functional_gain_proven)

__all__ = ["EvidenceLevel","FunctionalValueEvidence","CURRENT_EVIDENCE","classify","functional_candidates"]