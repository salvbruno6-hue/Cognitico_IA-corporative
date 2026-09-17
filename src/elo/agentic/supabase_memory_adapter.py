from dataclasses import dataclass
from typing import Any, Mapping

from elo.agentic.contracts import IntentSpec, KnowledgeCandidate, KnowledgeRequirement


@dataclass(frozen=True)
class MemoryTableSpec:
    table: str
    role: str
    domain: str
    requirement: str


MEMORY_TABLES = (
    MemoryTableSpec("elo_experience_records", "experience", "corporativo", "experience"),
    MemoryTableSpec("elo_orcamento_memoria", "calculation", "orçamento", "calculation_memory"),
    MemoryTableSpec("elo_reasoning_patterns", "reasoning", "corporativo", "reasoning_patterns"),
    MemoryTableSpec("elo_aprendizado_padroes_raciocinio", "reasoning_learning", "corporativo", "reasoning_patterns"),
    MemoryTableSpec("excedentes", "excedentes", "orçamento", "excedentes"),
    MemoryTableSpec("excedente_itens", "excedentes", "orçamento", "excedentes"),
    MemoryTableSpec("excedente_mao_obra", "excedentes", "orçamento", "excedentes"),
    MemoryTableSpec("elo_aprendizado_conceitos", "standards", "corporativo", "standards"),
)

_TABLE_BY_NAME = {item.table: item for item in MEMORY_TABLES}


class SupabaseLearningMemoryAdapter:
    def __init__(self, rows: Mapping[str, list[Mapping[str, Any]]]):
        self._rows = rows

    def retrieve(self, intent: IntentSpec, requirement: KnowledgeRequirement) -> tuple[KnowledgeCandidate, ...]:
        tables = [item for item in MEMORY_TABLES if item.requirement == requirement.name]
        if not tables:
            return ()
        requested_domain = intent.domain.lower()
        candidates: list[KnowledgeCandidate] = []
        for spec in tables:
            table = spec.table
            for row in self._rows.get(table, ()):
                if not self._scope_matches(row, intent):
                    continue
                candidates.append(
                    KnowledgeCandidate(
                        source_id=f"supabase:{table}:{self._row_id(row)}",
                        content=self._content(row, spec),
                        source_type=f"supabase:{spec.role}",
                        status=self._status(row),
                        relevance=self._relevance(spec.domain, requested_domain),
                        confidence=self._confidence(row),
                        context_match=self._context_match(row, intent),
                        authority=self._authority(row),
                        provenance=self._provenance(table, row),
                        metadata={"table": table, "memory_role": spec.role},
                    )
                )
        return tuple(candidates)

    @staticmethod
    def _row_id(row: Mapping[str, Any]) -> str:
        for key in (
            "id", "experience_id", "learning_id", "concept_id", "conceito_id", "padrao_id",
            "calculation_memory_id", "memoria_id", "orcamento_id", "associacao_id", "varredura_id",
            "correlation_id", "source_id", "codigo_excedente",
        ):
            if row.get(key) is not None:
                return str(row[key])
        return "unidentified"

    @staticmethod
    def _scope_matches(row: Mapping[str, Any], intent: IntentSpec) -> bool:
        requested_scope = intent.metadata.get("scope")
        if requested_scope is None:
            return True

        scope = row.get("scope") or row.get("scope_key") or row.get("tenant_scope")
        if scope is None:
            return False

        scope = str(scope)
        requested_scope = str(requested_scope)

        # Governed inheritance: GLOBAL memory is reusable by a scoped request.
        # A scoped record remains restricted to its own scope.
        if scope == "GLOBAL":
            return True
        return scope == requested_scope

    @staticmethod
    def _content(row: Mapping[str, Any], spec: MemoryTableSpec) -> str:
        for key in (
            "finding", "description", "titulo", "nome", "objetivo", "premissa", "assessment", "diagnosis",
            "resultado", "result", "evidencia", "evidencias", "contexto", "context", "formula",
            "justificativa", "recommendation", "item", "material", "conteudo", "decisao", "descricao",
            "funcao",
        ):
            value = row.get(key)
            if value not in (None, "", [], {}):
                return f"{spec.table}: {value}"
        return f"{spec.table}: record available"

    @staticmethod
    def _status(row: Mapping[str, Any]) -> str:
        return "GOVERNED" if row.get("status") else "REFERENCE"

    @staticmethod
    def _confidence(row: Mapping[str, Any]) -> float:
        try:
            return float(row.get("confidence", 1.0))
        except (TypeError, ValueError):
            return 1.0

    @staticmethod
    def _relevance(table_domain: str, requested_domain: str) -> float:
        return 1.0 if table_domain.lower() == requested_domain else 0.5

    @staticmethod
    def _context_match(row: Mapping[str, Any], intent: IntentSpec) -> bool:
        return True

    @staticmethod
    def _authority(row: Mapping[str, Any]) -> str:
        return str(row.get("authority", "supabase"))

    @staticmethod
    def _provenance(table: str, row: Mapping[str, Any]) -> dict[str, Any]:
        result: dict[str, Any] = {"storage": "supabase", "table": table}
        if row.get("source_reference") is not None:
            result["source_reference"] = row["source_reference"]
        return result
