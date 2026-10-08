"""Read-only adapter for ELO's existing Supabase learning-memory fabric.

The adapter maps caller-supplied rows into the canonical agentic knowledge
contract. It never connects to Supabase, persists data, authorizes access,
promotes learning, or mutates canonical state.
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
    MemoryTableSpec("elo_experience_records","corporate","experience","Experiences with context, decomposition, action sequence, decisions, verification, result, errors and corrections."),
    MemoryTableSpec("elo_reasoning_patterns","corporate","reasoning","Reusable reasoning patterns, triggers, sequence, decision rules and heuristics."),
    MemoryTableSpec("elo_specializations","corporate","specialization","Scoped specialization with prerequisites, knowledge, reasoning patterns and decision rules."),
    MemoryTableSpec("elo_aprendizado_experiencias","learning","learning_experience","Learning experiences with input, decomposition, sequence, decisions, verification, result, errors and corrections."),
    MemoryTableSpec("elo_aprendizado_conceitos","learning","concept","Governed concepts associated with domains and optional specializations."),
    MemoryTableSpec("elo_aprendizado_padroes_raciocinio","learning","learning_reasoning","Learning reasoning patterns with triggers, sequence, decision rules, heuristics and evidence."),
    MemoryTableSpec("elo_aprendizado_especializacoes","learning","learning_specialization","Learning specializations with context, prerequisites, guidance, errors and evidence."),
    MemoryTableSpec("elo_aprendizado_relacoes","learning","learning_relation","Typed weighted relations between learning entities."),
    MemoryTableSpec("elo_aprendizado_extracoes","learning","extraction","Provenance-preserving extraction links from sources to experiences, concepts and patterns."),
    MemoryTableSpec("elo_aprendizado_fontes","learning","source","Configured learning sources and extraction rules."),
    MemoryTableSpec("elo_orcamentos","orcamento","budget_run","Budget identity and current context."),
    MemoryTableSpec("elo_orcamento_memoria","orcamento","budget_memory","Budget memory with calculation memory, evidence, confidence and governance fields."),
    MemoryTableSpec("elo_orcamento_calculos_aprendidos","orcamento","budget_calculation","Learned budget calculations, formulas, premises, results, validation and provenance."),
    MemoryTableSpec("elo_orcamento_calculo_evidencias","orcamento","budget_evidence","Evidence supporting learned budget calculations."),
    MemoryTableSpec("elo_orcamento_calculo_similaridades","orcamento","budget_similarity","Similarity links between learned calculations."),
    MemoryTableSpec("elo_orcamento_associacoes","orcamento","budget_association","Budget associations, occurrences, arbitrated decisions and weighting."),
    MemoryTableSpec("elo_orcamento_decisoes","orcamento","budget_decision","Budget decisions and arbitration records."),
    MemoryTableSpec("excedentes","orcamento","excess","Canonical excess records for material and/or labor composition."),
    MemoryTableSpec("excedente_itens","orcamento","excess_item","Material/component lines belonging to an excess record and linked to LISTA_MAE by cod_produt."),
    MemoryTableSpec("excedente_mao_obra","orcamento","excess_labor","Labor lines belonging to an excess record; kept separate from material lines."),
    MemoryTableSpec("elo_audit_log","governance","audit","Immutable operational audit trail with correlation and entity references."),
    MemoryTableSpec("elo_evolution_events","governance","evolution","Governed evolution events sourced from experience/pattern evidence."),
    MemoryTableSpec("elo_automation_registry","automation","automation","Automation definitions and validation requirements."),
    MemoryTableSpec("elo_automation_runs","automation","automation_run","Automation execution history."),
    MemoryTableSpec("elo_aprendizado_automacoes","automation","learning_automation","Learning automation definitions."),
    MemoryTableSpec("elo_aprendizado_automacao_execucoes","automation","learning_automation_run","Learning automation execution history."),
)
_TABLE_BY_NAME={x.table:x for x in MEMORY_TABLES}
_REQUIREMENT_TABLES={
"calculation_memory":("elo_orcamento_memoria","elo_orcamento_calculos_aprendidos"),
"budget_template":(),"applicable_composition":("elo_orcamento_memoria","elo_orcamento_calculos_aprendidos"),
"current_requirements":("elo_orcamentos","elo_orcamento_memoria","elo_aprendizado_experiencias"),
"budget_lines":(),"materials":("elo_orcamento_memoria","elo_aprendizado_experiencias"),
"labor":("elo_orcamento_memoria","elo_aprendizado_experiencias"),"equipment":("elo_orcamento_memoria","elo_aprendizado_experiencias"),
"excesses":("excedentes","excedente_itens","excedente_mao_obra","elo_orcamento_associacoes","elo_orcamento_calculos_aprendidos"),
"requirements":("elo_aprendizado_experiencias","elo_aprendizado_conceitos"),"specifications":("elo_aprendizado_experiencias","elo_aprendizado_conceitos"),
"standards":("elo_aprendizado_conceitos","elo_aprendizado_experiencias"),"constraints":("elo_aprendizado_conceitos","elo_aprendizado_experiencias"),
"scope":("elo_orcamentos","elo_aprendizado_experiencias"),"dependencies":("elo_aprendizado_experiencias","elo_aprendizado_padroes_raciocinio"),
"resources":("elo_aprendizado_experiencias","elo_aprendizado_conceitos"),"duration":("elo_aprendizado_experiencias",),
"item":("elo_orcamento_memoria","elo_aprendizado_experiencias"),"price":("elo_orcamento_memoria","elo_orcamento_calculos_aprendidos"),
"calculations":("elo_orcamento_calculos_aprendidos","elo_aprendizado_experiencias"),"conflicts":("elo_aprendizado_experiencias","elo_orcamento_decisoes"),
"gaps":("elo_aprendizado_experiencias","elo_orcamento_decisoes"),"patterns":("elo_reasoning_patterns","elo_aprendizado_padroes_raciocinio"),
"learning":("elo_aprendizado_conceitos","elo_aprendizado_extracoes","elo_aprendizado_relacoes")}

class SupabaseLearningMemoryAdapter:
    def __init__(self, rows_by_table: Mapping[str, Sequence[Mapping[str, Any]]]) -> None:
        self._rows={name:tuple(rows) for name,rows in rows_by_table.items()}
    @staticmethod
    def inventory()->tuple[MemoryTableSpec,...]: return MEMORY_TABLES
    def retrieve(self,intent:IntentSpec,requirement:KnowledgeRequirement)->tuple[KnowledgeCandidate,...]:
        tables=_REQUIREMENT_TABLES.get(requirement.key)
        requested_domain=(intent.domain or "").casefold()
        requested_scope=str(intent.metadata.get("scope") or "").strip()
        requested_address=str(intent.metadata.get("resource_address") or "").strip()
        scoped_table=requested_address.removeprefix("public.") if requested_address.startswith("public.") else None
        if scoped_table:
            tables=(scoped_table,) if scoped_table in _TABLE_BY_NAME else ()
        if not tables: return ()
        candidates=[]
        for table in tables:
            spec=_TABLE_BY_NAME.get(table)
            if spec is None: continue
            for index,row in enumerate(self._rows.get(table,())):
                row_scope=str(row.get("scope") or "").strip()
                if requested_scope and row_scope!=requested_scope: continue
                source_value=(row.get("id") or row.get("memoria_id") or row.get("learning_id") or row.get("experience_id") or row.get("concept_id") or row.get("calculo_id") or row.get("decision_id") or row.get("orcamento_id") or f"row-{index}")
                source_id=f"supabase:{table}:{source_value}"
                content="; ".join(f"{k}={v}" for k,v in row.items() if v is not None)
                domain_match=1.0 if not requested_domain or spec.domain.casefold()==requested_domain else 0.5
                confidence_value=row.get("confidence",row.get("confianca",0.0))
                try: confidence=float(confidence_value or 0.0)
                except (TypeError,ValueError): confidence=0.0
                status="REFERENCE"
                if spec.role in {"budget_memory","budget_calculation","learning_experience","experience","reasoning","specialization"}:
                    status="GOVERNED" if row.get("status") in {"VALIDADO","GOVERNED","APPROVED"} or spec.role in {"budget_memory","budget_calculation"} else "REFERENCE"
                provenance={"storage":"supabase","table":table,"source_reference":str(row.get("source_reference") or row.get("origem_so") or row.get("origem_referencia") or row.get("fonte") or "")}
                metadata={"scope":row_scope,"role":spec.role,"memory_role":spec.role,"canonical_mutation":"false"}
                candidates.append(KnowledgeCandidate(source_id=source_id,content=content,source_type=spec.role,status=status,relevance=domain_match,confidence=max(0.0,min(1.0,confidence)),context_match=domain_match,provenance=provenance,metadata=metadata))
        return tuple(candidates)
__all__=["MEMORY_TABLES","MemoryTableSpec","SupabaseLearningMemoryAdapter"]
