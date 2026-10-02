#!/usr/bin/env python3
"""Integra as camadas da PTS Pós-Orçamento sem criar uma segunda PTS.

Fluxo:
auditoria existente -> competitividade -> validação -> arbitragem explícita
-> pacote consultivo para ELO Aprender.

Este módulo é determinístico e não persiste memória nem altera orçamento.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

KNOWLEDGE = {"FORTE", "MEDIO", "FRACO", "AUSENTE", "CONFLITANTE"}
FLEXIBILITY = {"ALTA", "MEDIA", "BAIXA", "INDETERMINADA"}
RISK = {"BAIXO", "MEDIO", "ALTO", "CRITICO"}
DECISIONS = {
    "MANTER", "REVISAR", "NEGOCIAR", "SUBSTITUIR",
    "REESTRUTURAR", "CONFIRMAR", "NAO_REDUZIR", "AGUARDAR_DECISAO",
}
VALIDATION = {"VALIDADO", "VALIDADO_COM_PENDENCIAS", "NAO_VALIDADO"}
SCENARIOS = {"BASE", "COMPETITIVO", "MAXIMO"}


@dataclass(frozen=True)
class IntegrationResult:
    competitividade: Mapping[str, Any]
    validacao: Mapping[str, Any]
    resultado_arbitrado: Mapping[str, Any]
    elo_aprender: Mapping[str, Any]


def _number(value: Any) -> float:
    if value in (None, "", "—"):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(text)
    except ValueError:
        return 0.0


def _audit_rows(pos: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    rows = pos.get("matriz_principal") or []
    if not isinstance(rows, list):
        raise ValueError("matriz_principal deve ser lista")
    return rows


def calculate_abc(
    rows: Sequence[Mapping[str, Any]],
    *,
    a_limit: float = 0.80,
    b_limit: float = 0.95,
) -> list[dict[str, Any]]:
    """Classifica somente o peso financeiro; não representa criticidade técnica."""
    if not 0 < a_limit < b_limit <= 1:
        raise ValueError("limites ABC inválidos")
    valued = [(row, _number(row.get("valor"))) for row in rows]
    valued.sort(key=lambda pair: pair[1], reverse=True)
    total = sum(value for _, value in valued)
    cumulative = 0.0
    output: list[dict[str, Any]] = []
    for row, value in valued:
        weight = (value / total) if total else 0.0
        cumulative += weight
        abc = "A" if cumulative <= a_limit or (not output and cumulative > a_limit) else (
            "B" if cumulative <= b_limit else "C"
        )
        output.append({
            "item": row.get("n"),
            "ref_tecnica": row.get("ref_tecnica"),
            "ref_orc": row.get("ref_orc"),
            "valor": row.get("valor"),
            "peso": round(weight * 100, 4),
            "peso_acumulado": round(cumulative * 100, 4),
            "abc": abc,
        })
    return output


def build_competitividade(
    pos: Mapping[str, Any],
    *,
    a_limit: float = 0.80,
    b_limit: float = 0.95,
) -> dict[str, Any]:
    """Consome a auditoria; não recria ou corrige seus resultados."""
    audit = _audit_rows(pos)
    abc_rows = calculate_abc(audit, a_limit=a_limit, b_limit=b_limit)
    source = pos.get("competitividade") or {}
    supplied = {
        str(item.get("ref_orc") or item.get("item")): item
        for item in source.get("indicadores", [])
        if isinstance(item, Mapping)
    }

    indicators: list[dict[str, Any]] = []
    for item in abc_rows:
        key = str(item.get("ref_orc") or item.get("item"))
        given = supplied.get(key, {})
        indicators.append({
            **item,
            "conhecimento": given.get("conhecimento", "AUSENTE"),
            "flexibilidade": given.get("flexibilidade", "INDETERMINADA"),
            "risco": given.get("risco", "MEDIO"),
            "decisao": given.get("decisao", "AGUARDAR_DECISAO"),
            "evidencia": given.get("evidencia", "não informada"),
            "oportunidade": given.get("oportunidade", "não informada"),
            "responsavel": given.get("responsavel", "não informado"),
        })

    for row in indicators:
        if row["conhecimento"] not in KNOWLEDGE:
            raise ValueError(f"conhecimento inválido em {row['item']}")
        if row["flexibilidade"] not in FLEXIBILITY:
            raise ValueError(f"flexibilidade inválida em {row['item']}")
        if row["risco"] not in RISK:
            raise ValueError(f"risco inválido em {row['item']}")
        if row["decisao"] not in DECISIONS:
            raise ValueError(f"decisão inválida em {row['item']}")

    classes = []
    for abc in ("A", "B", "C"):
        members = [r for r in indicators if r["abc"] == abc]
        classes.append({
            "classe": abc,
            "criterio": "peso financeiro acumulado",
            "itens": [r["item"] for r in members],
            "peso_acumulado": members[-1]["peso_acumulado"] if members else 0,
            "tratamento": "priorizar análise econômica sem autorizar redução",
        })

    return {
        "natureza": "complementar",
        "indicadores": indicators,
        "curva_abc": classes,
        "oportunidades": source.get("oportunidades", []),
        "cenarios": source.get("cenarios", []),
    }


def validate_integration(
    pos: Mapping[str, Any],
    competitividade: Mapping[str, Any],
) -> dict[str, Any]:
    """Executa o gate estrutural e produz proposta, não arbitragem."""
    required = ("matriz_principal", "divergencias", "riscos", "pendencias", "checklist")
    missing = [key for key in required if key not in pos]
    if missing:
        raise ValueError("camada de validação sem campos: " + ", ".join(missing))

    refs = {str(row.get("ref_orc")) for row in _audit_rows(pos) if row.get("ref_orc")}
    comp_refs = {str(row.get("ref_orc")) for row in competitividade.get("indicadores", []) if row.get("ref_orc")}
    orphan = sorted(comp_refs - refs)
    if orphan:
        raise ValueError("competitividade possui ref_orc órfã: " + ", ".join(orphan))

    checklist = pos.get("checklist") or {}
    pending = len(pos.get("pendencias") or [])
    divergences = len(pos.get("divergencias") or [])
    unresolved = [
        str(value).strip().lower()
        for value in checklist.values()
        if str(value).strip().lower() in {"não", "nao", "pendente", "incompleto"}
    ]

    if unresolved or divergences:
        proposed = "VALIDADO_COM_PENDENCIAS" if not unresolved else "NAO_VALIDADO"
    elif pending:
        proposed = "VALIDADO_COM_PENDENCIAS"
    else:
        proposed = "VALIDADO"

    return {
        "status_proposto": proposed,
        "divergencias": divergences,
        "pendencias": pending,
        "checklist_inconclusivo": len(unresolved),
        "evidencias": [
            "matriz_principal",
            "camada_analitica_competitividade",
            "checklist_de_completude",
        ],
        "requer_arbitragem": True,
    }


def arbitrar(
    proposta: Mapping[str, Any],
    *,
    resultado: str,
    responsavel: str,
    justificativa: str,
) -> dict[str, Any]:
    """Registra a arbitragem explícita; nunca escolhe o resultado sozinho."""
    if resultado not in VALIDATION:
        raise ValueError(f"resultado arbitrado inválido: {resultado}")
    if not responsavel or not justificativa:
        raise ValueError("arbitragem exige responsável e justificativa")
    return {
        "status": resultado,
        "responsavel": responsavel,
        "justificativa": justificativa,
        "status_proposto": proposta.get("status_proposto"),
        "evidencias": list(proposta.get("evidencias", [])),
        "arbitragem_explicita": True,
    }


def build_learning_pack(
    pos: Mapping[str, Any],
    arbitrado: Mapping[str, Any],
) -> dict[str, Any]:
    """Produz evidência candidata; não promove nem persiste aprendizado."""
    return {
        "status": "CANDIDATA",
        "so": pos.get("so"),
        "origem": "PTS Pós-Orçamento",
        "resultado_arbitrado": arbitrado.get("status"),
        "decisoes": [arbitrado.get("justificativa")],
        "evidencias": list(arbitrado.get("evidencias", [])),
        "regras_novas": [],
        "memorias_calculo": [],
        "padroes": [],
        "limitacoes": [
            "não promove conhecimento ao Core",
            "não altera orçamento",
            "requer governança ELO APRENDER",
        ],
    }


def integrate(
    pos: Mapping[str, Any],
    *,
    resultado: str | None = None,
    responsavel: str | None = None,
    justificativa: str | None = None,
    a_limit: float = 0.80,
    b_limit: float = 0.95,
) -> IntegrationResult:
    competitividade = build_competitividade(pos, a_limit=a_limit, b_limit=b_limit)
    validacao = validate_integration(pos, competitividade)
    if not (resultado and responsavel and justificativa):
        arbitrado = {
            "status": "AGUARDANDO_ARBITRAGEM",
            "status_proposto": validacao["status_proposto"],
            "arbitragem_explicita": False,
        }
    else:
        arbitrado = arbitrar(
            validacao,
            resultado=resultado,
            responsavel=responsavel,
            justificativa=justificativa,
        )
    learning = build_learning_pack(pos, arbitrado)
    return IntegrationResult(competitividade, validacao, arbitrado, learning)
