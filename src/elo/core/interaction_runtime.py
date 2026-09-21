"""Runtime adapter for mature, contextual ELO conversation behavior.

This module connects the existing mature-interaction contract to the canonical
CognitiveCore response path. It does not introduce a second response model and
does not make decisions on behalf of the user.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .mature_interaction import InteractionPosture, choose_interaction_posture


@dataclass(frozen=True)
class InteractionRuntimeResult:
    content: str
    posture: InteractionPosture
    next_step: str | None
    uncertainty: tuple[str, ...]
    metadata: Mapping[str, Any]


def _clamp(value: Any) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def _signals(message: str, context: Mapping[str, Any]) -> tuple[bool, float, float, float, float, float]:
    text = message.strip().lower()
    ambiguity = _clamp(context.get("ambiguity", 0.0))
    decision_relevance = _clamp(context.get("decision_relevance", 0.0))
    risk = _clamp(context.get("risk", 0.0))
    evidence_gap = _clamp(context.get("evidence_gap", 0.0))
    user_is_explaining = bool(context.get("user_is_explaining", False))

    if not ambiguity:
        ambiguity = 0.55 if any(
            token in text for token in ("como", "qual", "o que", "por que", "preciso", "ajude")
        ) else 0.0
    if not decision_relevance:
        decision_relevance = 0.65 if any(
            token in text for token in ("decidir", "decisão", "escolher", "aprovar", "devo")
        ) else 0.0
    if not evidence_gap:
        evidence_gap = 0.55 if any(
            token in text for token in ("não sei", "sem dados", "incerto", "verificar", "investigue")
        ) else 0.0

    return user_is_explaining, ambiguity, decision_relevance, risk, evidence_gap, 0.0


def build_interaction(
    message: str,
    *,
    context: Mapping[str, Any] | None = None,
    base_result: Mapping[str, Any] | None = None,
) -> InteractionRuntimeResult:
    """Choose a governed conversational posture and render a natural response."""

    context = context or {}
    base_result = base_result or {}
    user_is_explaining, ambiguity, decision_relevance, risk, evidence_gap, _ = _signals(message, context)

    posture = choose_interaction_posture(
        user_is_explaining=user_is_explaining,
        ambiguity=ambiguity,
        decision_relevance=decision_relevance,
        risk=risk,
        evidence_gap=evidence_gap,
        user_requested_recommendation=bool(context.get("user_requested_recommendation", False)),
    )

    content = str(base_result.get("content") or message).strip()
    uncertainty = tuple(str(item) for item in (base_result.get("uncertainty") or ()))
    next_step: str | None = None

    if posture is InteractionPosture.LISTEN:
        next_step = "Traga o objetivo ou a informação que falta para eu orientar o próximo passo."
    elif posture is InteractionPosture.INVESTIGATE:
        next_step = "Vou separar o que já está evidenciado do que ainda precisa ser verificado."
    elif posture is InteractionPosture.ANALYZE:
        next_step = "Vou organizar os fatos, restrições e consequências antes de indicar alternativas."
    elif posture is InteractionPosture.RECOMMEND:
        next_step = "Posso apresentar a recomendação acompanhada das premissas, riscos e evidências."
    elif posture is InteractionPosture.GUARD:
        next_step = "Antes de avançar, é necessário validar a evidência e a autorização aplicável."
    else:
        next_step = "Se quiser, seguimos para o próximo passo com o contexto já disponível."

    return InteractionRuntimeResult(
        content=content,
        posture=posture,
        next_step=next_step,
        uncertainty=uncertainty,
        metadata={
            "interaction_mode": "mature_contextual",
            "posture": posture.value,
            "evidence_gap": evidence_gap,
            "ambiguity": ambiguity,
            "decision_relevance": decision_relevance,
            "risk": risk,
        },
    )
