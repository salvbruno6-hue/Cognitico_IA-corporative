from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KnowledgeNode:
    id: str
    label: str
    source: str


@dataclass(frozen=True, slots=True)
class KnowledgeEdge:
    source: str
    target: str
    relation: str


class CognitiveKnowledgeGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, KnowledgeNode] = {}
        self.edges: list[KnowledgeEdge] = []

    def add_node(self, node: KnowledgeNode) -> None:
        self.nodes[node.id] = node

    def add_edge(self, edge: KnowledgeEdge) -> None:
        if edge.source not in self.nodes or edge.target not in self.nodes:
            raise ValueError("edges require existing nodes")
        self.edges.append(edge)

    def neighbors(self, node_id: str) -> tuple[KnowledgeNode, ...]:
        ids = {e.target for e in self.edges if e.source == node_id}
        return tuple(self.nodes[i] for i in ids)
