"""Intenções reconhecidas pelo parser de linguagem natural.

Refs: ELO-NATURAL-LANGUAGE-PROTOCOL
"""
from __future__ import annotations

from enum import Enum


class Intent(str, Enum):
    CONFERE_ANALISE = "confere_analise"
    O_QUE_SABE = "o_que_sabe"
    GUARDA_APRENDIZADO = "guarda_aprendizado"
    STATUS_DECISAO = "status_decisao"
    LISTA_ABERTAS = "lista_abertas"
    BUSCA_PRECEDENTE = "busca_precedente"


INTENT_DESCRIPTIONS = {
    Intent.CONFERE_ANALISE: "Confere uma análise contra o que o ELO sabe",
    Intent.O_QUE_SABE: "Retorna o que o ELO sabe sobre uma SO",
    Intent.GUARDA_APRENDIZADO: "Registra aprendizado novo",
    Intent.STATUS_DECISAO: "Consulta o estado de uma decisão",
    Intent.LISTA_ABERTAS: "Lista decisões abertas",
    Intent.BUSCA_PRECEDENTE: "Busca precedentes similares",
}
