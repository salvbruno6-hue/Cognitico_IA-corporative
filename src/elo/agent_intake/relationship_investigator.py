"""Bounded relationship/cascade investigator for ELO scan missions.

Provider-neutral and deterministic. It consumes already-resolved relationship
edges and records; it does not query the database, infer causality, or promote
learning. Structural edges are evidence of association only.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

@dataclass(frozen=True, slots=True)
class RelationshipEdge:
    source: str
    target: str
    relation_type: str
    provenance: str
    tenant_scope: str = ""

@dataclass(frozen=True, slots=True)
class CascadePath:
    nodes: tuple[str, ...]
    edges: tuple[RelationshipEdge, ...]
    structural_only: bool
    evidence_required: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class RelationshipInvestigation:
    paths: tuple[CascadePath, ...]
    evidence_gaps: tuple[str, ...]
    causality_established: bool
    learning_eligible: bool

def _edge(item: Mapping[str, Any]) -> RelationshipEdge | None:
    source = str(item.get("source", "")).strip()
    target = str(item.get("target", "")).strip()
    relation_type = str(item.get("relation_type", "structural")).strip() or "structural"
    provenance = str(item.get("provenance", "")).strip()
    tenant = str(item.get("tenant_scope", "")).strip()
    if not source or not target or not provenance:
        return None
    return RelationshipEdge(source, target, relation_type, provenance, tenant)

def investigate_relationships(
    records: Sequence[Mapping[str, Any]],
    edges: Sequence[Mapping[str, Any]],
    *,
    tenant_scope: str,
    max_depth: int = 4,
) -> RelationshipInvestigation:
    """Build bounded paths from records and resolved edges.

    A path is retained only when every node belongs to the supplied records
    and every edge has provenance and the same tenant scope (or no tenant).
    """
    if max_depth < 1:
        return RelationshipInvestigation((), ("max_depth must be >= 1",), False, False)

    nodes = {
        str(r.get("id", "")).strip()
        for r in records
        if str(r.get("id", "")).strip()
    }
    usable: list[RelationshipEdge] = []
    for raw in edges:
        e = _edge(raw)
        if e and e.source in nodes and e.target in nodes and (
            not e.tenant_scope or e.tenant_scope == tenant_scope
        ):
            usable.append(e)

    adjacency: dict[str, list[RelationshipEdge]] = {}
    for e in sorted(usable, key=lambda x: (x.source, x.target, x.relation_type, x.provenance)):
        adjacency.setdefault(e.source, []).append(e)

    paths: list[CascadePath] = []
    seen: set[tuple[str, ...]] = set()

    def walk(start: str, current: str, path_edges: tuple[RelationshipEdge, ...], visited: frozenset[str]) -> None:
        if path_edges:
            signature = (start,) + tuple(e.target for e in path_edges)
            if signature not in seen:
                seen.add(signature)
                paths.append(CascadePath(
                    signature,
                    path_edges,
                    True,
                    ("observed result or outcome", "coherence check", "cause/effect evidence"),
                ))
        if len(path_edges) >= max_depth:
            return
        for e in adjacency.get(current, ()):
            if e.target not in visited:
                walk(start, e.target, path_edges + (e,), visited | {e.target})

    for start in sorted(nodes):
        walk(start, start, (), frozenset({start}))

    gaps: list[str] = []
    if not nodes:
        gaps.append("no scoped records available")
    if not usable:
        gaps.append("no provenance-backed relationship edge connects scoped records")
    if paths:
        gaps.append("structural relationships do not establish causality")
    return RelationshipInvestigation(
        tuple(paths),
        tuple(dict.fromkeys(gaps)),
        False,
        False,
    )

__all__ = ["RelationshipEdge", "CascadePath", "RelationshipInvestigation", "investigate_relationships"]
