"""Controlled evaluation of Hermes profile boundary."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_profile_boundary import ProfileDisposition, ProfileSignal, assess_profile

@dataclass(frozen=True)
class ProfileEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _signals(prefix):
    return tuple(ProfileSignal(
        profile_id=f"{prefix}-{i}", tenant_scope="multiteiner",
        source_refs=(f"hermes:profile:{prefix.lower()}/{i}",),
        identity_digest=f"id-{i}", isolated_state=True,
        explicit_activation=True, shared_canonical_memory=False,
        authority_transfer=False
    ) for i in range(1,6))

def _rate(signals):
    return sum(assess_profile(s).disposition is ProfileDisposition.CANDIDATE for s in signals)/len(signals)

def _integrity(signals):
    return sum((a:=assess_profile(s)).canonical_authority is False and a.execution_permitted is False and a.promotion_permitted is False for s in signals)/len(signals)

def evaluate():
    baseline=_signals("BASE"); adapted=_signals("HERMES")
    b=_rate(baseline); a=_rate(adapted); i=_integrity(adapted)
    repeatable=_rate(_signals("REPEAT"))==a and i==1.0
    result="EVOLUTION_GATE_REQUIRED" if a>b and repeatable else "RETEST"
    return ProfileEvaluation(b,a,i,repeatable,result)
