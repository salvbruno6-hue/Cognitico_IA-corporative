"""Controlled evaluation of EXT-PROFILE-HERMES."""
from dataclasses import dataclass
from .hermes_profile_boundary import ProfileDisposition,ProfileSignal,assess_profile
@dataclass(frozen=True)
class ProfileEvaluation:
 baseline_rate:float;adapted_rate:float;boundary_integrity_rate:float;repeatable:bool;result:str
def _signals(p): return tuple(ProfileSignal(f"{p}-{i}","multiteiner",(f"hermes:profile:{p.lower()}/{i}",),f"id-{i}",True,True,False,False) for i in range(1,6))
def _rate(s): return sum(assess_profile(x).disposition is ProfileDisposition.CANDIDATE for x in s)/len(s)
def _int(s): return sum((a:=assess_profile(x)).canonical_authority is False and a.execution_permitted is False and a.promotion_permitted is False for x in s)/len(s)
def evaluate():
 b=_rate(_signals("BASE"));a=_rate(_signals("HERMES"));i=_int(_signals("HERMES"));r=_rate(_signals("REPEAT"))==a and i==1.0
 return ProfileEvaluation(b,a,i,r,"EVOLUTION_GATE_REQUIRED" if a>b and r else "RETEST")
