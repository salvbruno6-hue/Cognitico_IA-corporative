"""Parser de linguagem natural para o ELO.

Aceita comandos em português e retorna payload estruturado.
Tolerante a variações formais e coloquiais.

Refs: ELO-NATURAL-LANGUAGE-PROTOCOL.
"""
from __future__ import annotations

import json
import re
from typing import Any

from ..knowledge.so_resolver import normalize_so_id
from .intents import Intent

SO_PATTERN = re.compile(
    r"\bSO[\s\-_]?(\d{3})[\s\-_.]?(\d{2})\b",
    re.IGNORECASE,
)
SO_REFERENCE_PATTERN = re.compile(r"\bSO(?=$|[\s_-])", re.IGNORECASE)
DECISION_PATTERN = re.compile(r"\bDEC[\s\-_]?(\w+)\b", re.IGNORECASE)
JSON_BLOCK_PATTERN = re.compile(
    r"<!--\s*elo-request-payload\s*(.*?)\s*-->",
    re.DOTALL,
)


def _normalize(text: str) -> str:
    return text.strip().lower()


def _extract_so_id(text: str) -> str | None:
    match = SO_PATTERN.search(text)
    if not match:
        return None
    candidate = f"SO {match.group(1)}.{match.group(2)}"
    try:
        return normalize_so_id(candidate)
    except ValueError:
        return None


def _extract_decision_id(text: str) -> str | None:
    match = DECISION_PATTERN.search(text)
    if match:
        return f"DEC_{match.group(1)}"
    return None


def _extract_body_after_command(text: str) -> str:
    """Extrai o texto após ':' ou após a primeira frase."""
    if ":" in text:
        _, _, rest = text.partition(":")
        return rest.strip()
    if "\n" in text:
        _, _, rest = text.partition("\n")
        return rest.strip()
    return ""


def _detect_intent(normalized: str) -> Intent | None:
    rules = [
        (Intent.CONFERE_ANALISE, [
            "confere", "confira", "revisa", "revise", "olha",
            "veja", "valida", "valide", "verifica", "verifique",
        ]),
        (Intent.O_QUE_SABE, [
            "o que você sabe sobre", "o que voce sabe sobre",
            "me conta sobre", "me conte sobre",
            "analisa ", "analise ", "sobre a so ",
        ]),
        (Intent.GUARDA_APRENDIZADO, [
            "guarda isso", "guarde isso", "anota", "anote",
            "registra", "registre", "aprende", "aprenda",
            "memoriza", "memorize",
        ]),
        (Intent.STATUS_DECISAO, [
            "como está a decisão", "como esta a decisao",
            "status da decisão", "status da decisao",
            "estado da decisão", "estado da decisao",
        ]),
        (Intent.LISTA_ABERTAS, [
            "o que está aberto", "o que esta aberto",
            "lista pendências", "lista pendencias",
            "quais decisões", "quais decisoes",
            "decisões abertas", "decisoes abertas",
        ]),
        (Intent.BUSCA_PRECEDENTE, [
            "já vimos algo parecido", "ja vimos algo parecido",
            "tem precedente", "busca precedente",
            "compara com", "compare com",
        ]),
    ]
    for intent, keywords in rules:
        for kw in keywords:
            if kw in normalized:
                return intent
    return None


def parse_json_block(text: str) -> dict[str, Any] | None:
    match = JSON_BLOCK_PATTERN.search(text)
    if not match:
        return None
    raw = match.group(1).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def parse_natural_request(text: str) -> dict[str, Any]:
    """Parseia comando em linguagem natural."""
    json_payload = parse_json_block(text)
    if json_payload is not None:
        return json_payload

    normalized = _normalize(text)
    intent = _detect_intent(normalized)

    if intent is None:
        return {
            "error": "intent_not_recognized",
            "text": text[:500],
            "suggestions": [
                "ELO, confere essa análise da SO NNN.AA: <texto>",
                "ELO, o que você sabe sobre a SO NNN.AA",
                "ELO, guarda isso da SO NNN.AA: <texto>",
                "ELO, como está a decisão DEC_X",
                "ELO, o que está aberto",
                "ELO, já vimos algo parecido com a SO NNN.AA",
            ],
        }

    payload: dict[str, Any] = {"intent": intent.value}
    payload["question"] = text.strip()

    so_id = _extract_so_id(text)
    so_intents = {
        Intent.CONFERE_ANALISE,
        Intent.O_QUE_SABE,
        Intent.GUARDA_APRENDIZADO,
        Intent.BUSCA_PRECEDENTE,
    }
    if intent in so_intents and SO_REFERENCE_PATTERN.search(text) and so_id is None:
        return {
            **payload,
            "error": "invalid_so_id",
            "so_id": None,
            "message": "Informe a SO atribuída no formato canônico SO NNN.AA.",
        }

    if intent == Intent.CONFERE_ANALISE:
        payload["so_id"] = so_id
        payload["chatgpt_analysis"] = _extract_body_after_command(text)
    elif intent == Intent.O_QUE_SABE:
        payload["so_id"] = so_id
    elif intent == Intent.GUARDA_APRENDIZADO:
        payload["so_id"] = so_id
        payload["learning"] = _extract_body_after_command(text)
    elif intent == Intent.STATUS_DECISAO:
        payload["decision_id"] = _extract_decision_id(text)
    elif intent == Intent.LISTA_ABERTAS:
        payload["state_filter"] = [
            "proposed", "approved", "executed",
            "observing", "evaluated", "attributed",
        ]
    elif intent == Intent.BUSCA_PRECEDENTE:
        payload["query"] = _extract_body_after_command(text)
        payload["so_id"] = so_id

    return payload
