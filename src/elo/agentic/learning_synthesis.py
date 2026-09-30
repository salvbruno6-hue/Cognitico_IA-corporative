"""Governed synthesis from a concrete learning experience to a reusable decision pattern.

This module performs synthesis, not promotion. A source experience remains
evidence; the returned candidate is a structured, consultative pattern that
must still pass the canonical learning gate before becoming governed knowledge.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class DecisionPatternCandidate:
    """A reusable decision pattern synthesized from one or more experiences."""

    nome: str
    gatilhos: tuple[str, ...]
    pre_requisitos: tuple[str, ...]
    sequencia: tuple[str, ...]
    regras_decisao: tuple[str, ...]
    heuristicas: tuple[str, ...]
    limitacoes: tuple[str, ...]
    evidencias: tuple[str, ...]
    status: str = "CANDIDATO"
    origem_experiencias: tuple[str, ...] = ()

    def as_row(self) -> Mapping[str, Any]:
        """Shape compatible with elo_aprendizado_padroes_raciocinio."""
        return {
            "nome": self.nome,
            "gatilhos": list(self.gatilhos),
            "pre_requisitos": list(self.pre_requisitos),
            "sequencia": list(self.sequencia),
            "regras_decisao": list(self.regras_decisao),
            "heuristicas": list(self.heuristicas),
            "limitacoes": list(self.limitacoes),
            "evidencias": list(self.evidencias),
            "status": self.status,
            "origem_experiencias": list(self.origem_experiencias),
        }


def synthesize_decision_pattern(
    experience: Mapping[str, Any],
    *,
    experience_id: str | None = None,
) -> DecisionPatternCandidate:
    """Extract a reusable decision pattern without copying the source decision."""

    decisions = _as_strings(experience.get("decisoes") or experience.get("decisions"))
    verifications = _as_strings(experience.get("verificacoes") or experience.get("verification"))
    result = _as_strings(experience.get("resultado") or experience.get("result"))
    context = _first_text(experience, "contexto", "context", "objetivo", "objective")
    dependencies = _as_strings(experience.get("dependencias") or experience.get("dependencies"))
    errors = _as_strings(experience.get("erros") or experience.get("errors"))
    corrections = _as_strings(experience.get("correcoes") or experience.get("corrections"))

    if not decisions:
        raise ValueError("learning experience requires at least one decision")
    if not verifications and not result:
        raise ValueError("decision pattern requires verification or result evidence")

    arbitration_absent = _contains_any(
        [context, *decisions],
        (
            "sem arbitragem",
            "sem retorno",
            "ausência de arbitragem",
            "não houve retorno",
            "cliente não respondeu",
            "sem resposta do cliente",
        ),
    )

    if arbitration_absent:
        gatilhos = (
            "há uma dúvida/requisito sem arbitragem externa suficiente",
            "existe evidência técnica, documental ou de composição interna para sustentar uma premissa",
        )
        regra_principal = (
            "Quando faltar arbitragem, recuperar orientação interna aplicável, "
            "verificar equivalência com a SO atual e somente então propor uma premissa "
            "explicitamente limitada ao que a evidência sustenta."
        )
        heuristicas = (
            "histórico é orientação consultiva, não autorização automática",
            "não preencher lacunas com escopo, quantidade ou especificação sem evidência",
            "registrar a decisão atual separadamente da referência histórica",
        )
        limitacoes = (
            "não aplicar se o contexto técnico ou comercial não for equivalente",
            "não transformar uma decisão de uma única SO em regra universal",
            "não assumir escopo externo além do limite comprovado pela evidência atual",
        )
    else:
        gatilhos = (
            "existe uma decisão recorrente associada a uma condição identificável",
            "a decisão possui evidência e verificação suficientes para formular uma orientação condicional",
        )
        regra_principal = (
            "Generalizar a relação condição → critério → decisão somente no nível "
            "explicitamente sustentado pelas evidências da experiência."
        )
        heuristicas = (
            "preservar a condição que disparou a decisão",
            "separar orientação reutilizável da solução específica da SO de origem",
        )
        limitacoes = (
            "não extrapolar além das condições comprovadas",
            "não aplicar automaticamente sem validação da SO atual",
        )

    sequence = (
        "identificar o gatilho e a dúvida atual",
        "consultar evidências e orientações previamente aprendidas",
        "verificar equivalência e aplicabilidade ao contexto atual",
        "formular orientação condicional, preservando limites",
        "submeter a orientação à decisão do analista",
        "registrar o resultado para futura validação do padrão",
    )
    prerequisites = tuple(dict.fromkeys((*dependencies, "evidência suficiente para sustentar a decisão")))
    evidence = tuple(
        dict.fromkeys(
            [
                *verifications,
                *result,
                *corrections,
                *(f"origem_experiencia:{experience_id}",) if experience_id else (),
            ]
        )
    )
    if errors:
        limitacoes = tuple(
            dict.fromkeys(
                (*limitacoes, "preservar erros observados como evidência para revisão do padrão")
            )
        )

    return DecisionPatternCandidate(
        nome="Orientação por padrão de decisão diante de arbitragem ausente ou insuficiente",
        gatilhos=gatilhos,
        pre_requisitos=prerequisites,
        sequencia=sequence,
        regras_decisao=(regra_principal,),
        heuristicas=heuristicas,
        limitacoes=limitacoes,
        evidencias=evidence,
        status="CANDIDATO",
        origem_experiencias=(experience_id,) if experience_id else (),
    )


def _as_strings(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    if isinstance(value, Mapping):
        return tuple(str(v).strip() for v in value.values() if str(v).strip())
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return tuple(str(item).strip() for item in value if str(item).strip())
    return (str(value).strip(),) if str(value).strip() else ()


def _first_text(experience: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        value = experience.get(key)
        if value not in (None, ""):
            return str(value)
    return ""


def _contains_any(values: Sequence[str], needles: Sequence[str]) -> bool:
    haystack = " ".join(values).casefold()
    return any(needle.casefold() in haystack for needle in needles)


__all__ = ["DecisionPatternCandidate", "synthesize_decision_pattern"]
