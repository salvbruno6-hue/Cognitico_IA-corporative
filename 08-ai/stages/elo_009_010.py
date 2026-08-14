"""Governed, deterministic reference primitives for ELO stages 9 and 10."""
from __future__ import annotations
from dataclasses import dataclass, replace
from enum import Enum
from typing import Iterable

class PlanState(str, Enum):
    VALID = "VALID"
    INCONSISTENT = "PLAN WITH INCONSISTENCIES"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"

@dataclass(frozen=True)
class Node:
    id: str
    tenant_id: str
    domain: str
    kind: str
    value: float = 0.0

@dataclass(frozen=True)
class Dependency:
    source: str
    target: str
    weight: float = 1.0

@dataclass(frozen=True)
class Constraint:
    id: str
    node_id: str
    maximum: float | None = None
    minimum: float | None = None

@dataclass(frozen=True)
class Scenario:
    id: str
    tenant_id: str
    domain: str
    principal_id: str
    assumptions: tuple[str, ...]
    changed_nodes: tuple[str, ...]
    evidence_refs: tuple[str, ...] = ()

@dataclass(frozen=True)
class Impact:
    node_id: str
    depth: int
    score: float
    reason: str

@dataclass(frozen=True)
class Alternative:
    id: str
    scenario_id: str
    tenant_id: str
    impacts: tuple[Impact, ...]
    risk: float
    strategic_effect: float
    feasibility: float
    evidence_refs: tuple[str, ...] = ()

    @property
    def score(self) -> float:
        impact = sum(i.score for i in self.impacts)
        return round((self.feasibility * 0.45) + (self.strategic_effect * 0.35) - (self.risk * 0.20) - (impact * 0.10), 6)

@dataclass(frozen=True)
class PlanVersion:
    plan_id: str
    version: int
    tenant_id: str
    domain: str
    state: PlanState
    supersedes: int | None = None
    decision_id: str | None = None
    approval_principal_id: str | None = None

def _tenant_nodes(nodes: Iterable[Node], tenant_id: str, domain: str) -> dict[str, Node]:
    return {n.id: n for n in nodes if n.tenant_id == tenant_id and n.domain == domain}

def propagate_impact(nodes: Iterable[Node], dependencies: Iterable[Dependency], scenario: Scenario) -> tuple[Impact, ...]:
    """Traverse only the scenario tenant/domain graph; never cross the boundary."""
    graph: dict[str, list[Dependency]] = {}
    for edge in dependencies:
        graph.setdefault(edge.source, []).append(edge)
    allowed = _tenant_nodes(nodes, scenario.tenant_id, scenario.domain)
    if any(node_id not in allowed for node_id in scenario.changed_nodes):
        raise ValueError("changed node is outside tenant/domain boundary")
    found: dict[str, Impact] = {}
    frontier = [(node_id, 0, 1.0) for node_id in scenario.changed_nodes]
    while frontier:
        current, depth, score = frontier.pop(0)
        if current in found and found[current].score >= score:
            continue
        found[current] = Impact(current, depth, round(score, 6), f"dependency depth {depth}")
        for edge in sorted(graph.get(current, []), key=lambda e: e.target):
            if edge.target in allowed:
                frontier.append((edge.target, depth + 1, score * edge.weight))
    return tuple(sorted(found.values(), key=lambda i: (i.depth, i.node_id)))

def validate_constraints(nodes: Iterable[Node], constraints: Iterable[Constraint], tenant_id: str, domain: str) -> tuple[str, ...]:
    selected = _tenant_nodes(nodes, tenant_id, domain)
    conflicts: list[str] = []
    for c in constraints:
        node = selected.get(c.node_id)
        if node is None:
            continue
        if c.maximum is not None and node.value > c.maximum:
            conflicts.append(f"{c.id}:maximum")
        if c.minimum is not None and node.value < c.minimum:
            conflicts.append(f"{c.id}:minimum")
    return tuple(sorted(conflicts))

def rank_alternatives(alternatives: Iterable[Alternative], tenant_id: str, scenario_id: str) -> tuple[Alternative, ...]:
    selected = [a for a in alternatives if a.tenant_id == tenant_id and a.scenario_id == scenario_id]
    return tuple(sorted(selected, key=lambda a: (-a.score, a.id)))

def recommend(alternatives: Iterable[Alternative], conflicts: Iterable[str], tenant_id: str, scenario_id: str) -> dict:
    ranked = rank_alternatives(alternatives, tenant_id, scenario_id)
    conflicts = tuple(sorted(conflicts))
    if conflicts:
        return {"status": PlanState.INCONSISTENT.value, "recommended": None, "alternatives": [a.id for a in ranked], "conflicts": conflicts}
    if not ranked:
        return {"status": "NO_FEASIBLE_ALTERNATIVE", "recommended": None, "alternatives": [], "conflicts": ()}
    winner = ranked[0]
    return {"status": PlanState.VALID.value, "recommended": winner.id, "score": winner.score, "alternatives": [a.id for a in ranked], "evidence_refs": winner.evidence_refs}

def propose_replan(plan: PlanVersion, decision_id: str, conflicts: Iterable[str]) -> PlanVersion:
    if tuple(conflicts):
        return replace(plan, state=PlanState.INCONSISTENT, decision_id=decision_id)
    return replace(plan, version=plan.version + 1, state=PlanState.PENDING_APPROVAL, supersedes=plan.version, decision_id=decision_id)

def approve_replan(plan: PlanVersion, principal_id: str) -> PlanVersion:
    if plan.state is not PlanState.PENDING_APPROVAL:
        raise ValueError("only pending plans can be approved")
    return replace(plan, state=PlanState.APPROVED, approval_principal_id=principal_id)

def reject_replan(plan: PlanVersion, principal_id: str) -> PlanVersion:
    if plan.state is not PlanState.PENDING_APPROVAL:
        raise ValueError("only pending plans can be rejected")
    return replace(plan, state=PlanState.REJECTED, approval_principal_id=principal_id)

def supersede(previous: PlanVersion, replacement: PlanVersion) -> tuple[PlanVersion, PlanVersion]:
    if replacement.supersedes != previous.version:
        raise ValueError("replacement must explicitly supersede previous version")
    return replace(previous, state=PlanState.SUPERSEDED), replacement
