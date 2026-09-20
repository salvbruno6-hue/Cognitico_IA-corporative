"""Canonical routing composition for ELO flow complementarity.

This is a thin adapter over existing cadence, complementarity and capability
selection contracts. It does not execute flows or grant authorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Mapping

from .flow_complementarity import RelationKind

if TYPE_CHECKING:
    from elo.cognitive.reasoning.capability_selection import (
        CapabilityDecision,
        CapabilityRequirement,
        CapabilitySelector,
    )
from .elo_flow_cadence import CadenceOutcome, FlowCadence
from .flow_complementarity import (
    ComplementarityEngine,
    ConnectionStatus,
    FlowConnectionDecision,
)


@dataclass(frozen=True, slots=True)
class NextFlowResolution:
    """Discovery result for complementary next-flow candidates.

    selected_next is populated only when exactly one eligible candidate
    remains. Ambiguity never becomes an implicit routing decision.
    """

    origin_flow: str
    outcome: CadenceOutcome
    candidates: tuple["RoutingDecision", ...]
    selected_next: str | None
    status: str


@dataclass(frozen=True, slots=True)
class RoutingDecision:
    connection: FlowConnectionDecision
    cadence_next: str | None
    capability: CapabilityDecision | None
    status: str


class GovernedFlowRouter:
    """Resolve an eligible next flow using existing ELO contracts."""

    def __init__(
        self,
        *,
        complementarity: ComplementarityEngine,
        capability_selector: CapabilitySelector | None = None,
        cadence: FlowCadence | None = None,
    ) -> None:
        self._complementarity = complementarity
        self._capability_selector = capability_selector
        self._cadence = cadence or FlowCadence()

    def resolve_next(
        self,
        *,
        origin_flow: str,
        outcome: CadenceOutcome,
        evidence: Mapping[str, object] | None = None,
        provenance_refs: tuple[str, ...] = (),
        relation_kind: RelationKind | None = None,
        capability_requirement: CapabilityRequirement | None = None,
    ) -> NextFlowResolution:
        """Discover the governed next flow without executing or authorizing it.

        Candidate relations come only from the explicit complementarity set.
        Cadence remains the deterministic next-step constraint; a complementary
        relation that disagrees with cadence is never selected.
        """
        cadence_link = self._cadence.next(origin_flow, outcome)
        if cadence_link is None or cadence_link.next_flow is None:
            return NextFlowResolution(origin_flow, outcome, (), None, "WAITING")

        candidates: list[RoutingDecision] = []
        for relation in self._complementarity.candidate_relations(origin_flow):
            if relation_kind is not None and relation.kind is not relation_kind:
                continue
            candidates.append(
                self.resolve(
                    origin_flow=origin_flow,
                    target_flow=relation.target_flow,
                    outcome=outcome,
                    relation_kind=relation.kind,
                    evidence=evidence,
                    provenance_refs=provenance_refs,
                    capability_requirement=capability_requirement,
                )
            )

        eligible = tuple(
            decision for decision in candidates
            if decision.status == "ELIGIBLE"
        )
        if len(eligible) == 1:
            return NextFlowResolution(
                origin_flow, outcome, tuple(candidates), eligible[0].cadence_next, "ELIGIBLE"
            )
        if len(eligible) > 1:
            return NextFlowResolution(
                origin_flow, outcome, tuple(candidates), None, "REVIEW_REQUIRED"
            )
        return NextFlowResolution(
            origin_flow, outcome, tuple(candidates), None, "WAITING"
        )

    def resolve(
        self,
        *,
        origin_flow: str,
        target_flow: str,
        outcome: CadenceOutcome,
        relation_kind,
        evidence: Mapping[str, object] | None = None,
        provenance_refs: tuple[str, ...] = (),
        capability_requirement: CapabilityRequirement | None = None,
    ) -> RoutingDecision:
        connection = self._complementarity.evaluate(
            origin_flow=origin_flow,
            target_flow=target_flow,
            relation_kind=relation_kind,
            outcome=outcome.value,
            available_evidence=evidence,
            provenance_refs=provenance_refs,
        )

        cadence_link = self._cadence.next(origin_flow, outcome)
        if connection.status is not ConnectionStatus.ELIGIBLE:
            return RoutingDecision(connection, cadence_link.next_flow if cadence_link else None, None, connection.status.value)

        if cadence_link is None or cadence_link.next_flow != target_flow:
            return RoutingDecision(
                connection,
                cadence_link.next_flow if cadence_link else None,
                None,
                "REVIEW_REQUIRED",
            )

        capability = None
        if capability_requirement is not None:
            if self._capability_selector is None:
                raise ValueError("capability selector is required for capability resolution")
            capability = self._capability_selector.select(capability_requirement)
            if capability.status != "SELECTED":
                return RoutingDecision(connection, target_flow, capability, capability.status)

        return RoutingDecision(connection, target_flow, capability, "ELIGIBLE")


__all__ = ["GovernedFlowRouter", "NextFlowResolution", "RoutingDecision"]
