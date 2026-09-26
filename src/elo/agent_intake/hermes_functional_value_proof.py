"""Structured functional-value evidence for governed Hermes handoff.

A caller cannot promote a candidate by asserting a boolean. The handoff must
receive evidence whose validity is derived from candidate attribution, positive
task-level gain, repeatability, provenance, and regression absence.
"""
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
            and self.attribution == "CANDIDATE_ATTRIBUTED" and bool(self.provenance_refs)
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

HOOK_EVIDENCE = classify(
    "EXT-HOOK-HERMES",
    baseline=0.0,
    adapted=1.0,
    metric="lifecycle_guardrail_detection_rate",
    direction="maximize",
    repeatable=True,
    regressions=(),
    attribution="CANDIDATE_ATTRIBUTED",
    proof_scope="controlled lifecycle guardrail detection task",
    provenance_refs=("controlled-eval:hook/1", "controlled-eval:hook/2", "controlled-eval:hook/3", "controlled-eval:hook/4", "controlled-eval:hook/5"),
)

__all__ = ["Attribution","EvidenceLevel","FunctionalValueEvidence","classify","HOOK_EVIDENCE"]
