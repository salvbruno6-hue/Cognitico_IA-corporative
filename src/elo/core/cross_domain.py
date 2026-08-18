"""Provider-neutral cross-domain relationship contracts for ELO.

This module models relationships; it does not persist domain data or merge
business authorities. Each relation retains origin/destination ownership,
provenance, evidence and temporal validity.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


class CorporateDomain(StrEnum):
    COMMERCIAL = "COMERCIAL"
    TENDERS = "LICITACOES"
    BUDGET = "ORCAMENTO"
    PROJECTS = "PROJETOS_ENGENHARIA"
    PROCUREMENT = "COMPRAS_SUPRIMENTOS"
    PRODUCTION = "PRODUCAO"
    PCP = "PCP"
    LOGISTICS = "LOGISTICA_EXPEDICAO"
    OUTCOME = "RESULTADO_POS_EXECUCAO"


@dataclass(frozen=True)
class CrossDomainRelation:
    relation_id: str
    origin_domain: CorporateDomain
    destination_domain: CorporateDomain
    relation_type: str
    statement: str
    tenant_id: str
    principal_id: str
    source_id: str
    evidence_ids: tuple[str, ...]
    valid_from: str
    valid_until: str | None = None
    confidence: float = 0.0
    responsibility: str | None = None
    provenance: Mapping[str, str] = ()

    def __post_init__(self) -> None:
        if not self.relation_id or not self.statement or not self.tenant_id or not self.principal_id:
            raise ValueError("relation identity, statement, tenant and principal are required")
        if self.origin_domain == self.destination_domain:
            raise ValueError("cross-domain relation requires distinct origin and destination domains")
        if not self.source_id or not self.evidence_ids:
            raise ValueError("cross-domain relation requires source and evidence")
        if not self.valid_from:
            raise ValueError("valid_from is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class CrossDomainValidation:
    status: str
    relation_id: str
    gaps: tuple[str, ...] = ()


class CrossDomainGovernance:
    """Validate cross-domain relations without becoming a business-rule authority."""

    def validate(
        self,
        relation: CrossDomainRelation,
        *,
        expected_tenant_id: str | None = None,
        minimum_confidence: float = 0.6,
    ) -> CrossDomainValidation:
        gaps: list[str] = []
        if expected_tenant_id and relation.tenant_id != expected_tenant_id:
            gaps.append("tenant mismatch")
        if relation.confidence < minimum_confidence:
            gaps.append("confidence below cross-domain threshold")
        provenance = dict(relation.provenance)
        if provenance.get("origin_domain") not in (None, relation.origin_domain.value):
            gaps.append("provenance origin domain mismatch")
        if provenance.get("destination_domain") not in (None, relation.destination_domain.value):
            gaps.append("provenance destination domain mismatch")
        return CrossDomainValidation(
            status="VALID" if not gaps else "BLOCKED",
            relation_id=relation.relation_id,
            gaps=tuple(gaps),
        )

    @staticmethod
    def canonical_chain() -> tuple[tuple[CorporateDomain, CorporateDomain], ...]:
        return (
            (CorporateDomain.COMMERCIAL, CorporateDomain.BUDGET),
            (CorporateDomain.COMMERCIAL, CorporateDomain.TENDERS),
            (CorporateDomain.TENDERS, CorporateDomain.BUDGET),
            (CorporateDomain.BUDGET, CorporateDomain.PROJECTS),
            (CorporateDomain.PROJECTS, CorporateDomain.PROCUREMENT),
            (CorporateDomain.PROCUREMENT, CorporateDomain.PRODUCTION),
            (CorporateDomain.PCP, CorporateDomain.PRODUCTION),
            (CorporateDomain.PRODUCTION, CorporateDomain.LOGISTICS),
            (CorporateDomain.LOGISTICS, CorporateDomain.OUTCOME),
        )
