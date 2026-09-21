"""Cognitive Runtime Loop (CRL). Orquestrador dos loops governados.

Não implementa estágios — apenas despacha para os loops existentes.
Refs: ADR-0014-cognitive-runtime-loop.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class Stage(str, Enum):
    OBSERVE = "observe"
    CONTEXTUALIZE = "contextualize"
    ANALYZE = "analyze"
    FORMULATE = "formulate"
    DECIDE = "decide"
    EXECUTE = "execute"
    MONITOR = "monitor"
    LEARN = "learn"
    FOLLOW_UP = "follow_up"
    REASSESS = "reassess"


@dataclass
class CRLContext:
    """Contexto compartilhado entre estágios."""
    request_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    stage_results: dict[str, Any] = field(default_factory=dict)
    audit: list[dict[str, Any]] = field(default_factory=list)


class CognitiveRuntimeLoop:
    """Orquestrador do ciclo cognitivo canônico.

    Cada estágio é delegado a um handler registrado. O CRL não
    implementa nenhum estágio — apenas coordena a passagem de
    contexto e registra auditoria.
    """

    STAGES_ORDER = [
        Stage.OBSERVE,
        Stage.CONTEXTUALIZE,
        Stage.ANALYZE,
        Stage.FORMULATE,
        Stage.DECIDE,
        Stage.EXECUTE,
        Stage.MONITOR,
        Stage.LEARN,
        Stage.FOLLOW_UP,
        Stage.REASSESS,
    ]

    def __init__(self) -> None:
        self._handlers: dict[Stage, Callable[[CRLContext], CRLContext]] = {}

    def register(
        self,
        stage: Stage,
        handler: Callable[[CRLContext], CRLContext],
    ) -> None:
        """Registra um handler para um estágio. Não cria novo estágio."""
        if stage not in self.STAGES_ORDER:
            raise ValueError(f"Estágio desconhecido: {stage}")
        self._handlers[stage] = handler

    def run(self, context: CRLContext) -> CRLContext:
        """Executa o ciclo completo.

        Estágios sem handler são pulados e auditados como skipped.
        Erros em handlers são capturados, auditados e propagados.
        """
        for stage in self.STAGES_ORDER:
            handler = self._handlers.get(stage)
            if handler is None:
                context.audit.append({
                    "stage": stage.value,
                    "status": "skipped",
                    "reason": "handler_not_registered",
                })
                continue

            try:
                context = handler(context)
                context.audit.append({
                    "stage": stage.value,
                    "status": "ok",
                })
            except Exception as exc:
                context.audit.append({
                    "stage": stage.value,
                    "status": "error",
                    "error": str(exc),
                })
                raise

        return context