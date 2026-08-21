"""Governed ELO budgeting execution primitives.

This module intentionally separates canonical data resolution, relationship
checks, specialist escalation, and learning admission. Prices remain external
inputs and are never invented by the engine.
"""
from dataclasses import dataclass, field
from typing import Any, Literal

Decision = Literal["AUTO", "SPECIALIST", "BLOCKED"]

@dataclass
class BudgetItem:
    code: str
    description: str
    quantity: float
    unit: str
    source: str = "canonical"
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class AuditFinding:
    rule: str
    severity: Literal["INFO", "WARNING", "CRITICAL"]
    message: str
    decision: Decision

@dataclass
class BudgetExecution:
    base_model: str | None
    items: list[BudgetItem]
    findings: list[AuditFinding]
    decision: Decision
    specialist_question: str | None = None

class BudgetExecutionEngine:
    """Resolve a request without silently mutating canonical models."""

    def execute(self, request: dict[str, Any], canonical_model: dict[str, Any] | None) -> BudgetExecution:
        findings: list[AuditFinding] = []
        items: list[BudgetItem] = []
        model_code = canonical_model.get("code") if canonical_model else None

        if canonical_model:
            for item in canonical_model.get("standard_items", []):
                items.append(BudgetItem(**item))
        else:
            findings.append(AuditFinding(
                "MODEL_MATCH_REQUIRED", "CRITICAL",
                "Nenhum modelo canônico foi identificado com segurança.", "SPECIALIST"
            ))

        for excess in request.get("excess_items", []):
            items.append(BudgetItem(
                code=excess["code"],
                description=excess["description"],
                quantity=excess["quantity"],
                unit=excess["unit"],
                source="request_excess",
                metadata=excess.get("metadata", {}),
            ))

        if request.get("relationship_checks_pending"):
            findings.append(AuditFinding(
                "RELATIONSHIP_AUDIT", "WARNING",
                "Existem relações de composição/interligação pendentes de auditoria.", "SPECIALIST"
            ))

        decision: Decision = "SPECIALIST" if any(f.decision == "SPECIALIST" for f in findings) else "AUTO"
        question = None
        if decision == "SPECIALIST":
            question = request.get(
                "specialist_question",
                "Posso dar seguimento às evoluções identificadas após a auditoria das relações?"
            )
        return BudgetExecution(model_code, items, findings, decision, question)
