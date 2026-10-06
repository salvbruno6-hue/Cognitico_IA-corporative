from dataclasses import dataclass
from datetime import datetime, timezone

from elo.application.use_cases.orchestrator import GovernedOrchestrator, OrchestrationRequest
from elo.cognitive.runtime.humanization.humanizer import Humanizer
from elo.evidence import Evidence, EvidenceRepository


@dataclass
class FakeForge:
    evidence: Evidence
    absence: Evidence

    def gather_evidence(self, *, question, tenant_id, repository, entity_code):
        repository.save(self.evidence)
        repository.save(self.absence)
        return {
            "entity_code": entity_code,
            "selected_sources": [
                {"schema_name": "public", "table_name": "modelos", "dominio_codigo": "produtos", "prioridade": 54},
                {"schema_name": "public", "table_name": "fluxo_produtivo_modular", "dominio_codigo": "producao_fluxo_modular", "prioridade": 60},
            ],
            "source_results": [
                {"table": "modelos", "mode": "relational_context", "records": 1},
                {"table": "fluxo_produtivo_modular", "mode": "entity_scan", "records_scanned": 1, "matches": 0},
            ],
            "evidence": [self.evidence],
            "absences": [self.absence],
            "conflicts": [],
            "evidence_ids": (self.evidence.evidence_id, self.absence.evidence_id),
        }


def _evidence():
    now = datetime.now(timezone.utc)
    observed = Evidence.from_forge(
        tenant_id="tenant-a",
        source_table="modelos",
        source_record_id="model-1",
        source_domain="produtos",
        source_fields=("codigo", "nome", "ativo"),
        claim="O modelo M01 é Habitacional Amplo 20 pés e está ativo=True.",
        value={"codigo": "M01", "nome": "Habitacional Amplo 20 pés", "ativo": True},
        observed_at=now,
    )
    absence = Evidence.from_forge(
        tenant_id="tenant-a",
        source_table="fluxo_produtivo_modular",
        source_domain="producao_fluxo_modular",
        source_fields=(),
        claim="Nenhum registro correspondente a M01 foi encontrado em fluxo_produtivo_modular dentro do escopo consultado.",
        absence_type="no_matching_record_found",
        query_scope={"entity_code": "M01", "records_scanned": 1},
        observed_at=now,
    )
    return observed, absence


def test_governed_orchestrator_conversation_preserves_evidence_and_absence():
    observed, absence = _evidence()
    repository = EvidenceRepository()
    orchestrator = GovernedOrchestrator(evidence_repository=repository)
    result = orchestrator.converse(
        OrchestrationRequest(
            tenant_id="tenant-a",
            principal_id="principal-a",
            domain="produtos",
            objective="Me explique o M01 e como ele entra na produção.",
            request_id="req-1",
            correlation_id="corr-1",
        ),
        forge_adapter=FakeForge(observed, absence),
    )

    assert result["forge"]["entity_code"] == "M01"
    assert result["provenance"]["evidence_refs"] == [observed.evidence_id, absence.evidence_id]
    stored = repository.list_for_refs(result["provenance"]["evidence_refs"], tenant_id="tenant-a")
    assert len(stored) == 2
    assert stored[0].source_fields == ("codigo", "nome", "ativo")
    assert stored[1].absence_type == "no_matching_record_found"
    assert "inexistência absoluta" in result["response"]["content"]


def test_humanizer_does_not_turn_absence_into_nonexistence():
    observed, absence = _evidence()
    text = Humanizer().humanize(
        {
            "intent": "forge_consulta",
            "entity_code": "M01",
            "evidence": [observed],
            "absences": [absence],
            "selected_sources": [
                {"table_name": "fluxo_produtivo_modular", "dominio_codigo": "producao_fluxo_modular"}
            ],
        }
    )

    assert "Nenhum registro correspondente" in text
    assert "não foi encontrado" in text
    assert "inexistência absoluta" in text
