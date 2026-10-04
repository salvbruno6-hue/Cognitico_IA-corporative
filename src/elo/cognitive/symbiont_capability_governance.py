"""Read-only governance orchestration for existing Symbiont capability authorities.

This module composes existing governance read models. It does not create a
new capability owner, Evolution Gate, learning authority, runtime authority,
or promotion path.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from elo.agent_intake.implementation_loop_readiness import LoopReadiness
from elo.agent_intake.symbiont_implementation_view import SymbiontImplementationView
from elo.cognitive.symbiont_capability_evolution import (
    CapabilityEvolutionReview,
    CapabilityStatusReport,
)


@dataclass(frozen=True, slots=True)
class GovernanceRelation:
    source: str
    relation: str
    target: str
    authority: str
    evidence_refs: tuple[str, ...] = ()
    condition: str = ""


@dataclass(frozen=True, slots=True)
class SymbiontGovernanceOrchestration:
    capability_id: str
    status: str
    owner: str
    relations: tuple[GovernanceRelation, ...]
    blockers: tuple[str, ...]
    next_action: str
    canonical_mutation: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "capability_id": self.capability_id,
            "status": self.status,
            "owner": self.owner,
            "relations": [
                {
                    "source": relation.source,
                    "relation": relation.relation,
                    "target": relation.target,
                    "authority": relation.authority,
                    "evidence_refs": list(relation.evidence_refs),
                    "condition": relation.condition,
                }
                for relation in self.relations
            ],
            "blockers": list(self.blockers),
            "next_action": self.next_action,
            "canonical_mutation": self.canonical_mutation,
        }


def orchestrate_capability_governance(
    *,
    implementation_view: SymbiontImplementationView,
    readiness: LoopReadiness,
    evolution_review: CapabilityEvolutionReview,
    status_report: CapabilityStatusReport,
) -> SymbiontGovernanceOrchestration:
    """Compose existing authorities into one deterministic governance view.

    The orchestration order is:
    Symbiont -> canonical capability/owner -> implementation view ->
    readiness/evidence -> capability evolution -> existing Evolution Gate /
    governance decision -> runtime observation.

    This function only describes relationships and next actions. It never
    authorizes any downstream action.
    """
    refs = tuple(dict.fromkeys(status_report.evidence_refs))
    relations: list[GovernanceRelation] = [
        GovernanceRelation(
            source="SIMBIONTE",
            relation="DIAGNOSES",
            target=implementation_view.capability,
            authority="Symbiont read-model",
            evidence_refs=refs,
            condition=status_report.status.value,
        ),
        GovernanceRelation(
            source=implementation_view.capability,
            relation="OWNED_BY",
            target=implementation_view.owner,
            authority="canonical owner resolution",
            evidence_refs=implementation_view.evidence_refs,
            condition=implementation_view.ownership.value,
        ),
        GovernanceRelation(
            source=implementation_view.capability,
            relation="DESCRIBED_BY",
            target="SymbiontImplementationView",
            authority="implementation governance contract",
            evidence_refs=implementation_view.evidence_refs,
            condition=implementation_view.loop_stage,
        ),
        GovernanceRelation(
            source="SymbiontImplementationView",
            relation="FEEDS",
            target="LoopReadiness",
            authority="implementation readiness contract",
            evidence_refs=implementation_view.evidence_refs,
            condition="ready_for_loop=" + str(readiness.ready_for_loop),
        ),
        GovernanceRelation(
            source="LoopReadiness",
            relation="FEEDS",
            target="CapabilityEvolutionReview",
            authority="existing implementation/evolution loop",
            evidence_refs=readiness.missing,
            condition="ready_for_loop=" + str(readiness.ready_for_loop),
        ),
        GovernanceRelation(
            source="CapabilityEvolutionReview",
            relation="OBSERVES",
            target="EVOLUÇÃO_DE_CAPACIDADES",
            authority="existing capability evolution review",
            evidence_refs=evolution_review.evidence_refs,
            condition=evolution_review.status,
        ),
        GovernanceRelation(
            source="CapabilityEvolutionReview",
            relation="HANDOFF_TO",
            target="Evolution Gate",
            authority="existing Evolution Gate",
            evidence_refs=evolution_review.evidence_refs,
            condition="only when existing gate criteria are satisfied",
        ),
        GovernanceRelation(
            source="Evolution Gate",
            relation="GOVERNS",
            target="canonical promotion/merge decision",
            authority="existing Evolution Gate",
            evidence_refs=(),
            condition="explicit authorization required",
        ),
        GovernanceRelation(
            source="canonical runtime",
            relation="EMITS",
            target="RuntimeOperationalEvidence",
            authority="existing runtime evidence boundary",
            evidence_refs=(),
            condition=status_report.status.value,
        ),
    ]

    if not readiness.ready_for_loop:
        blockers = tuple(
            dict.fromkeys(
                (
                    *status_report.blockers,
                    *(f"readiness:{item}" for item in readiness.missing),
                )
            )
        )
    else:
        blockers = status_report.blockers

    return SymbiontGovernanceOrchestration(
        capability_id=status_report.capability_id,
        status=status_report.status.value,
        owner=implementation_view.owner,
        relations=tuple(relations),
        blockers=blockers,
        next_action=status_report.next_action,
        canonical_mutation=False,
    )


__all__ = [
    "GovernanceRelation",
    "SymbiontGovernanceOrchestration",
    "orchestrate_capability_governance",
]
