"""Controlled evaluation of EXT-CRON-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_cron_boundary import ScheduleDisposition,ScheduleSignal,assess_schedule

CAPABILITY_ID="EXT-CRON-HERMES"; PRIMARY_METRIC="authorized_idempotent_schedule_recognition_rate"; METRIC_DIRECTION="maximize"

@dataclass(frozen=True)
class CronEvaluation:
    baseline_rate:float; adapted_rate:float; boundary_integrity_rate:float; repeatable:bool; result:str

def _signals(prefix):
    return tuple(ScheduleSignal(f"{prefix}-{i}","multiteiner",f"task-{i}",(f"hermes:cron:{prefix.lower()}/{i}",),"0 8 * * *","elo",True,True,True,False) for i in range(1,6))
def _rate(s): return sum(assess_schedule(x).disposition is ScheduleDisposition.CANDIDATE for x in s)/len(s)
def _integrity(s): return sum((a:=assess_schedule(x)).canonical_authority is False and a.execution_permitted is False for x in s)/len(s)
def evaluate():
    b=_rate(_signals("BASE")); a=_rate(_signals("HERMES")); i=_integrity(_signals("HERMES"))
    repeatable=_rate(_signals("REPEAT"))==a and i==1.0
    return CronEvaluation(b,a,i,repeatable,"EVOLUTION_GATE_REQUIRED" if a>b and repeatable else "RETEST")
