"""Read-only adapter for ELO's existing Supabase learning-memory fabric.

The adapter deliberately consumes already-retrieved rows. It does not connect to
Supabase, mutate records, promote learning, or create a second memory store.
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
    MemoryTableSpec("elo_experience_record", "corporate", "experience", "Observed experience, context, decisions, verification, errors and outcomes."),
    MemoryTableSpec("elo_experience_pattern", "corporate", "pattern", "Reusable patterns extracted from comparable experiences."),
    MemoryTableSpec("elo_reasoning_pattern", "corporate", "reasoning", "Reusable reasoning approaches, heuristics and decision patterns."),
    MemoryTableSpec("elo_corporate_learning", "corporate", "learning", "Explicit learning supported by evidence, provenance, scope and governance state."),
    MemoryTableSpec("elo_specialization_profile", "corporate", "specialization", "Scoped specialized knowledge and context."),
    MemoryTableSpec("elo_corporate_assessment", "corporate", "assessment", "Corporate assessments combining evidence from multiple domains."),
    MemoryTableSpec("elo_corporate_advisory", "corporate", "advisory", "Diagnoses and recommendations linked to evidence and learning."),
    MemoryTableSpec("elo_pts_pos", "corporate", "arbitration", "Governed positions and arbitration states."),
    MemoryTableSpec("elo_orcament_calculation_memory", "orcamento", "budget_memory", "Reusable budget premises, formulas, results and reuse conditions."),
    MemoryTableSpec("elo_orcament_run", "orcamento", "budget_run", "Concrete budget runs, inputs, outputs and decision traces."),
    MemoryTableSpec("elo_orcament_association", "orcamento", "budget_relation", "Relationships among budget entities."),
    MemoryTableSpec("elo_quality_inspection", "qualidade", "quality_evidence", "Quality inspection evidence."),
    MemoryTableSpec("elo_quality_nonconformity", "qualidade", "quality_evidence", "Quality nonconformity evidence."),
    MemoryTableSpec("elo_pcp_demanda", "pcp", "planning", "PCP demand context."),
    MemoryTableSpec("elo_pcp_ordem_pcp", "pcp", "planning", "PCP order context."),
    MemoryTableSpec("elo_pcp_planejamento_dia", "pcp", "planning", "Daily PCP planning context."),
    MemoryTableSpec("elo_pcp_mrp_necessidade", "pcp", "planning", "MRP material requirement context."),
    MemoryTableSpec("elo_pcp_fluxo_modular", "pcp", "production", "Modular production-flow context."),
    MemoryTableSpec("elo_pcp_fluxo_paralelo", "pcp", "production", "Parallel-flow context."),
)

_TABLE_BY_NAME = {item.table: item for item in MEMORY_TABLES}

# Requirement keys are intentionally explicit. Unknown keys are not guessed.
_REQUIREMENT_TABLES: Mapping[str, tuple[str, ...]] = {
    "calculation_memory": ("elo_orcament_calculation_memory", "elo_orcament_run"),
    "current_requirements": ("elo_orcament_run", "elo_experience_record"),
    "materials": ("elo_pcp_mrp_necessidade",),
    "labor": ("elo_experience_record",),
    "equipment": ("elo_experience_record",),
    "excesses": ("elo_orcament_association", "elo_orcament_calculation_memory"),
    "requirements": ("elo_experience_record",),
    "specifications": ("elo_experience_record",),
    "standards": ("elo_corporate_learning", "elo_pts_pos"),
    "constraints": ("elo_corporate_learning", "elo_experience_record"),
    "scope": ("elo_pcp_demanda", "elo_pcp_ordem_pcp"),
    "dependencies": ("elo_pcp_ordem_pcp", "elo_pcp_fluxo_modular"),
    "resources": ("elo_pcp_fluxo_modular", "elo_pcp_fluxo_paralelo"),
    "duration": ("elo_pcp_planejamento_dia", "elo_experience_record"),
    "item": ("elo_pcp_mrp_necessidade",),
    "price": ("elo_orcament_calculation_memory", "elo_orcament_run"),
    "lead_time": ("elo_pcp_mrp_necessidade",),
}


class SupabaseLearningMemoryAdapter:
    """Resolve requirements against supplied Supabase rows without persistence."""

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
        requested_domain = (intent.domain or "").casefold()
        for table in tables:
            spec = _TABLE_BY_NAME[table]
            for row in self._rows.get(table, ()):
                if not self._scope_matches(row, intent):
                    continue
                content = self._content(row, spec)
                candidates.append(
                    KnowledgeCandidate(
                        source_id=f"supabase:{table}:{self._row_id(row)}",
                        content=content,
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
        for key in ("experience_id", "learning_id", "reasoning_pattern_id", "experience_pattern_id", "calculation_memory_id", "budget_run_id", "association_id", "inspection_id", "nonconformity_id", "demanda_id", "ordem_pcp_id", "planejamento_dia_id", "mrp_need_id", "fluxo_modular_id", "fluxo_paralelo_id"):
            if row.get(key) is not None:
                return str(row[key])
        return "unidentified"

    @staticmethod
    def _scope_matches(row: Mapping[str, Any], intent: IntentSpec) -> bool:
        scope = row.get("scope")
        requested_scope = intent.metadata.get("scope")
        return requested_scope is None or scope is None or str(scope) == requested_scope

    @staticmethod
    def _content(row: Mapping[str, Any], spec: MemoryTableSpec) -> str:
        for key in ("finding", "description", "premise", "assessment", "diagnosis", "result", "notes", "context"):
            value = row.get(key)
            if value not in (None, ""):
                return f"{spec.table}: {value}"
        return f"{spec.table}: record available"

    @staticmethod
    def _status(row: Mapping[str, Any]) -> str:
        raw = str(row.get("status") or row.get("validation_status") or row.get("promotion_status") or "UNVERIFIED").upper()
        if raw in {"VALIDATED", "CANONICAL", "INCORPORATED", "CURRENT", "PROVISORIO", "CANDIDATE", "OBSERVED"}:
            return "GOVERNED" if raw in {"VALIDATED", "INCORPORATED", "CANONICAL"} else "REFERENCE"
        if raw in {"REJECTED", "DESCARTADO", "OUTDATED"}:
            return "OUTDATED"
        return "UNVERIFIED"

    @staticmethod
    def _confidence(row: Mapping[str, Any]) -> float:
        value = row.get("confidence")
        try:
            return max(0.0, min(1.0, float(value))) if value is not None else 0.0
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _authority(row: Mapping[str, Any]) -> str | None:
        return str(row["source_system"]) if row.get("source_system") else None

    @staticmethod
    def _provenance(table: str, row: Mapping[str, Any]) -> Mapping[str, str]:
        result = {"storage": "supabase", "table": table}
        if row.get("source_reference"):
            result["source_reference"] = str(row["source_reference"])
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
        haystack = " ".join(str(row.get(key, "")) for key in ("context", "description", "finding", "premise", "notes"))
        return 1.0 if entity.casefold() in haystack.casefold() else 0.0


__all__ = ["MEMORY_TABLES", "MemoryTableSpec", "SupabaseLearningMemoryAdapter"]
