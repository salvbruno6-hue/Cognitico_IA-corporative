"""Governed interview protocol for capturing budget-building experience.

This module does not infer learning and does not persist data. It asks a small,
phase-specific set of questions during an orçamento so the final experience
captures the reasoning behind the result, not only the final number.
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

    def _answers_by_prefix(self, prefix: str) -> dict[str, Any]:
        return {k: v for k, v in self.answers.items() if k.startswith(prefix + "_")}


_QUESTIONS: tuple[InterviewQuestion, ...] = (
    # START — establish the decision context before calculations dominate the work.
    InterviewQuestion("context_objective", BudgetPhase.START, "Qual é o objetivo deste orçamento e qual resultado precisa ser entregue?", "fixar objetivo e escopo", required=True),
    InterviewQuestion("context_requirements", BudgetPhase.START, "Quais requisitos da solicitação realmente podem mudar a solução, quantidade ou custo?", "separar requisitos decisivos de informação acessória", required=True),
    InterviewQuestion("context_uncertainty", BudgetPhase.START, "O que ainda não está claro ou precisa ser confirmado antes de definir a solução?", "registrar incertezas antes da decisão", required=True),
    InterviewQuestion("knowledge_precedent", BudgetPhase.START, "Existe precedente, modelo, composição ou regra conhecida que você pretende considerar? Por quê?", "capturar conhecimento utilizado e sua aplicabilidade"),
    InterviewQuestion("context_constraints", BudgetPhase.START, "Há restrição técnica, contratual, prazo, logística ou comercial que limite as alternativas?", "capturar condicionantes do orçamento"),

    # MIDDLE — interrogate the reasoning while decisions and calculations are still reversible.
    InterviewQuestion("decision_change", BudgetPhase.MIDDLE, "O que mudou ou ficou mais claro desde o início e qual decisão isso provocou?", "capturar evolução do entendimento", required=True),
    InterviewQuestion("decision_alternative", BudgetPhase.MIDDLE, "Qual alternativa foi considerada e por que a solução adotada foi escolhida?", "capturar comparação e motivo da decisão", required=True),
    InterviewQuestion("decision_critical", BudgetPhase.MIDDLE, "Qual decisão até aqui tem maior impacto no valor ou na viabilidade do orçamento?", "identificar decisão de maior impacto"),
    InterviewQuestion("knowledge_used", BudgetPhase.MIDDLE, "Que informação, precedente, regra, produto ou experiência foi determinante para esta decisão?", "ligar decisão à fonte de conhecimento"),
    InterviewQuestion("evidence_calculation", BudgetPhase.MIDDLE, "Qual cálculo, premissa ou evidência sustenta esta escolha?", "ligar raciocínio à evidência"),
    InterviewQuestion("problem_gap", BudgetPhase.MIDDLE, "Encontrou algum erro, incongruência ou informação ausente? Como isso foi tratado?", "capturar problema e correção durante a construção"),

    # END — reconstruct what actually determined the final budget.
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
