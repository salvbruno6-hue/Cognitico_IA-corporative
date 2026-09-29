"""Candidate-only refinements observed from Hermes Agent v0.21.x.

These are refinements of existing ELO owners, not new capabilities or authorities.
The contracts are side-effect free and do not invoke Hermes or execute business work.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class HermesRefinement:
    refinement_id: str
    parent_capability: str
    mechanism: str
    owner: str
    source_revision: str
    candidate_only: bool = True
    canonical_mutation: bool = False


@dataclass(frozen=True, slots=True)
class LiveSteeringObservation:
    refinement_id: str
    parent_execution_id: str
    child_execution_id: str
    directive_id: str
    explicit: bool
    provenance_ref: str


@dataclass(frozen=True, slots=True)
class CronContinuityObservation:
    refinement_id: str
    automation_id: str
    prior_run_ref: str
    continuity_scope: str
    memory_boundary: Literal["bounded", "unbounded"]
    provenance_ref: str


REFINEMENTS = (
    HermesRefinement(
        "REF-MULTIAGENT-LIVE-STEERING-HERMES",
        "EXT-MULTIAGENT-HERMES",
        "live subagent steering",
        "ELO Agent Delegation",
        "hermes-v0.21.0@29112be",
    ),
    HermesRefinement(
        "REF-CRON-CONTINUITY-HERMES",
        "EXT-CRON-HERMES",
        "cron memory and continuity",
        "ELO Workflow/Automation",
        "hermes-v0.21.0@29112be",
    ),
)


def get_refinement(refinement_id: str) -> HermesRefinement:
    for item in REFINEMENTS:
        if item.refinement_id == refinement_id:
            return item
    raise ValueError(f"unknown Hermes refinement: {refinement_id}")


def validate_live_steering(observation: LiveSteeringObservation) -> bool:
    return (
        observation.refinement_id == "REF-MULTIAGENT-LIVE-STEERING-HERMES"
        and bool(observation.parent_execution_id)
        and bool(observation.child_execution_id)
        and bool(observation.directive_id)
        and observation.explicit
        and bool(observation.provenance_ref)
    )


def validate_cron_continuity(observation: CronContinuityObservation) -> bool:
    return (
        observation.refinement_id == "REF-CRON-CONTINUITY-HERMES"
        and bool(observation.automation_id)
        and bool(observation.prior_run_ref)
        and bool(observation.continuity_scope)
        and observation.memory_boundary == "bounded"
        and bool(observation.provenance_ref)
    )


__all__ = [
    "CronContinuityObservation",
    "HermesRefinement",
    "LiveSteeringObservation",
    "REFINEMENTS",
    "get_refinement",
    "validate_cron_continuity",
    "validate_live_steering",
]
