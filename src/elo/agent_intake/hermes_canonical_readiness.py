"""Evidence-only readiness evaluation for Hermes -> ELO candidate mechanisms.

This module is intentionally not a promotion engine. It evaluates whether an
independently supplied evidence package is complete enough for Evolution Gate
review. Canonical mutation is never permitted here.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class Readiness(str, Enum):
    GREEN_READY_FOR_EVOLUTION_GATE = "GREEN_READY_FOR_EVOLUTION_GATE"
    YELLOW_EVIDENCE_PENDING = "YELLOW_EVIDENCE_PENDING"
    RED_REJECTED = "RED_REJECTED"

@dataclass(frozen=True)
class HermesReadinessEvidence:
    candidate_id: str
    owner: str
    baseline_id: Optional[str] = None
    experiment_id: Optional[str] = None
    metric: Optional[str] = None
    baseline_value: Optional[float] = None
    candidate_value: Optional[float] = None
    metric_direction: Optional[str] = None
    repeatability_runs: int = 0
    repeatability_passed: bool = False
    security_verified: bool = False
    isolation_verified: bool = False
    authority_conflict: bool = False
    evolution_gate: Optional[str] = None
    approval_ref: Optional[str] = None
    promotion_package_ref: Optional[str] = None

HERMES_EVALUATED_CAPABILITIES = (
    "EXT-CONTEXTREF-HERMES", "EXT-CHECKPOINT-HERMES", "EXT-HOOK-HERMES",
    "EXT-ROUTE-HERMES", "EXT-PROFILE-HERMES", "EXT-BATCH-HERMES",
    "EXT-MEMPROVIDER-HERMES", "EXT-LEARN-HERMES",
    "EXT-LEARNING-GRAPH-HERMES", "EXT-CONTEXT-PLUGIN-HERMES",
    "EXT-WORKTREE-HERMES", "EXT-MULTIAGENT-HERMES", "EXT-CRON-HERMES",
    "EXT-CURATOR-HERMES",
)
_REQUIRED_TEXT = ("candidate_id", "owner", "baseline_id", "experiment_id", "metric")

def _complete_identity(evidence: HermesReadinessEvidence) -> bool:
    return all(bool(getattr(evidence, field)) for field in _REQUIRED_TEXT)

def _measurable_gain(evidence: HermesReadinessEvidence) -> bool:
    if evidence.baseline_value is None or evidence.candidate_value is None:
        return False
    if evidence.metric_direction == "higher":
        return evidence.candidate_value > evidence.baseline_value
    if evidence.metric_direction == "lower":
        return evidence.candidate_value < evidence.baseline_value
    return False

def evaluate_readiness(evidence: HermesReadinessEvidence) -> Readiness:
    if evidence.candidate_id not in HERMES_EVALUATED_CAPABILITIES:
        return Readiness.RED_REJECTED
    if evidence.authority_conflict:
        return Readiness.RED_REJECTED
    if not _complete_identity(evidence):
        return Readiness.YELLOW_EVIDENCE_PENDING
    if (evidence.repeatability_runs < 2 or not evidence.repeatability_passed
        or not _measurable_gain(evidence) or not evidence.security_verified
        or not evidence.isolation_verified):
        return Readiness.YELLOW_EVIDENCE_PENDING
    if evidence.evolution_gate != "PASS":
        return Readiness.YELLOW_EVIDENCE_PENDING
    if not evidence.approval_ref or not evidence.promotion_package_ref:
        return Readiness.YELLOW_EVIDENCE_PENDING
    return Readiness.GREEN_READY_FOR_EVOLUTION_GATE

def canonical_mutation_permitted(_: HermesReadinessEvidence) -> bool:
    return False