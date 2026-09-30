"""Governed interview protocol for capturing budget-building experience.

The interview captures observed budget-building experience and exposes a
persistence-ready mapping to the existing ELO learning tables. It does not
write to Supabase, infer learning, or promote knowledge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class BudgetPhase(str, Enum):
    START = "START"
    MIDDLE = "MIDDLE"
    END = "END"


@dataclass(frozen=True)
class InterviewQuestion:
    id: str
    phase: BudgetPhase
    question: str
    objective: str
    answer_type: str = "text"
    required: bool = False


@dataclass(frozen=True)
class BudgetSourceRef:
    """Logical provenance for an existing budget record/table."""

    table_name: str
    record_key: str
    source_id: str | None = None


@dataclass
class ExperienceInterview:
    budget_ref: str
    phase: BudgetPhase
    questions: list[InterviewQuestion]
    answers: dict[str, Any] = field(default_factory=dict)

    def record(self, question_id: str, answer: Any) -> None:
        allowed = {q.id for q in self.questions}
        if question_id not in allowed:
            raise ValueError(f"question_not_in_phase:{question_id}")
        self.answers[question_id] = answer

    def unanswered_required(self) -> list[str]:
        return [q.id for q in self.questions if q.required and q.id not in self.answers]

    def to_experience_fragment(self) -> dict[str, Any]:
        """Map answers into the existing experience model without promotion."""
        return {
            "contexto": {"budget_ref": self.budget_ref, "phase": self.phase.value},
            "sequencia": [{"question_id": q.id, "objective": q.objective} for q in self.questions],
            "decisoes": self._answers_by_prefix("decision"),
            "verificacoes": self._answers_by_prefix("evidence"),
            "resultado": self._answers_by_prefix("result"),
            "erros": self._answers_by_prefix("problem"),
            "correcoes": self._answers_by_prefix("correction"),
            "conhecimentos_utilizados": self._answers_by_prefix("knowledge"),
            "nivel_experiencia_observado": "OBSERVADO",
            "status_validacao": "OBSERVADA",
            "learning_candidate": False,
            "canonical_mutation": False,
        }

    def to_persistence_plan(self, sources: list[BudgetSourceRef]) -> dict[str, Any]:
        """Build an explicit write plan for existing canonical tables.

        This function only produces data for a repository adapter. It never
        performs a database write. Missing source identity is preserved as a
        gap instead of being invented.
        """
        if not sources:
            raise ValueError("budget_source_required")

        fragment = self.to_experience_fragment()
        source_refs = [
            {"table_name": source.table_name, "record_key": source.record_key, "source_id": source.source_id}
            for source in sources
        ]
        primary = sources[0]
        origin_reference = f"{primary.table_name}:{primary.record_key}"

        return {
            "target": {
                "experience_table": "elo_aprendizado_experiencias",
                "extraction_table": "elo_aprendizado_extracoes",
                "relation_table": "elo_aprendizado_relacoes",
            },
            "experience": {
                "objetivo": self._objective(),
                "entrada": {"budget_ref": self.budget_ref, "sources": source_refs},
                "decomposicao": {"phase": self.phase.value, "questions": [q.id for q in self.questions]},
                "sequencia": fragment["sequencia"],
                "dependencias": {"budget_sources": source_refs},
                "capacidades": {"capture": "ELO-ORCAMENTO-EXPERIENCE-INTERVIEW"},
                "conhecimentos_utilizados": fragment["conhecimentos_utilizados"],
                "decisoes": fragment["decisoes"],
                "verificacoes": fragment["verificacoes"],
                "resultado": fragment["resultado"],
                "erros": fragment["erros"],
                "correcoes": fragment["correcoes"],
                "nivel_experiencia_observado": "OBSERVADO",
                "confianca": self._confidence(),
                "status_validacao": "OBSERVADA",
                "origem": primary.table_name,
                "origem_referencia": origin_reference,
            },
            "extractions": [
                {
                    "fonte_id": source.source_id,
                    "origem_chave": source.record_key,
                    "origem_hash": f"budget-interview:{self.budget_ref}:{source.table_name}:{source.record_key}",
                    "status": "OBSERVADA",
                    "evidencia": {
                        "table_name": source.table_name,
                        "record_key": source.record_key,
                        "budget_ref": self.budget_ref,
                        "phase": self.phase.value,
                    },
                }
                for source in sources
            ],
            "relations": [
                {
                    "relation_type": "derived_from",
                    "origin": {"type": "experience", "id": "$experience.id"},
                    "destination": {"type": "budget_source", "reference": origin_reference},
                    "status": "OBSERVADA",
                    "confidence": self._confidence(),
                }
            ],
            "governance": {
                "learning_candidate": False,
                "canonical_mutation": False,
                "automatic_learning_promotion": False,
                "requires_validation": True,
            },
        }

    def _objective(self) -> str:
        value = self.answers.get("context_objective")
        if value is None:
            value = self.answers.get("result_final_driver")
        return str(value) if value is not None else f"Construir orçamento {self.budget_ref}"

    def _confidence(self) -> float:
        value = self.answers.get("result_confidence")
        if isinstance(value, (int, float)) and 0 <= value <= 1:
            return float(value)
        return 0.0

    def _answers_by_prefix(self, prefix: str) -> dict[str, Any]:
        return {k: v for k, v in self.answers.items() if k.startswith(prefix + "_")}


_QUESTIONS: tuple[InterviewQuestion, ...] = (
    InterviewQuestion("context_objective", BudgetPhase.START, "Qual é o objetivo deste orçamento e qual resultado precisa ser entregue?", "fixar objetivo e escopo", required=True),
    InterviewQuestion("context_requirements", BudgetPhase.START, "Quais requisitos da solicitação realmente podem mudar a solução, quantidade ou custo?", "separar requisitos decisivos de informação acessória", required=True),
    InterviewQuestion("context_uncertainty", BudgetPhase.START, "O que ainda não está claro ou precisa ser confirmado antes de definir a solução?", "registrar incertezas antes da decisão", required=True),
    InterviewQuestion("knowledge_precedent", BudgetPhase.START, "Existe precedente, modelo, composição ou regra conhecida que você pretende considerar? Por quê?", "capturar conhecimento utilizado e sua aplicabilidade"),
    InterviewQuestion("context_constraints", BudgetPhase.START, "Há restrição técnica, contratual, prazo, logística ou comercial que limite as alternativas?", "capturar condicionantes do orçamento"),
    InterviewQuestion("decision_change", BudgetPhase.MIDDLE, "O que mudou ou ficou mais claro desde o início e qual decisão isso provocou?", "capturar evolução do entendimento", required=True),
    InterviewQuestion("decision_alternative", BudgetPhase.MIDDLE, "Qual alternativa foi considerada e por que a solução adotada foi escolhida?", "capturar comparação e motivo da decisão", required=True),
    InterviewQuestion("decision_critical", BudgetPhase.MIDDLE, "Qual decisão até aqui tem maior impacto no valor ou na viabilidade do orçamento?", "identificar decisão de maior impacto"),
    InterviewQuestion("knowledge_used", BudgetPhase.MIDDLE, "Que informação, precedente, regra, produto ou experiência foi determinante para esta decisão?", "ligar decisão à fonte de conhecimento"),
    InterviewQuestion("evidence_calculation", BudgetPhase.MIDDLE, "Qual cálculo, premissa ou evidência sustenta esta escolha?", "ligar raciocínio à evidência"),
    InterviewQuestion("problem_gap", BudgetPhase.MIDDLE, "Encontrou algum erro, incongruência ou informação ausente? Como isso foi tratado?", "capturar problema e correção durante a construção"),
    InterviewQuestion("result_final_driver", BudgetPhase.END, "O que efetivamente determinou o orçamento final?", "reconstruir os fatores determinantes", required=True),
    InterviewQuestion("result_key_decisions", BudgetPhase.END, "Quais foram as decisões mais importantes para chegar ao resultado final e por quê?", "consolidar decisões causais", required=True),
    InterviewQuestion("result_deviations", BudgetPhase.END, "O que ficou diferente do modelo, precedente ou expectativa inicial?", "capturar divergências e adaptações"),
    InterviewQuestion("evidence_final", BudgetPhase.END, "Quais evidências ou validações dão suporte ao resultado final?", "preservar sustentação do resultado", required=True),
    InterviewQuestion("knowledge_reusable", BudgetPhase.END, "O que desta experiência vale a pena ser recuperado em um próximo orçamento, e em qual contexto?", "identificar candidato a reutilização sem promover aprendizado"),
    InterviewQuestion("problem_lessons", BudgetPhase.END, "O que deu errado, quase deu errado ou precisou ser corrigido? O que foi feito?", "preservar falhas e correções para análise posterior"),
    InterviewQuestion("result_confidence", BudgetPhase.END, "Qual é o nível de confiança no resultado e o que ainda depende de confirmação?", "separar resultado concluído de pendências"),
)


def start_interview(budget_ref: str) -> ExperienceInterview:
    return ExperienceInterview(budget_ref, BudgetPhase.START, list(_questions_for(BudgetPhase.START)))


def continue_interview(budget_ref: str) -> ExperienceInterview:
    return ExperienceInterview(budget_ref, BudgetPhase.MIDDLE, list(_questions_for(BudgetPhase.MIDDLE)))


def close_interview(budget_ref: str) -> ExperienceInterview:
    return ExperienceInterview(budget_ref, BudgetPhase.END, list(_questions_for(BudgetPhase.END)))


def _questions_for(phase: BudgetPhase) -> tuple[InterviewQuestion, ...]:
    return tuple(q for q in _QUESTIONS if q.phase is phase)


def build_experience_capture(
    budget_ref: str,
    phase: BudgetPhase,
    answers: Mapping[str, Any],
) -> dict[str, Any]:
    """Build an observed experience fragment from one checkpoint."""
    interview = ExperienceInterview(budget_ref, phase, list(_questions_for(phase)))
    for question_id, answer in answers.items():
        interview.record(question_id, answer)
    return interview.to_experience_fragment()


def build_persistence_plan(
    budget_ref: str,
    phase: BudgetPhase,
    answers: Mapping[str, Any],
    sources: list[BudgetSourceRef],
) -> dict[str, Any]:
    """Build the canonical-table write plan without performing persistence."""
    interview = ExperienceInterview(budget_ref, phase, list(_questions_for(phase)))
    for question_id, answer in answers.items():
        interview.record(question_id, answer)
    return interview.to_persistence_plan(sources)
