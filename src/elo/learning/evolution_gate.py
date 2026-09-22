"""Evolution Gate do Loop Simbionte ELO.

O Gate decide se uma evidência de aprendizado pode avançar no ciclo de
validação. Ele não executa a promoção canônica: produz uma decisão governada
e os dados necessários para posterior persistência/auditoria.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Union


class GateDecision(str, Enum):
    PROMOVER = "PROMOVER"
    RETER = "RETER"
    REJEITAR = "REJEITAR"
    SOLICITAR_MAIS_EVIDENCIA = "SOLICITAR_MAIS_EVIDENCIA"
    REPLAN = "REPLAN"


class ValidationLevel(str, Enum):
    CANDIDATE = "CANDIDATE"
    TESTED = "TESTED"
    VALIDATED = "VALIDATED"
    CONSOLIDATED = "CONSOLIDATED"


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    source: str
    kind: str = "UNKNOWN"
    provenance: Optional[str] = None
    independent_key: Optional[str] = None

    def audit_record(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "source": self.source,
            "kind": self.kind,
            "provenance": self.provenance,
            "independent_key": self.independent_key,
        }


EvidenceInput = Union[Evidence, str]


@dataclass
class GateInput:
    experience_id: Optional[str] = None
    pattern_id: Optional[str] = None
    evidence: List[EvidenceInput] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    current_rule: Optional[str] = None
    test_result: Optional[str] = None
    confidence: float = 0.0
    impact: Optional[str] = None
    applicability: Optional[str] = None
    limitations: List[str] = field(default_factory=list)
    regression_passed: bool = False
    reproducible: bool = False
    contradictions: List[str] = field(default_factory=list)
    duplicates: List[str] = field(default_factory=list)


@dataclass
class GateOutput:
    decision: GateDecision
    reason: str
    from_level: Optional[str] = None
    to_level: Optional[str] = None
    experience_id: Optional[str] = None
    pattern_id: Optional[str] = None
    evidence_used: List[Dict[str, Any]] = field(default_factory=list)
    criteria: Dict[str, Any] = field(default_factory=dict)

    def to_evolution_event(self) -> Dict[str, Any]:
        """Monta payload lógico; não executa INSERT no Supabase."""
        return {
            "source_experience_id": self.experience_id,
            "source_pattern_id": self.pattern_id,
            "event_type": self.decision.value,
            "from_level": self.from_level,
            "to_level": self.to_level,
            "evidence": self.evidence_used,
            "decision_reason": self.reason,
            "confidence": self.criteria.get("confidence"),
        }


class EvolutionGate:
    """Avalia promoção sem executar a promoção.

    Precedência:
    entrada inválida → evidência → contradição → duplicidade → teste →
    regressão → reprodutibilidade → confiança → aplicabilidade → promoção.
    """

    MIN_EVIDENCE_COUNT = 2
    MIN_CONFIDENCE = 0.7
    VALID_TEST_RESULTS = {"PASS", "FAIL", "PARTIAL"}

    def __init__(
        self,
        min_evidence_count: int = MIN_EVIDENCE_COUNT,
        min_confidence: float = MIN_CONFIDENCE,
        require_applicability: bool = True,
    ) -> None:
        if min_evidence_count < 1:
            raise ValueError("min_evidence_count deve ser >= 1")
        if not 0.0 <= min_confidence <= 1.0:
            raise ValueError("min_confidence deve estar entre 0 e 1")
        self.min_evidence_count = min_evidence_count
        self.min_confidence = min_confidence
        self.require_applicability = require_applicability

    @staticmethod
    def _normalize_evidence(
        evidence: Sequence[EvidenceInput],
    ) -> List[Dict[str, Any]]:
        normalized: List[Dict[str, Any]] = []
        for index, item in enumerate(evidence):
            if isinstance(item, Evidence):
                normalized.append(item.audit_record())
            elif isinstance(item, str) and item.strip():
                normalized.append(
                    {
                        "evidence_id": item,
                        "source": "UNSPECIFIED",
                        "kind": "LEGACY_REFERENCE",
                        "provenance": None,
                        "independent_key": None,
                    }
                )
            else:
                raise ValueError(
                    f"evidence[{index}] deve ser Evidence ou string não vazia"
                )
        return normalized

    @staticmethod
    def _distinct_evidence_count(evidence: List[Dict[str, Any]]) -> int:
        keys = set()
        for item in evidence:
            key = item.get("independent_key") or (
                item.get("source"),
                item.get("evidence_id"),
            )
            keys.add(key)
        return len(keys)

    def evaluate(self, gate_input: GateInput) -> GateOutput:
        evidence = self._normalize_evidence(gate_input.evidence)
        distinct_evidence_count = self._distinct_evidence_count(evidence)

        def output(
            decision: GateDecision,
            reason: str,
            *,
            from_level: Optional[str] = None,
            to_level: Optional[str] = None,
        ) -> GateOutput:
            return GateOutput(
                decision=decision,
                reason=reason,
                from_level=from_level,
                to_level=to_level,
                experience_id=gate_input.experience_id,
                pattern_id=gate_input.pattern_id,
                evidence_used=evidence,
                criteria={
                    "evidence_count": len(evidence),
                    "distinct_evidence_count": distinct_evidence_count,
                    "confidence": gate_input.confidence,
                    "test_result": gate_input.test_result,
                    "regression_passed": gate_input.regression_passed,
                    "reproducible": gate_input.reproducible,
                    "has_contradictions": bool(gate_input.contradictions),
                    "has_duplicates": bool(gate_input.duplicates),
                    "applicability": gate_input.applicability,
                },
            )

        if not 0.0 <= gate_input.confidence <= 1.0:
            return output(
                GateDecision.REPLAN,
                "Confiança fora do intervalo válido [0, 1]. Corrigir entrada.",
            )

        if distinct_evidence_count < self.min_evidence_count:
            return output(
                GateDecision.SOLICITAR_MAIS_EVIDENCIA,
                "Evidência independente insuficiente para atravessar o Gate.",
            )

        if gate_input.contradictions:
            return output(
                GateDecision.REJEITAR,
                "Aprendizado contraditório com conhecimento existente.",
            )

        if gate_input.duplicates:
            return output(
                GateDecision.REPLAN,
                "Possível duplicidade. Consolidar ou relacionar antes de promover.",
            )

        if gate_input.test_result not in self.VALID_TEST_RESULTS:
            return output(
                GateDecision.RETER,
                "Resultado de teste ausente ou inválido. Manter como candidato.",
            )

        if gate_input.test_result != "PASS":
            return output(
                GateDecision.RETER,
                "Teste não aprovado. Manter como candidato.",
            )

        if not gate_input.regression_passed:
            return output(
                GateDecision.RETER,
                "Regressão não aprovada. Não promover.",
            )

        if not gate_input.reproducible:
            return output(
                GateDecision.SOLICITAR_MAIS_EVIDENCIA,
                "Resultado não reproduzível. Solicitar mais evidência.",
            )

        if gate_input.confidence < self.min_confidence:
            return output(
                GateDecision.RETER,
                f"Confiança abaixo do mínimo ({self.min_confidence}).",
            )

        if self.require_applicability and not gate_input.applicability:
            return output(
                GateDecision.SOLICITAR_MAIS_EVIDENCIA,
                "Aplicabilidade não definida. Delimitar escopo antes de promover.",
            )

        return output(
            GateDecision.PROMOVER,
            "Todos os critérios do Gate foram atendidos.",
            from_level=ValidationLevel.VALIDATED.value,
            to_level=ValidationLevel.CONSOLIDATED.value,
        )
