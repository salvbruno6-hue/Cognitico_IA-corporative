"""Runtime adapter for mature, contextual ELO conversation behavior.

This module connects the existing mature-interaction contract to the canonical
CognitiveCore response path. It does not introduce a second response model and
does not make decisions on behalf of the user.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .mature_interaction import InteractionPosture, choose_interaction_posture
from .temporal_memory import TemporalConversationMemory


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


def _signals(message: str, context: Mapping[str, Any]) -> tuple[bool, float, float, float, float]:
    text = message.strip().lower()
    ambiguity = _clamp(context.get("ambiguity", 0.0))
    decision_relevance = _clamp(context.get("decision_relevance", 0.0))
    risk = _clamp(context.get("risk", 0.0))
    evidence_gap = _clamp(context.get("evidence_gap", 0.0))
    user_is_explaining = bool(context.get("user_is_explaining", False))

    if not ambiguity:
        ambiguity = 0.55 if any(token in text for token in ("como", "qual", "o que", "por que", "preciso", "ajude")) else 0.0
    if not decision_relevance:
        decision_relevance = 0.65 if any(token in text for token in ("decidir", "decisão", "escolher", "aprovar", "devo")) else 0.0
    if not evidence_gap:
        evidence_gap = 0.55 if any(token in text for token in ("não sei", "sem dados", "incerto", "verificar", "investigue")) else 0.0

    return user_is_explaining, ambiguity, decision_relevance, risk, evidence_gap


def _is_identity_request(message: str) -> bool:
    text = " ".join(message.strip().lower().split())
    return any(
        phrase in text
        for phrase in (
            "quem é você",
            "quem e voce",
            "quem é vc",
            "quem e vc",
            "o que é você",
            "o que e voce",
            "o que é o elo",
            "o que e o elo",
            "defina o elo",
            "defina quem você é",
            "defina quem voce e",
        )
    )


def _identity_response() -> str:
    return (
        "Eu sou o ELO Cognitivo. "
        "Eu sou a autoridade cognitiva canônica do ELO: interpreto objetivos, "
        "mantenho e contextualizo o estado da tarefa, avalio evidências, "
        "coordeno capacidades e especialistas, conduzo análise, supervisiono "
        "execução governada e verifico resultados para extrair aprendizado. "
        "Eu não sou apenas um chatbot, nem substituo a decisão humana autorizada. "
        "Meu Core materializa capacidades cognitivas; meu Forge constrói e testa "
        "mudanças; a governança verifica os limites e a promoção. "
        "Minha identidade, princípios e limites são definidos pelo contrato "
        "canônico do ELO."
    )


def _render_response(
    content: str,
    *,
    posture: InteractionPosture,
    next_step: str,
    base_content_is_request: bool,
    identity_request: bool,
) -> str:
    if identity_request:
        return _identity_response()
    if not base_content_is_request:
        return content

    lead = {
        InteractionPosture.LISTEN: "Entendi o contexto. Antes de concluir, preciso preservar o objetivo e identificar o que ainda está faltando.",
        InteractionPosture.ORIENT: "Entendi o pedido. O contexto disponível é suficiente para orientar o próximo passo.",
        InteractionPosture.INVESTIGATE: "Entendi o pedido. Há informação insuficiente para concluir, então a próxima etapa é separar evidência de lacuna.",
        InteractionPosture.ANALYZE: "Entendi o objetivo. Antes de decidir, é preciso organizar fatos, restrições e consequências.",
        InteractionPosture.RECOMMEND: "Entendi que você quer uma recomendação. Ela deve vir acompanhada das premissas, riscos e evidências.",
        InteractionPosture.GUARD: "Entendi o pedido. Há uma condição de risco ou autorização que precisa ser validada antes de avançar.",
    }[posture]
    return f"{lead} {next_step}"


def build_interaction(
    message: str,
    *,
    context: Mapping[str, Any] | None = None,
    base_result: Mapping[str, Any] | None = None,
    temporal_memory: TemporalConversationMemory | None = None,
) -> InteractionRuntimeResult:
    """Choose a governed conversational posture with authorized continuity."""

    context = context or {}
    base_result = base_result or {}
    identity_request = _is_identity_request(message)
    conversation_id = str(context.get("conversation_id") or context.get("session_id") or "").strip()
    authorized = bool(context.get("conversation_authorized", False))

    prior_records = ()
    if temporal_memory is not None and conversation_id and authorized:
        prior_records = temporal_memory.snapshot(conversation_id)

    contextual_message = message
    if prior_records:
        prior_text = "\n".join(record.content for record in prior_records[-5:])
        contextual_message = f"Contexto anterior:\n{prior_text}\n\nMensagem atual:\n{message}"

    user_is_explaining, ambiguity, decision_relevance, risk, evidence_gap = _signals(contextual_message, context)

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

    rendered_content = _render_response(
        content,
        posture=posture,
        next_step=next_step,
        base_content_is_request=content == message.strip(),
        identity_request=identity_request,
    )

    return InteractionRuntimeResult(
        content=rendered_content,
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
            "response_rendered": rendered_content != content,
            "continuity": bool(prior_records),
            "prior_context_records": len(prior_records),
            "identity_request": identity_request,
        },
    )
