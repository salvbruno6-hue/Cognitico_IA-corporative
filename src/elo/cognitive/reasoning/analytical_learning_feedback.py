"""Governed feedback loop for EAIF observations.

Stages:
1. capture avoided analytical errors and observed divergences;
2. detect recurring divergences and create anti-pattern candidates;
3. route candidates through the existing Symbiont learning/Lab path.

This module never promotes canonical knowledge and never creates a new learning owner.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Iterable, Sequence

from elo.cognitive.learning_memory_router import LearningRequest, MemoryEntry
from elo.cognitive.symbiont_memory_learning_bridge import (
    LearningHandoff,
    LearningLabHandoff,
    SymbiontMemoryLearningBridge,
)
from elo.cognitive.symbionte_lab import SymbiontLabAdapter, SymbiontLabObservation
from .analytical_integrity import IntegrityFinding


class FeedbackOutcome(StrEnum):
    ERROR_AVOIDED = "ERROR_AVOIDED"
    DIVERGENCE_OCCURRED = "DIVERGENCE_OCCURRED"


@dataclass(frozen=True, slots=True)
class AnalyticalFeedbackEvent:
    observation_id: str
    tenant_id: str
    domain: str
    control_id: str
    anti_pattern_code: str
    subject: str
    outcome: FeedbackOutcome
    corrective_action: str
    evidence_ids: tuple[str, ...]
    source_ref: str
    source_commit: str


class AnalyticalFeedbackLedger:
    """Append-only runtime ledger; persistence remains owned by governed learning."""

    def __init__(self) -> None:
        self._events: list[AnalyticalFeedbackEvent] = []
        self._ids: set[str] = set()

    def append(self, event: AnalyticalFeedbackEvent) -> None:
        if event.observation_id in self._ids:
            raise ValueError("duplicate analytical feedback observation")
        self._ids.add(event.observation_id)
        self._events.append(event)

    def events(self) -> tuple[AnalyticalFeedbackEvent, ...]:
        return tuple(self._events)


@dataclass(frozen=True, slots=True)
class AntiPatternCandidate:
    candidate_id: str
    tenant_id: str
    domain: str
    control_id: str
    anti_pattern_code: str
    concept_key: str
    hypothesis: str
    occurrences: int
    divergence_count: int
    avoided_count: int
    evidence_ids: tuple[str, ...]
    source_refs: tuple[str, ...]
    corrective_action: str
    state: str = "CANDIDATE"


def _stable_id(*parts: str) -> str:
    return sha256("|".join(parts).encode("utf-8")).hexdigest()[:24]


def capture_integrity_feedback(
    finding: IntegrityFinding,
    *,
    tenant_id: str,
    domain: str,
    control_id: str,
    corrected_before_output: bool,
    evidence_ids: Sequence[str],
    source_ref: str,
    source_commit: str,
    observation_id: str | None = None,
) -> AnalyticalFeedbackEvent:
    """Classify an integrity finding as avoided error or observed divergence."""
    required = (tenant_id, domain, control_id, source_ref, source_commit)
    if not all(required):
        raise ValueError("feedback requires tenant, domain, control, source and commit")
    if not evidence_ids:
        raise ValueError("feedback requires evidence")
    outcome = (
        FeedbackOutcome.ERROR_AVOIDED
        if corrected_before_output
        else FeedbackOutcome.DIVERGENCE_OCCURRED
    )
    oid = observation_id or _stable_id(
        tenant_id, domain, control_id, finding.code, source_ref, outcome.value
    )
    return AnalyticalFeedbackEvent(
        observation_id=oid,
        tenant_id=tenant_id,
        domain=domain,
        control_id=control_id,
        anti_pattern_code=finding.code,
        subject=finding.subject,
        outcome=outcome,
        corrective_action=finding.corrective_action,
        evidence_ids=tuple(dict.fromkeys(evidence_ids)),
        source_ref=source_ref,
        source_commit=source_commit,
    )


def detect_recurring_divergence(
    events: Iterable[AnalyticalFeedbackEvent],
    *,
    minimum_divergences: int = 3,
) -> tuple[AntiPatternCandidate, ...]:
    """Create candidates only from repeated divergence; avoided errors add evidence only."""
    if minimum_divergences < 2:
        raise ValueError("minimum_divergences must be >= 2")
    grouped: dict[tuple[str, str, str, str], list[AnalyticalFeedbackEvent]] = {}
    for event in events:
        key = (event.tenant_id, event.domain, event.control_id, event.anti_pattern_code)
        grouped.setdefault(key, []).append(event)

    candidates: list[AntiPatternCandidate] = []
    for (tenant_id, domain, control_id, code), group in grouped.items():
        divergences = [e for e in group if e.outcome is FeedbackOutcome.DIVERGENCE_OCCURRED]
        if len(divergences) < minimum_divergences:
            continue
        avoided = [e for e in group if e.outcome is FeedbackOutcome.ERROR_AVOIDED]
        evidence_ids = tuple(dict.fromkeys(i for e in group for i in e.evidence_ids))
        source_refs = tuple(dict.fromkeys(e.source_ref for e in group))
        corrective = divergences[-1].corrective_action
        concept_key = f"EAIF::{code}::{control_id}"
        candidates.append(AntiPatternCandidate(
            candidate_id=_stable_id(tenant_id, domain, concept_key),
            tenant_id=tenant_id,
            domain=domain,
            control_id=control_id,
            anti_pattern_code=code,
            concept_key=concept_key,
            hypothesis=(
                f"Recurring analytical divergence {code} under control {control_id}; "
                f"the governed corrective behavior should be reinforced: {corrective}"
            ),
            occurrences=len(group),
            divergence_count=len(divergences),
            avoided_count=len(avoided),
            evidence_ids=evidence_ids,
            source_refs=source_refs,
            corrective_action=corrective,
        ))
    return tuple(candidates)


class EAIFLearningFeedbackBridge:
    """Route recurring anti-pattern candidates into existing governed learning."""

    def __init__(self, bridge: SymbiontMemoryLearningBridge | None = None) -> None:
        self.bridge = bridge or SymbiontMemoryLearningBridge()

    @staticmethod
    def learning_request(candidate: AntiPatternCandidate) -> LearningRequest:
        return LearningRequest(
            learning_id=candidate.candidate_id,
            tenant_scope=candidate.tenant_id,
            domain="EVOLUTION",
            learning_kind="experience",
            concept_key=candidate.concept_key,
            source_refs=candidate.source_refs,
            relation_keys=("EAIF", "ANALYTICAL_ANTI_PATTERN", candidate.anti_pattern_code, candidate.control_id),
            validated=False,
        )

    def route(
        self,
        candidate: AntiPatternCandidate,
        memories: Sequence[MemoryEntry],
    ) -> LearningHandoff:
        return self.bridge.route(self.learning_request(candidate), memories)

    @staticmethod
    def lab_observation(
        candidate: AntiPatternCandidate,
        *,
        source_commit: str,
    ) -> SymbiontLabObservation:
        if not source_commit:
            raise ValueError("source_commit is required")
        return SymbiontLabObservation(
            observation_id=candidate.candidate_id,
            tenant_id=candidate.tenant_id,
            domain="EVOLUTION",
            decision_id=candidate.candidate_id,
            expected_outcome="EAIF control remains conformant across repeated analytical contexts",
            observed_outcome=(
                f"{candidate.divergence_count} divergences across {candidate.occurrences} observations"
            ),
            evidence_ids=candidate.evidence_ids,
            source_ref=candidate.source_refs[-1],
            source_commit=source_commit,
            hypothesis=candidate.hypothesis,
            baseline="analytical control expected to prevent the recurring divergence",
            experiment="evaluate repeated EAIF observations and corrective behavior",
            result=candidate.corrective_action,
            regression_status="NO_REGRESSION",
            generalization_status="PARTIAL",
            risk="MEDIUM",
            existing_owner=None,
            scope="EAIF_ANALYTICAL_ANTI_PATTERN",
            tenant_scope=candidate.tenant_id,
            source_kind="experience",
        )

    def route_to_governed_learning(
        self,
        candidate: AntiPatternCandidate,
        memories: Sequence[MemoryEntry],
        *,
        laboratory: SymbiontLabAdapter,
        principal_id: str,
        dataset_version: str,
        source_commit: str,
    ) -> LearningLabHandoff:
        observation = self.lab_observation(candidate, source_commit=source_commit)
        return self.bridge.route_to_lab(
            self.learning_request(candidate),
            memories,
            observation=observation,
            laboratory=laboratory,
            principal_id=principal_id,
            dataset_version=dataset_version,
        )


__all__ = [
    "AnalyticalFeedbackEvent",
    "AnalyticalFeedbackLedger",
    "AntiPatternCandidate",
    "EAIFLearningFeedbackBridge",
    "FeedbackOutcome",
    "capture_integrity_feedback",
    "detect_recurring_divergence",
]
