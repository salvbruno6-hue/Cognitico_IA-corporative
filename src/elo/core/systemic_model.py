"""Systemic model primitives for ELO's enterprise-wide reasoning.

This module represents relationships between processes/entities/events without
owning operational data. It is deliberately provider-neutral and keeps the
Core focused on systemic understanding.
"""

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class SystemicNode:
    id: str
    kind: str
    name: str
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SystemicRelation:
    source_id: str
    relation: str
    target_id: str
    confidence: float = 1.0
    evidence_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class SystemicModel:
    nodes: tuple[SystemicNode, ...] = ()
    relations: tuple[SystemicRelation, ...] = ()

    def related_to(self, node_id: str) -> tuple[SystemicRelation, ...]:
        return tuple(
            relation
            for relation in self.relations
            if relation.source_id == node_id or relation.target_id == node_id
        )
