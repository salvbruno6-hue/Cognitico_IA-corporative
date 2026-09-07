"""Candidate-only harmonic association for the ELO Symbiont.

The association engine detects reusable relationships among laboratory
observations without creating canonical knowledge links or changing authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


LAB_ONLY = "LAB_ONLY"


@dataclass(frozen=True)
class HarmonicAssociationObservation:
    observation_id: str
    tenant_id: str
    context: str
    need: str
    capability: str
    skill: str
    tool: str
    result: str
    evidence_ids: tuple[str, ...]
    source_ref: str
    source_commit: str
    existing_owner: str | None = None


@dataclass(frozen=True)
class HarmonicAssociation:
    association_id: str
    tenant_id: str
    source_observation_ids: tuple[str, ...]
    relation_key: str
    similarity_score: float
    evidence_ids: tuple[str, ...]
    existing_owner: str | None
    disposition: str
    state: str = LAB_ONLY


class HarmonicAssociationEngine:
    """Relates experimental observations while preserving canonical boundaries."""

    @staticmethod
    def associate(
        observations: Iterable[HarmonicAssociationObservation],
        *,
        association_id: str,
    ) -> tuple[HarmonicAssociation, ...]:
        items = tuple(observations)
        if not items:
            return ()
        tenants = {item.tenant_id for item in items}
        if len(tenants) != 1:
            raise ValueError("harmonic association cannot cross tenant boundaries")
        for item in items:
            if not item.observation_id or not item.evidence_ids or not item.source_ref or not item.source_commit:
                raise ValueError("association requires observation identity, evidence and provenance")

        groups: dict[str, list[HarmonicAssociationObservation]] = {}
        for item in items:
            key = "|".join(
                value.strip().casefold()
                for value in (item.context, item.need, item.capability, item.skill, item.tool)
            )
            groups.setdefault(key, []).append(item)

        associations: list[HarmonicAssociation] = []
        for relation_key, group in groups.items():
            if len(group) < 2:
                continue
            evidence = tuple(dict.fromkeys(e for item in group for e in item.evidence_ids))
            owners = {item.existing_owner for item in group if item.existing_owner}
            owner = next(iter(owners), None) if len(owners) == 1 else None
            disposition = "REUSE" if owner else "CANDIDATE_FOR_GOVERNED_LEARNING"
            score = min(1.0, 0.5 + 0.1 * (len(group) - 2) + 0.1 * min(len(evidence), 5))
            associations.append(
                HarmonicAssociation(
                    association_id=association_id,
                    tenant_id=group[0].tenant_id,
                    source_observation_ids=tuple(item.observation_id for item in group),
                    relation_key=relation_key,
                    similarity_score=score,
                    evidence_ids=evidence,
                    existing_owner=owner,
                    disposition=disposition,
                )
            )
        return tuple(associations)
