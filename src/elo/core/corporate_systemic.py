"""Enterprise systemic projection over existing Core and cross-domain contracts.

The projection is immutable and derived. It is not a second knowledge store or
business-system source of truth.
"""

from dataclasses import dataclass
from typing import Mapping

from .cross_domain import CrossDomainGovernance, CrossDomainRelation, CorporateDomain
from .systemic_primitives import SystemicModel


@dataclass(frozen=True)
class CorporateSystemicView:
    base_model: SystemicModel
    cross_domain_relations: tuple[CrossDomainRelation, ...] = ()
    source_of_truth: str = "derived_projection"

    @classmethod
    def build(
        cls,
        base_model: SystemicModel,
        relations: tuple[CrossDomainRelation, ...],
        *,
        tenant_id: str,
    ) -> "CorporateSystemicView":
        governance = CrossDomainGovernance()
        validations = tuple(governance.validate(item, expected_tenant_id=tenant_id) for item in relations)
        invalid = tuple(item for item in validations if item.status != "VALID")
        if invalid:
            raise ValueError("invalid cross-domain relations: " + "; ".join(
                f"{item.relation_id}: {', '.join(item.gaps)}" for item in invalid
            ))
        return cls(base_model=base_model, cross_domain_relations=relations)

    def relations_from(self, domain: CorporateDomain) -> tuple[CrossDomainRelation, ...]:
        return tuple(item for item in self.cross_domain_relations if item.origin_domain == domain)

    def relations_to(self, domain: CorporateDomain) -> tuple[CrossDomainRelation, ...]:
        return tuple(item for item in self.cross_domain_relations if item.destination_domain == domain)

    def path_exists(self, origin: CorporateDomain, destination: CorporateDomain) -> bool:
        frontier = [origin]
        visited: set[CorporateDomain] = set()
        while frontier:
            current = frontier.pop()
            if current in visited:
                continue
            visited.add(current)
            if current == destination:
                return True
            frontier.extend(item.destination_domain for item in self.relations_from(current))
        return False

    def executive_summary(self) -> Mapping[str, object]:
        return {
            "source_of_truth": self.source_of_truth,
            "relation_count": len(self.cross_domain_relations),
            "domains": tuple(sorted({
                domain.value
                for relation in self.cross_domain_relations
                for domain in (relation.origin_domain, relation.destination_domain)
            })),
            "evidence_ids": tuple(dict.fromkeys(
                evidence_id
                for relation in self.cross_domain_relations
                for evidence_id in relation.evidence_ids
            )),
        }
