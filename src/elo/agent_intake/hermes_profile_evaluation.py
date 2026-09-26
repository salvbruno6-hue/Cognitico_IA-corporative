"""Controlled three-phase evaluation of EXT-PROFILE-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_profile_adapter import adapt_profile
from .hermes_profile_boundary import ProfileDisposition, ProfileSignal

CAPABILITY_ID="EXT-PROFILE-HERMES"
PRIMARY_METRIC="bounded_profile_isolation_integrity_rate"
METRIC_DIRECTION="maximize"

@dataclass(frozen=True, slots=True)
class ProfileEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _signals(prefix: str):
    return tuple(ProfileSignal(f"{prefix}-{i}","multiteiner",(f"hermes:profile:{prefix.lower()}/{i}",),f"id-{i}",True,True,False,False) for i in range(1,6))

def _integrity(contracts):
    return sum(c is not None and c.disposition is ProfileDisposition.CANDIDATE
               and not c.shared_canonical_memory and not c.authority_transfer
               and not c.execution_permitted and not c.promotion_permitted for c in contracts)/len(contracts)

def evaluate():
    baseline=0.0
    adapted_contracts=tuple(adapt_profile(s) for s in _signals("HERMES"))
    repeat_contracts=tuple(adapt_profile(s) for s in _signals("REPEAT"))
    adapted=sum(c is not None for c in adapted_contracts)/len(adapted_contracts)
    integrity=_integrity(adapted_contracts)
    repeatable=sum(c is not None for c in repeat_contracts)/len(repeat_contracts)==adapted and _integrity(repeat_contracts)==1.0
    result="EVOLUTION_GATE_REQUIRED" if adapted>baseline and repeatable and integrity==1.0 else "RETEST"
    return ProfileEvaluation(baseline,adapted,integrity,repeatable,result)
