"""Read-only adapter for ELO's existing Supabase learning-memory fabric.

The adapter is provider-neutral: Supabase rows are supplied by the caller and
this layer only maps the verified Elo-forge schema into KnowledgeCandidate.
It never persists, promotes, authorizes or mutates canonical state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .contracts import IntentSpec, KnowledgeCandidate, KnowledgeRequirement


@dataclass(frozen=True)
class MemoryTableSpec:
    table: str
    domain: str
    role: str
    description: str


MEMORY_TABLES: tuple[MemoryTableSpec, ...] = (
    MemoryTableSpec("elo_experience_records", "corporate", "experience", "Experiences with context, decomposition, action sequence, decisions, verification, result, errors and corrections."),
    MemoryTableSpec("elo_reasoning_patterns", "corporate", "reasoning", "Reusable reasoning patterns, triggers, sequence, decision rules and heuristics."),
    MemoryTableSpec("elo_specializations", "corporate", "specialization", "Scoped specialization with prerequisites, knowledge, reasoning patterns and decision rules."),
    MemoryTableSpec("elo_aprendizado_experiencias", "learning", "learning_experience", "Learning experiences with input, decomposition, sequence, decisions, verification, result, errors and corrections."),
    MemoryTableSpec("elo_aprendizado_conceitos", "learning", "concept", "Governed concepts associated with domains and optional specializations."),
    MemoryTableSpec("elo_aprendizado_padroes_raciocinio", "learning", "learning_reasoning", "Learning reasoning patterns with triggers, sequence, decision rules, heuristics and evidence."),
    MemoryTableSpec("elo_aprendizado_especializacoes", "learning", "learning_specialization", "Learning specializations with context, prerequisites, guidance, errors and evidence."),
    MemoryTableSpec("elo_aprendizado_relacoes", "learning", "learning_relation", "Typed weighted relations between learning entities."),
    MemoryTableSpec("elo_aprendizado_extracoes", "learning", "extraction", "Provenance-preserving extraction links from sources to experiences, concepts and patterns."),
    MemoryTableSpec("elo_aprendizado_fontes", "learning", "source", "Configured learning sources and extraction rules."),
    MemoryTableSpec("elo_orcamentos", "orcamento", "budget_run", "Budget identity and current context."),
    MemoryTableSpec("elo_orcamento_memoria", "orcamento", "budget_memory", "Budget memory with calculation memory, evidence, confidence and governance fields."),
    MemoryTableSpec("elo_orcamento_calculos_aprendidos", "orcamento", "budget_calculation", "Learned budget calculations, formulas, premises, results, validation and provenance."),
    MemoryTableSpec("elo_orcamento_calculo_evidencias", "orcamento", "budget_evidence", "Evidence supporting learned budget calculations."),
    MemoryTableSpec("elo_orcamento_calculo_similaridades", "orcamento", "budget_similarity", "Similarity links between learned calculations."),
    MemoryTableSpec("elo_orcamento_associacoes", "orcamento", "budget_association", "Budget associations, occurrences, arbitrated decisions and weighting."),
    MemoryTableSpec("elo_orcamento_decisoes", "orcamento", "budget_decision", "Budget decisions and arbitration records."),
    MemoryTableSpec("excedentes", "orcamento", "excess", "Canonical excess records for material and/or labor composition."),
    MemoryTableSpec("excedente_itens", "orcamento", "excess_item", "Material/component lines belonging to an excess record and linked to LISTA_MAE by cod_produt."),
    MemoryTableSpec("excedente_mao_obra", "orcamento", "excess_labor", "Labor lines belonging to an excess record; kept separate from material lines."),
    MemoryTableSpec("elo_audit_log", "governance", "audit", "Immutable operational audit trail with correlation and entity references."),
    MemoryTableSpec("elo_evolution_events", "governance", "evolution", "Governed evolution events sourced from experience/pattern evidence."),
    MemoryTableSpec("elo_automation_registry", "automation", "automation", "Automation definitions and validation requirements."),
    MemoryTableSpec("elo_automation_runs", "automation", "automation_run", "Automation execution history."),
    MemoryTableSpec("elo_aprendizado_automacoes", "automation", "learning_automation", "Learning automation definitions."),
    MemoryTableSpec("elo_aprendizado_automacao_execucoes", "automation", "learning_automation_run", "Learning automation execution history."),
)

_TABLE_BY_NAME = {item.table: item for item in MEMORY_TABLES}

_REQUIREMENT_TABLES: Mapping[str, tuple[str, ...]] = {
    "calculation_memory": ("elo_orcamento_memoria", "elo_orcamento_calculos_aprendidos"),
    "budget_template": (),
    "applicable_composition": ("elo_orcamento_memoria", "elo_orcamento_calculos_aprendidos"),
    "current_requirements": ("elo_orcamentos", "elo_orcamento_memoria", "elo_aprendizado_experiencias"),
    "budget_lines": (),
    "materials": ("elo_orcamento_memoria", "elo_aprendizado_experiencias"),
    "labor": ("elo_orcamento_memoria", "elo_aprendizado_experiencias"),
    "equipment": ("elo_orcamento_memoria", "elo_aprendizado_experiencias"),
    "excesses": ("excedentes", "excedente_itens", "excedente_mao_obra", "elo_orcamento_associacoes", "elo_orcamento_calculos_aprendidos"),
    "requirements": ("elo_aprendizado_experiencias", "elo_aprendizado_conceitos"),
    "specifications": ("elo_aprendizado_experiencias", "elo_aprendizado_conceitos"),
    "standards": ("elo_aprendizado_conceitos", "elo_aprendizado_experiencias"),
    "constraints": ("elo_aprendizado_conceitos", "elo_aprendizado_experiencias"),
    "scope": ("elo_orcamentos", "elo_aprendizado_experiencias"),
    "dependencies": ("elo_aprendizado_experiencias", "elo_aprendizado_padroes_raciocinio"),
    "resources": ("elo_aprendizado_experiencias", "elo_aprendizado_conceitos"),
    "duration": ("elo_aprendizado_experiencias",),
    "item": ("elo_orcamento_memoria", "elo_aprendizado_experiencias"),
    "price": ("elo_orcamento_memoria", "elo_orcamento_calculos_aprendidos"),
    "calculations": ("elo_orcamento_calculos_aprendidos", "elo_aprendizado_experiencias"),
    "conflicts": ("elo_aprendizado_experiencias", "elo_orcamento_decisoes"),
    "gaps": ("elo_aprendizado_experiencias", "elo_orcamento_decisoes"),
    "patterns": ("elo_reasoning_patterns", "elo_aprendizado_padroes_raciocinio"),
    "learning": ("elo_aprendizado_conceitos", "elo_aprendizado_extracoes", "elo_aprendizado_relacoes"),
}


class SupabaseLearningMemoryAdapter:
    """Resolve requirements against supplied Elo-forge rows without persistence."""

    def __init__(self, rows_by_table: Mapping[str, Sequence[Mapping[str, Any]]]) -> None:
        self._rows = {name: tuple(rows) for name, rows in rows_by_table.items()}

    @staticmethod
    def inventory() -> tuple[MemoryTableSpec, ...]:
        return MEMORY_TABLES

    def retrieve(self, intent: IntentSpec, requirement: KnowledgeRequirement) -> tuple[KnowledgeCandidate, ...]:
        tables = _REQUIREMENT_TABLES.get(requirement.key)
        if not tables:
            return ()
        candidates: list[KnowledgeCandidate] = []
        requested_domain = (intent.domain or "").casefold()\n        requested_address = str(intent.metadata.get("resource_address") or "").strip()\n        scoped_tables = None\n        if requested_address.startswith("public."):\n            requested_table = requested_address.removeprefix("public.")\n            scoped_tables = {requested_table}
        for table in tables:\n            if scoped_tables is not None and table not in scoped_tables:\n                continue
            spec = _TABLE_BY_NAME[table]
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
        return scope is not None and str(scope) == requested_scope

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
        raw = str(
            row.get("status")
            or row.get("status_validacao")
            or row.get("validation_status")
            or row.get("promotion_status")
            or "UNVERIFIED"
        ).upper()
        if raw in {"VALIDATED", "CANONICAL", "INCORPORATED", "CURRENT", "VALIDADO", "APROVADO"}:
            return "GOVERNED"
        if raw in {"CANDIDATE", "OBSERVED", "PROVISORIO", "EM_ANALISE", "PENDENTE"}:
            return "REFERENCE"
        if raw in {"REJECTED", "DESCARTADO", "OUTDATED", "REPROVADO"}:
            return "OUTDATED"
        return "UNVERIFIED"

    @staticmethod
    def _confidence(row: Mapping[str, Any]) -> float:
        for key in ("confidence", "confianca", "valor_aprendizado"):
            value = row.get(key)
            if value is not None:
                try:
                    return max(0.0, min(1.0, float(value)))
                except (TypeError, ValueError):
                    return 0.0
        return 0.0

    @staticmethod
    def _authority(row: Mapping[str, Any]) -> str | None:
        for key in ("source_system", "fonte", "origem", "arbitrado_por"):
            if row.get(key):
                return str(row[key])
        return None

    @staticmethod
    def _provenance(table: str, row: Mapping[str, Any]) -> Mapping[str, str]:
        result = {"storage": "supabase", "project": "fxbpevjrkwhbicpmecow", "table": table}
        for key in ("source_reference", "origem_referencia", "origem_so", "origem_documento", "documento_origem", "referencia_so"):
            if row.get(key):
                result["source_reference"] = str(row[key])
                break
        return result

    @staticmethod
    def _relevance(table_domain: str, requested_domain: str) -> float:
        if not requested_domain:
            return 0.5
        return 1.0 if table_domain in requested_domain or requested_domain in table_domain else 0.5

    @staticmethod
    def _context_match(row: Mapping[str, Any], intent: IntentSpec) -> float:
        entity = intent.entity
        if not entity:
            return 0.5
        haystack = " ".join(
            str(row.get(key, ""))
            for key in (
                "context", "contexto", "description", "descricao", "finding", "premise", "premissa",
                "notes", "objetivo", "request_reference", "decision_reference", "origem_so", "orcamento_id",
                "codigo_excedente", "tipo_instalacao", "funcao",
            )
        )
        return 1.0 if entity.casefold() in haystack.casefold() else 0.0


__all__ = ["MEMORY_TABLES", "MemoryTableSpec", "SupabaseLearningMemoryAdapter"]
