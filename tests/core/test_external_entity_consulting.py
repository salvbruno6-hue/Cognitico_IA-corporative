from dataclasses import dataclass

import pytest

from elo.core.consulting import ConsultingResponse
from elo.core.entity_consultant import EntityConsultant
from elo.core.evolution_memory import EvolutionMemory
from elo.core.external_entity import EntityKnowledgeResult, EntityResolution, ExternalEntityRequest
from elo.core.knowledge_admission import KnowledgeAdmission
from elo.core.provider_gateway import ProviderGateway, ProviderRequest, ProviderUnavailable


@dataclass
class FakeInternal:
    facts: tuple[str, ...] = ()

    def resolve(self, request: ExternalEntityRequest) -> EntityResolution:
        return EntityResolution(
            canonical_name=request.entity_name,
            entity_kind=request.entity_kind,
            identifiers={"name": request.entity_name},
            confidence=0.99,
            internal_match=bool(self.facts),
            internal_evidence_count=len(self.facts),
        )

    def consult(self, entity: EntityResolution, query: str) -> EntityKnowledgeResult:
        return EntityKnowledgeResult(
            entity=entity,
            facts=self.facts,
            provenance={"source": "elo:test"},
            external=False,
        )


class FakeProvider:
    name = "GPT:test"

    def consult(self, request: ProviderRequest) -> EntityKnowledgeResult:
        return EntityKnowledgeResult(
            entity=request.entity,
            facts=("External company fact.",),
            evidence=("https://example.test/source",),
            provider=self.name,
            provider_request_id="provider-request-1",
            provenance={"provider": self.name, "source": "https://example.test/source"},
        )


def request(authorized: bool = True) -> ExternalEntityRequest:
    return ExternalEntityRequest(
        query="What do we know?",
        entity_name="Multiteiner",
        entity_kind="COMPANY",
        tenant_id="tenant-1",
        domain="commercial",
        principal="analyst-1",
        session_id="session-1",
        request_id="request-1",
        correlation_id="corr-1",
        external_consultation_authorized=authorized,
    )


def test_internal_knowledge_is_preferred_without_provider() -> None:
    consultant = EntityConsultant(
        FakeInternal(("Internal fact.",)),
        ProviderGateway(()),
        KnowledgeAdmission(),
        EvolutionMemory(),
    )

    result = consultant.consult(request())

    assert result.consulted_externally is False
    assert result.knowledge is not None
    assert result.knowledge.facts == ("Internal fact.",)


def test_external_provider_is_used_when_internal_knowledge_is_insufficient() -> None:
    memory = EvolutionMemory()
    consultant = EntityConsultant(
        FakeInternal(),
        ProviderGateway((FakeProvider(),)),
        KnowledgeAdmission(),
        memory,
    )

    result = consultant.consult(request())

    assert result.consulted_externally is True
    assert result.retained_evolution_id == "entity:Multiteiner:consult:request-1"
    assert memory.get(result.retained_evolution_id) is not None


def test_provider_is_not_called_without_authorization() -> None:
    consultant = EntityConsultant(
        FakeInternal(),
        ProviderGateway((FakeProvider(),)),
        KnowledgeAdmission(),
        EvolutionMemory(),
    )

    result = consultant.consult(request(authorized=False))

    assert result.consulted_externally is False
    assert result.response.status == "INSUFFICIENT_EVIDENCE"


def test_no_provider_returns_insufficient_evidence() -> None:
    consultant = EntityConsultant(
        FakeInternal(),
        ProviderGateway(()),
        KnowledgeAdmission(),
        EvolutionMemory(),
    )

    result = consultant.consult(request())

    assert result.response.status == "INSUFFICIENT_EVIDENCE"
    assert result.knowledge is None
