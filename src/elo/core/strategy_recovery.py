"""Provider-neutral strategic recovery lens.

The lens does not execute business actions and does not create a second decision
authority. It evaluates a resolved situation and identifies how the enterprise
can convert the resolution into forward movement, including recovery, reversal,
protection and opportunity paths.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class StrategicPath(str, Enum):
    ADVANCE = "ADVANCE"
    RECOVER = "RECOVER"
    REVERSE = "REVERSE"
    PROTECT = "PROTECT"
    EXPLOIT = "EXPLOIT"
    HANDOFF = "HANDOFF"


@dataclass(frozen=True)
class StrategicRecoveryAssessment:
    situation: str
    resolution: str
    objective: str
    residual_risks: tuple[str, ...]
    strategic_paths: tuple[StrategicPath, ...]
    recommended_path: StrategicPath
    next_move: str
    trigger: str
    authority_required: bool


def assess_resolution_for_forward_strategy(
    *,
    situation: str,
    resolution: str,
    objective: str,
    residual_risks: Iterable[str] = (),
    recovery_possible: bool = True,
    reversal_warranted: bool = False,
    opportunity_present: bool = False,
    authority_available: bool = False,
) -> StrategicRecoveryAssessment:
    """Turn a resolved situation into an explicit forward-strategy assessment.

    Resolution is treated as a checkpoint, not the end of analysis. The function
    compares the residual state against the objective and produces bounded paths.
    It never authorizes or performs execution.
    """
    risks = tuple(str(item) for item in residual_risks if str(item).strip())
    paths: list[StrategicPath] = []

    if reversal_warranted:
        paths.append(StrategicPath.REVERSE)
    if recovery_possible and risks:
        paths.append(StrategicPath.RECOVER)
    if opportunity_present:
        paths.append(StrategicPath.EXPLOIT)
    if risks:
        paths.append(StrategicPath.PROTECT)
    paths.append(StrategicPath.ADVANCE)

    if not authority_available and (risks or reversal_warranted or opportunity_present):
        paths.append(StrategicPath.HANDOFF)

    if reversal_warranted:
        recommended = StrategicPath.REVERSE
        next_move = "reassess the failed or changed assumption, preserve the current evidence, and select the safest viable route toward the objective"
        trigger = "the current route is no longer the best supported path"
    elif risks:
        recommended = StrategicPath.RECOVER
        next_move = "close the highest-impact residual risk, then re-evaluate the path against the objective"
        trigger = "residual risk can materially prevent the objective"
    elif opportunity_present:
        recommended = StrategicPath.EXPLOIT
        next_move = "evaluate the opportunity against capacity, risk, evidence and authority before committing resources"
        trigger = "the resolution creates a validated opportunity with bounded downside"
    else:
        recommended = StrategicPath.ADVANCE
        next_move = "advance toward the objective while monitoring outcome signals and preserving rollback criteria"
        trigger = "the resolution is stable and evidence supports continuation"

    return StrategicRecoveryAssessment(
        situation=situation,
        resolution=resolution,
        objective=objective,
        residual_risks=risks,
        strategic_paths=tuple(dict.fromkeys(paths)),
        recommended_path=recommended,
        next_move=next_move,
        trigger=trigger,
        authority_required=not authority_available,
    )
