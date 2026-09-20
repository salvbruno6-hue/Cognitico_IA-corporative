"""Candidate-only governance boundary for Hermes scheduled tasks."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

CAPABILITY_ID = "EXT-CRON-HERMES"

class ScheduleDisposition(str, Enum):
    OBSERVATION="OBSERVATION"; CANDIDATE="CANDIDATE"; REJECTED="REJECTED"

@dataclass(frozen=True)
class ScheduleSignal:
    schedule_id:str; tenant_scope:str; task_digest:str; source_refs:Tuple[str,...]
    schedule_expression:str; owner_principal:str
    provenance_verified:bool=False; explicit_authorization:bool=False
    idempotent:bool=False; governance_bypass:bool=False

@dataclass(frozen=True)
class ScheduleAssessment:
    schedule_id:str; disposition:ScheduleDisposition; evidence_refs:Tuple[str,...]
    canonical_authority:bool=False; execution_permitted:bool=False

def assess_schedule(signal:ScheduleSignal)->ScheduleAssessment:
    if not signal.schedule_id or not signal.tenant_scope or not signal.task_digest or not signal.owner_principal:
        return ScheduleAssessment(signal.schedule_id,ScheduleDisposition.REJECTED,tuple(signal.source_refs))
    if not signal.source_refs or not signal.provenance_verified or not signal.schedule_expression:
        return ScheduleAssessment(signal.schedule_id,ScheduleDisposition.REJECTED,tuple(signal.source_refs))
    if signal.governance_bypass:
        return ScheduleAssessment(signal.schedule_id,ScheduleDisposition.REJECTED,tuple(signal.source_refs))
    if not signal.explicit_authorization or not signal.idempotent:
        return ScheduleAssessment(signal.schedule_id,ScheduleDisposition.OBSERVATION,tuple(signal.source_refs))
    return ScheduleAssessment(signal.schedule_id,ScheduleDisposition.CANDIDATE,tuple(signal.source_refs))
