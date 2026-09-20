"""Controlled evaluation of EXT-ROUTE-HERMES."""
from dataclasses import dataclass
from .hermes_routing_boundary import RoutingDisposition,RoutingSignal,assess_routing
@dataclass(frozen=True)
class RoutingEvaluation:
    baseline_rate:float; adapted_rate:float; boundary_integrity_rate:float; repeatable:bool; result:str
def _signals(p): return tuple(RoutingSignal(f"{p}-{i}","multiteiner",(f"hermes:routing:{p.lower()}/{i}",),"provider-a",("provider-b",),"bounded-pool-v1",True,True) for i in range(1,6))
def _rate(s): return sum(assess_routing(x).disposition is RoutingDisposition.CANDIDATE for x in s)/len(s)
def _int(s): return sum((a:=assess_routing(x)).canonical_authority is False and a.execution_permitted is False and a.governance_bypass_permitted is False for x in s)/len(s)
def evaluate():
    b=_rate(_signals("BASE"));a=_rate(_signals("HERMES"));i=_int(_signals("HERMES"));r=_rate(_signals("REPEAT"))==a and i==1.0
    return RoutingEvaluation(b,a,i,r,"EVOLUTION_GATE_REQUIRED" if a>b and r else "RETEST")
