"""Consultant orchestration for internal-first external entity knowledge.

The consultant searches internal knowledge first. Only when evidence is
insufficient and external consultation is authorized does it call a provider.
Any retained external result passes through KnowledgeAdmission and, when
admitted, EvolutionMemory. External output never changes ELO Soul directly.
"""

from dataclasses import dataclass
from typing import Protocol

from .consulting import ConsultingResponse
from .evolution_memory import EvolutionMemory, EvolutionRecord
from .external_entity import EntityKnowledgeResult, EntityResolution, ExternalEntityRequest
from .knowledge_admission import AdmissionRequest, KnowledgeAdmission
from .provider_gateway import ProviderGateway, ProviderRequest, ProviderUnavailable


class InternalEntityKnowledge(Protocol):
    """Repository/knowledge adapter used before any external consultation."""

    def resolve(self, request: ExternalEntityRequest) -> EntityResolution:
        ...

    def consult(self, entity: EntityResolution, query: str) -> EntityKnowledgeResult:
        ...


@dataclass(frozen=True)
class EntityConsultationResult:
    response: ConsultingResponse
    knowledge: EntityKnowledgeResult | None
    consulted_externally: bool
    retained_evolution_id: str | None


class EntityConsultant:
    """Governed consultant for external companies and other entities."""

    def __init__(
        self,
        internal: InternalEntityKnowledge,
        providers: ProviderGateway,
        admission: KnowledgeAdmission,
        evolution_memory: EvolutionMemory,
    ) -> None:
        self._internal = internal
        self._providers = providers
        self._admission = admission
        self._evolution_memory = evolution_memory

    def consult(self, request: ExternalEntityRequest) -> EntityConsultationResult:
        entity = self._internal.resolve(request)
        internal = self._internal.consult(entity, request.query)

        if internal.facts or internal.evidence:
            knowledge = internal
            external = False
        else:
            try:
                knowledge = self._providers.consult(
                    ProviderRequest(
                        request=request,
                        entity=entity,
                        instruction=(
                            "Identify the external entity, distinguish verified facts "
                            "from inference, provide source references where available, "
                            "and do not claim certainty without evidence."
                        ),
                    )
                )
                external = True
            except ProviderUnavailable as exc:
                response = ConsultingResponse(
                    objective=request.query,
                    context=(f"entity:{entity.canonical_name}",),
                    analysis=("Internal ELO knowledge was insufficient.",),
                    decision_required="No external provider is currently available; supply an authorized provider or source.",
                    provenance=("ELO:internal-search",),
                    status="INSUFFICIENT_EVIDENCE",
                    uncertainty=(str(exc),),
                )
                return EntityConsultationResult(response, None, False, None)

        retained_id = None
        if external:
            admission = self._admission.evaluate(
                AdmissionRequest(
                    tenant_id=request.tenant_id,
                    domain=request.domain,
                    source_type=knowledge.provider or "EXTERNAL_PROVIDER",
                    source_id=knowledge.provider_request_id or request.entity_name,
                    content="\n".join(knowledge.facts),
                    provenance=knowledge.provenance,
                    authorized=request.external_consultation_authorized,
                    relevant=True,
                    evidence_available=bool(knowledge.evidence),
                )
            )
            if admission.outcome not in {"REJECT", "ARCHIVE"}:
                retained_id = f"entity:{entity.canonical_name}:consult:{request.request_id}"
                self._evolution_memory.store(
                    EvolutionRecord(
                        evolution_id=retained_id,
                        tenant_id=request.tenant_id,
                        domain=request.domain,
                        source_type=knowledge.provider or "EXTERNAL_PROVIDER",
                        source_id=knowledge.provider_request_id or request.entity_name,
                        content="\n".join(knowledge.facts),
                        status="EVIDENCE" if knowledge.evidence else "OBSERVATION",
                        provenance=knowledge.provenance,
                    )
                )

        response = ConsultingResponse(
            objective=request.query,
            context=(f"entity:{entity.canonical_name}", f"kind:{entity.entity_kind}"),
            facts=knowledge.facts,
            evidence=knowledge.evidence,
            assumptions=knowledge.assumptions,
            analysis=("Internal evidence was preferred before external consultation.",),
            alternatives=(),
            risks=knowledge.contradictions,
            provenance=tuple(f"{k}:{v}" for k, v in knowledge.provenance.items()),
            status="ANALYSIS" if not knowledge.facts else "RECOMMENDATION",
            uncertainty=knowledge.contradictions,
        )
        return EntityConsultationResult(response, knowledge, external, retained_id)
