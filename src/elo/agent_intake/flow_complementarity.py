"""Evidence-aware composition of existing ELO flows.

This module adapts the Hermes relationship/learning pattern to ELO without
creating a second registry, scheduler, approval authority, or orchestrator.

Hermes contributes observed mechanisms and candidate evidence. ELO remains
responsible for identity, contracts, provenance, authorization and routing.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


class RelationKind(StrEnum):
    FEEDS = "FEEDS"
    REQUIRES = "REQUIRES"
    VALIDATES = "VALIDATES"
    CORRECTS = "CORRECTS"
    ENRICHES = "ENRICHES"
    HANDOFF = "HANDOFF"
    RETURNS_TO = "RETURNS_TO"
    BLOCKS = "BLOCKS"


class ConnectionStatus(StrEnum):
    UNRESOLVED = "UNRESOLVED"
    CONFLICT = "CONFLICT"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    WAITING = "WAITING"
    ELIGIBLE = "ELIGIBLE"


@dataclass(frozen=True, slots=True)
class FlowProfile:
    flow_id: str
    owner: str
    accepts: tuple[str, ...]
    produces: tuple[str, ...]
    prerequisites: tuple[str, ...] = ()
    success_outcomes: tuple[str, ...] = ()
    failure_outcomes: tuple[str, ...] = ()
    evidence_required: tuple[str, ...] = ()
    provenance_required: tuple[str, ...] = ()
    authority: str = ""
    side_effect_class: str = "none"
    allowed_next_relations: tuple[RelationKind, ...] = ()


@dataclass(frozen=True, slots=True)
class FlowRelation:
    relation_id: str
    origin_flow: str
    target_flow: str
    kind: RelationKind
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    source: str
    confidence: float = 0.0
    canonical: bool = False


@dataclass(frozen=True, slots=True)
class FlowConnectionDecision:
    origin_flow: str
    target_flow: str
    relation: RelationKind | None
    status: ConnectionStatus
    reasons: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]


class ComplementarityEngine:
    """Evaluate whether one existing flow can hand off to another.

    It reasons over registered profiles and explicit/evidenced relations.
    It never creates a new authority and never executes the selected flow.
    """

    def __init__(
        self,
        profiles: tuple[FlowProfile, ...],
        relations: tuple[FlowRelation, ...] = (),
    ) -> None:
        self._profiles = {profile.flow_id: profile for profile in profiles}
        self._relations = {
            (item.origin_flow, item.target_flow, item.kind): item
            for item in relations
        }

    def evaluate(
        self,
        *,
        origin_flow: str,
        target_flow: str,
        relation_kind: RelationKind,
        outcome: str,
        available_evidence: Mapping[str, object] | None = None,
        provenance_refs: tuple[str, ...] = (),
        required_authority: str | None = None,
    ) -> FlowConnectionDecision:
        evidence = available_evidence or {}
        reasons: list[str] = []

        origin = self._profiles.get(origin_flow)
        target = self._profiles.get(target_flow)
        if origin is None or target is None:
            return FlowConnectionDecision(
                origin_flow, target_flow, None, ConnectionStatus.UNRESOLVED,
                ("flow identity is not registered",), (), provenance_refs,
            )

        relation = self._relations.get((origin_flow, target_flow, relation_kind))
        if relation is None:
            return FlowConnectionDecision(
                origin_flow, target_flow, relation_kind,
                ConnectionStatus.REVIEW_REQUIRED,
                ("relationship is not explicitly registered",), (), provenance_refs,
            )

        if relation.canonical:
            reasons.append("canonical relation may not be introduced through the learning surface")

        if not relation.evidence_refs:
            reasons.append("relation has no evidence")
        if not provenance_refs or not relation.provenance_refs:
            reasons.append("provenance is incomplete")

        if relation.confidence < 0.6:
            reasons.append("relationship confidence is below the minimum")
        if relation.source not in {"ELO", "HERMES", "OBSERVED"}:
            reasons.append("relationship source is not recognized")

        if outcome not in origin.success_outcomes and outcome not in origin.failure_outcomes:
            reasons.append("origin outcome is not declared by its profile")

        if relation_kind not in origin.allowed_next_relations:
            reasons.append("origin flow does not permit this relation kind")

        if not set(origin.produces).intersection(target.accepts):
            reasons.append("output contract is incompatible with target input contract")

        missing = [
            key for key in target.prerequisites
            if not bool(evidence.get(key))
        ]
        if missing:
            reasons.append(
                "target prerequisites are missing: " + ", ".join(missing)
            )

        if required_authority and target.authority != required_authority:
            reasons.append("target authority does not match required authority")

        if target.evidence_required:
            missing_evidence = [
                item for item in target.evidence_required
                if not bool(evidence.get(item))
            ]
            if missing_evidence:
                reasons.append(
                    "required target evidence is missing: "
                    + ", ".join(missing_evidence)
                )

        if target.provenance_required and not provenance_refs:
            reasons.append("target requires provenance")

        if target.side_effect_class == "consequential" and not evidence.get("authorized"):
            reasons.append("consequential target lacks explicit authorization")

        if reasons:
            blocking = any(
                phrase in " ".join(reasons).lower()
                for phrase in (
                    "identity",
                    "no evidence",
                    "provenance",
                    "confidence",
                    "incompatible",
                    "missing",
                    "requires",
                    "authority",
                    "not permitted",
                )
            )
            return FlowConnectionDecision(
                origin_flow,
                target_flow,
                relation_kind,
                ConnectionStatus.WAITING if blocking else ConnectionStatus.REVIEW_REQUIRED,
                tuple(dict.fromkeys(reasons)),
                relation.evidence_refs,
                tuple(dict.fromkeys(relation.provenance_refs + provenance_refs)),
            )

        return FlowConnectionDecision(
            origin_flow,
            target_flow,
            relation_kind,
            ConnectionStatus.ELIGIBLE,
            (),
            relation.evidence_refs,
            tuple(dict.fromkeys(relation.provenance_refs + provenance_refs)),
        )


def hermes_relation(
    *,
    relation_id: str,
    origin_flow: str,
    target_flow: str,
    kind: RelationKind,
    evidence_refs: tuple[str, ...],
    provenance_refs: tuple[str, ...],
    confidence: float,
) -> FlowRelation:
    """Create an ELO candidate relation backed by Hermes-origin evidence.

    The resulting relation is never canonical.
    """
    if not evidence_refs:
        raise ValueError("Hermes-derived relation requires evidence")
    if not provenance_refs:
        raise ValueError("Hermes-derived relation requires provenance")
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be between 0 and 1")
    if origin_flow == target_flow:
        raise ValueError("self-relations are not admitted")

    return FlowRelation(
        relation_id=relation_id,
        origin_flow=origin_flow,
        target_flow=target_flow,
        kind=kind,
        evidence_refs=evidence_refs,
        provenance_refs=provenance_refs,
        source="HERMES",
        confidence=confidence,
        canonical=False,
    )


__all__ = [
    "ComplementarityEngine",
    "ConnectionStatus",
    "FlowConnectionDecision",
    "FlowProfile",
    "FlowRelation",
    "RelationKind",
    "hermes_relation",
]
