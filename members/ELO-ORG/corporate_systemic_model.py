"""Provider-neutral corporate systemic model primitives for ELO-ORG."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Tuple


class RelationKind(str, Enum):
    DEPENDS_ON = "DEPENDS_ON"
    SUPPLIES = "SUPPLIES"
    CONSUMES = "CONSUMES"
    IMPACTS = "IMPACTS"
    GOVERNED_BY = "GOVERNED_BY"


class AnalysisState(str, Enum):
    SUPPORTED = "SUPPORTED"
    INCONCLUSIVE = "INCONCLUSIVE"
    CONFLICTING = "CONFLICTING"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class DomainNode:
    domain_id: str
    name: str
    responsibilities: FrozenSet[str] = frozenset()


@dataclass(frozen=True)
class DomainRelation:
    source_domain: str
    target_domain: str
    kind: RelationKind
    evidence_ref: str
    valid_from: str
    valid_until: str | None = None


@dataclass(frozen=True)
class CorporateFlow:
    flow_id: str
    steps: Tuple[str, ...]
    source_ref: str
    tenant_id: str
    principal_id: str


@dataclass(frozen=True)
class CrossDomainAnalysis:
    state: AnalysisState
    involved_domains: FrozenSet[str]
    matched_relations: Tuple[DomainRelation, ...] = ()
    conflicts: Tuple[str, ...] = ()
    evidence_refs: Tuple[str, ...] = ()


@dataclass
class CorporateSystemicModel:
    domains: dict[str, DomainNode] = field(default_factory=dict)
    relations: list[DomainRelation] = field(default_factory=list)

    def add_domain(self, domain: DomainNode) -> None:
        self.domains[domain.domain_id] = domain

    def add_relation(self, relation: DomainRelation) -> None:
        if relation.source_domain not in self.domains:
            raise ValueError(f"unknown source domain: {relation.source_domain}")
        if relation.target_domain not in self.domains:
            raise ValueError(f"unknown target domain: {relation.target_domain}")
        if not relation.evidence_ref:
            raise ValueError("cross-domain relations require provenance/evidence")
        self.relations.append(relation)

    def analyze_flow(self, flow: CorporateFlow) -> CrossDomainAnalysis:
        if not flow.steps or not flow.tenant_id or not flow.principal_id:
            return CrossDomainAnalysis(
                state=AnalysisState.BLOCKED,
                involved_domains=frozenset(flow.steps),
            )

        involved = frozenset(flow.steps)
        matched = tuple(
            relation
            for relation in self.relations
            if relation.source_domain in involved and relation.target_domain in involved
        )
        evidence = tuple(sorted({relation.evidence_ref for relation in matched}))
        missing_pairs = []
        for left, right in zip(flow.steps, flow.steps[1:]):
            if not any(
                relation.source_domain == left and relation.target_domain == right
                for relation in matched
            ):
                missing_pairs.append(f"missing relation: {left}->{right}")

        if missing_pairs:
            return CrossDomainAnalysis(
                state=AnalysisState.INCONCLUSIVE,
                involved_domains=involved,
                matched_relations=matched,
                conflicts=tuple(missing_pairs),
                evidence_refs=evidence,
            )

        return CrossDomainAnalysis(
            state=AnalysisState.SUPPORTED,
            involved_domains=involved,
            matched_relations=matched,
            evidence_refs=evidence,
        )
