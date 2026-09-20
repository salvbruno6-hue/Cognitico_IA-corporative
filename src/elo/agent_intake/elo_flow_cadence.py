"""Deterministic cadence map for composing existing ELO flows.

This module is a routing contract, not a new governance engine. It answers:
"given the completed step and its governed outcome, which existing flow should
be invoked next?" Approval, promotion, merge and learning authorities remain
where they already live.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CadenceOutcome(str, Enum):
    PASS = "PASS"
    RETEST = "RETEST"
    BLOCKED = "BLOCKED"
    REJECT = "REJECT"
    APPROVED = "APPROVED"
    AUTHORIZED = "AUTHORIZED"


@dataclass(frozen=True, slots=True)
class FlowLink:
    current: str
    outcome: CadenceOutcome
    next_flow: str | None
    reason: str


# Existing canonical flow stages are referenced by ID; this table does not
# create a competing state machine.
FLOW_CADENCE: tuple[FlowLink, ...] = (
    FlowLink("OBJECTIVE", CadenceOutcome.PASS, "DECOMPOSE", "objective accepted"),
    FlowLink("DECOMPOSE", CadenceOutcome.PASS, "EXECUTE", "scope decomposed"),
    FlowLink("EXECUTE", CadenceOutcome.PASS, "VALIDATE", "execution produced evidence"),
    FlowLink("VALIDATE", CadenceOutcome.PASS, "SPECIALIST_REVIEW", "validation passed"),
    FlowLink("SPECIALIST_REVIEW", CadenceOutcome.PASS, "ELO_REVIEW", "specialist evidence complete"),
    FlowLink("ELO_REVIEW", CadenceOutcome.APPROVED, "COGNITIVE_MERGE", "ELO review explicitly approved"),
    FlowLink("ELO_REVIEW", CadenceOutcome.RETEST, "CORRECT_REPLAN", "evidence requires correction"),
    FlowLink("CORRECT_REPLAN", CadenceOutcome.PASS, "REVALIDATE", "correction/replan completed"),
    FlowLink("REVALIDATE", CadenceOutcome.PASS, "COGNITIVE_MERGE", "revalidation passed"),
    FlowLink("COGNITIVE_MERGE", CadenceOutcome.APPROVED, "GOVERNANCE", "cognitive merge approved"),
    FlowLink("GOVERNANCE", CadenceOutcome.PASS, "VIRTUAL_LABORATORY", "governance gates passed"),
    FlowLink("VIRTUAL_LABORATORY", CadenceOutcome.PASS, "APPROVE_COMMIT", "laboratory evidence passed"),
    FlowLink("APPROVE_COMMIT", CadenceOutcome.APPROVED, "COMMIT", "commit explicitly authorized"),
    FlowLink("COMMIT", CadenceOutcome.PASS, "VERIFY", "commit created"),
    FlowLink("VERIFY", CadenceOutcome.PASS, "PR", "commit verified"),
    FlowLink("PR", CadenceOutcome.PASS, "APPROVE_MERGE", "PR evidence complete"),
    FlowLink("APPROVE_MERGE", CadenceOutcome.APPROVED, "GIT_MERGE", "merge explicitly authorized"),
    FlowLink("GIT_MERGE", CadenceOutcome.PASS, "POST_MERGE_VERIFY", "merge completed"),
    FlowLink("POST_MERGE_VERIFY", CadenceOutcome.PASS, "LEARN", "post-merge verification passed"),
    FlowLink("LEARN", CadenceOutcome.PASS, "REPORT", "outcome captured"),
    FlowLink("REPORT", CadenceOutcome.PASS, "OBJECTIVE", "closed-loop return"),
    # Hermes implementation branch: existing implementation-loop stages.
    FlowLink("CANDIDATE", CadenceOutcome.PASS, "CONTROLLED_TEST", "candidate entry evidence complete"),
    FlowLink("CONTROLLED_TEST", CadenceOutcome.PASS, "MEASURED_GAIN", "controlled test passed"),
    FlowLink("MEASURED_GAIN", CadenceOutcome.PASS, "REPEATABLE", "positive gain measured"),
    FlowLink("REPEATABLE", CadenceOutcome.PASS, "ELO_REVIEW", "gain is repeatable"),
    FlowLink("ELO_REVIEW", CadenceOutcome.AUTHORIZED, "IMPLEMENTATION_AUTHORIZED", "ELO implementation authorization is explicit"),
)


class FlowCadence:
    """Resolve the next existing flow from a completed governed step."""

    def __init__(self, links: tuple[FlowLink, ...] = FLOW_CADENCE) -> None:
        self._links = links

    def next(self, current: str, outcome: CadenceOutcome) -> FlowLink | None:
        matches = [link for link in self._links if link.current == current and link.outcome == outcome]
        if len(matches) > 1:
            raise ValueError(f"ambiguous cadence for {current}/{outcome}")
        return matches[0] if matches else None

    def require_next(self, current: str, outcome: CadenceOutcome) -> FlowLink:
        link = self.next(current, outcome)
        if link is None:
            raise ValueError(f"no governed next flow for {current}/{outcome}")
        return link


__all__ = ["CadenceOutcome", "FlowLink", "FLOW_CADENCE", "FlowCadence"]
