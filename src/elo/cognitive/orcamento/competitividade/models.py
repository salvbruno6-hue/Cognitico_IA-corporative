"""Domain models for supervised post-budget competitiveness analysis."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


KNOWLEDGE_STATES = {"FORTE", "MEDIO", "FRACO", "AUSENTE", "CONFLITANTE"}
FLEXIBILITY_STATES = {"ALTA", "MEDIA", "BAIXA", "INDETERMINADA"}
RISK_STATES = {"BAIXO", "MEDIO", "ALTO", "CRITICO"}
DECISION_STATES = {
    "MANTER", "REVISAR", "NEGOCIAR", "SUBSTITUIR", "REESTRUTURAR",
    "CONFIRMAR", "NAO_REDUZIR", "AGUARDAR_DECISAO",
}


@dataclass(frozen=True)
class BudgetItem:
    item_id: str
    total_value: float
    quantity: Optional[float] = None
    unit_value: Optional[float] = None
    category: Optional[str] = None
    material_name: Optional[str] = None
    unit: Optional[str] = None
    requirement_ref: Optional[str] = None
    composition_ref: Optional[str] = None
    calculation_ref: Optional[str] = None


@dataclass(frozen=True)
class CompetitivenessAssessment:
    item_id: str
    financial_weight: float
    abc_class: str
    knowledge_state: str
    flexibility_state: str
    risk_state: str
    opportunity: Optional[str] = None
    recommendation: Optional[str] = None
    evidence_refs: List[str] = field(default_factory=list)
    provenance: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.abc_class not in {"A", "B", "C"}:
            raise ValueError("abc_class must be A, B or C")
        if self.knowledge_state not in KNOWLEDGE_STATES:
            raise ValueError("invalid knowledge_state")
        if self.flexibility_state not in FLEXIBILITY_STATES:
            raise ValueError("invalid flexibility_state")
        if self.risk_state not in RISK_STATES:
            raise ValueError("invalid risk_state")
        if self.recommendation and self.recommendation not in DECISION_STATES:
            raise ValueError("invalid recommendation")


@dataclass(frozen=True)
class ScenarioResult:
    name: str
    total_value: float
    delta_value: float
    delta_percent: float
    changed_items: List[str] = field(default_factory=list)
    changed_premises: List[str] = field(default_factory=list)
    risk_state: str = "BAIXO"

    def __post_init__(self) -> None:
        if self.name not in {"BASE", "COMPETITIVO", "MAXIMO"}:
            raise ValueError("invalid scenario")
        if self.risk_state not in RISK_STATES:
            raise ValueError("invalid risk_state")
