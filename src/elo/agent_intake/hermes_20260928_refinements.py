"""Candidate-only refinements discovered in Hermes 0.21.x.

These contracts reuse existing ELO owners. They do not execute Hermes,
create authority, persist memory, schedule work, or promote candidates.
"""
from dataclasses import dataclass
from enum import Enum

class RefinementDisposition(str, Enum):
    CANDIDATE = "CANDIDATE"
    REJECTED = "REJECTED"

@dataclass(frozen=True)
class LiveSteeringSignal:
    signal_id: str
    parent_execution_id: str
    child_agent_id: str
    directive: str
    explicit: bool
    provenance_ref: str

@dataclass(frozen=True)
class CronContinuitySignal:
    signal_id: str
    automation_id: str
    prior_run_ref: str
    continuity_scope: str
    explicit: bool
    provenance_ref: str

def assess_live_steering(signal: LiveSteeringSignal) -> RefinementDisposition:
    required = (signal.signal_id, signal.parent_execution_id, signal.child_agent_id, signal.directive, signal.provenance_ref)
    return RefinementDisposition.CANDIDATE if signal.explicit and all(required) else RefinementDisposition.REJECTED

def assess_cron_continuity(signal: CronContinuitySignal) -> RefinementDisposition:
    required = (signal.signal_id, signal.automation_id, signal.prior_run_ref, signal.continuity_scope, signal.provenance_ref)
    return RefinementDisposition.CANDIDATE if signal.explicit and all(required) else RefinementDisposition.REJECTED
