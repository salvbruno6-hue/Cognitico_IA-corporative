#!/usr/bin/env python3
"""Renderizador da PTS Pós-Orçamento.

Fluxo padrão:
    JSON da SO → fronteira documental → template canônico → apresentação em tela.

Uso:
    python POS_ORCAMENTO_RENDER.py data/SO_XXX.json
    python POS_ORCAMENTO_RENDER.py data/SO_XXX.json -o out/SO_XXX.md

A estrutura da PTS é canônica e versionada, mas não congelada. Evoluções devem
alterar o owner canônico desta pasta e manter schema, modelo, template,
documentação e testes sincronizados.
"""

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).parent
TEMPLATE_NAME = "POS_ORCAMENTO_TEMPLATE.md.j2"
ESTRUTURA_VERSION = "3.0"

REQUIRED_DATA_FIELDS = (
    "schema_version",
    "so",
    "cliente",
    "objeto",
    "revisao",
    "documentos",
    "matriz_principal",
    "blocos_quantitativos",
    "conferencia_valores",
    "auditoria_reversa",
    "itens_premissa",
    "logistica",
    "mao_de_obra",
    "exclusoes",
    "divergencias",
    "riscos",
    "pendencias",
    "itens_nao_orcados",
    "checklist",
    "conclusao",
)

SOURCE_SO_FIELDS = ("origem_so", "referencia_so", "so_origem", "so_referencia")
FALSE_DOCUMENT_FLAGS = ("document_safe", "documento_seguro", "aplicado_na_so_atual")
HISTORICAL_SOURCE_TYPES = {
    "historico",
    "historical",
    "precedente",
    "caso",
    "acervo",
    "referencia_consultiva",
    "consultiva",
}


def carregar_json(caminho: Path) -> dict:
    """Carrega os dados JSON da solicitação."""
    with caminho.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)


def validar_estrutura(dados: dict) -> None:
    """Impede que uma SO use uma estrutura parcial ou variante do template."""
    faltantes = [campo for campo in REQUIRED_DATA_FIELDS if campo not in dados]
    if faltantes:
        raise ValueError(
            "estrutura de dados incompleta; campos ausentes: "
            + ", ".join(faltantes)
        )

    if not str(dados.get("schema_version", "")).strip():
        raise ValueError("campo 'schema_version' é obrigatório.")

    if not dados.get("so"):
        raise ValueError("campo 'so' é obrigatório para aplicar a fronteira documental.")


def _normalizar_so(valor: Any) -> str:
    if valor is None:
        return ""
    return " ".join(str(valor).strip().upper().split())


def _eh_so_atual(item: Any, so_atual: str) -> bool:
    if not isinstance(item, dict):
        return True

    so = _normalizar_so(so_atual)

    for field in FALSE_DOCUMENT_FLAGS:
        if field in item and item[field] is False:
            return False

    for field in SOURCE_SO_FIELDS:
        if field in item and item[field] not in (None, ""):
            origem = _normalizar_so(item[field])
            if origem and origem != so:
                return False

    tipo = str(item.get("fonte_tipo", item.get("tipo_fonte", ""))).strip().lower()
    if tipo in HISTORICAL_SOURCE_TYPES and item.get("aplicado_na_so_atual") is not True:
        return False

    return True


def _filtrar_registro(item: Any, so_atual: str) -> Any:
    if isinstance(item, list):
        resultado = []
        for valor in item:
            filtrado = _filtrar_registro(valor, so_atual)
            if filtrado is not None:
                resultado.append(filtrado)
        return resultado

    if isinstance(item, dict):
        if not _eh_so_atual(item, so_atual):
            return None

        resultado = {}
        for chave, valor in item.items():
            if chave in {"fontes_consultivas", "acervo_historico", "historico_consultivo"}:
                continue
            filtrado = _filtrar_registro(valor, so_atual)
            if filtrado is not None:
                resultado[chave] = filtrado
        return resultado

    return item


def preparar_documento(dados: dict) -> dict:
    """Aplica a fronteira documental antes da apresentação."""
    if not isinstance(dados, dict):
        raise TypeError("os dados da PTS Pós devem ser um objeto JSON.")

    validar_estrutura(dados)

    documento = copy.deepcopy(dados)
    so_atual = documento["so"]

    for chave in ("fontes_consultivas", "acervo_historico", "historico_consultivo"):
        documento.pop(chave, None)

    filtrado = _filtrar_registro(documento, str(so_atual))
    if not isinstance(filtrado, dict):
        raise ValueError("os dados fornecidos não são seguros para gerar a PTS Pós.")

    return filtrado


def render(dados: dict) -> str:
    """Renderiza a PTS usando exclusivamente o template canônico."""
    dados_documentais = preparar_documento(dados)
    ambiente = Environment(
        loader=FileSystemLoader(ROOT),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = ambiente.get_template(TEMPLATE_NAME)
    return template.render(**dados_documentais)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Renderiza PTS Pós-Orçamento; por padrão, apresenta em tela e "
            "não cria arquivo."
        )
    )
    parser.add_argument("dados", type=Path, help="Arquivo JSON com os dados da SO.")
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        default=None,
        help="Persistir Markdown somente quando explicitamente solicitado.",
    )
    args = parser.parse_args()

    try:
        if not args.dados.exists():
            raise FileNotFoundError(f"arquivo não encontrado: {args.dados}")

        dados = carregar_json(args.dados)
        markdown = render(dados)

        if args.out is not None:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(markdown, encoding="utf-8")
            print(f"[ok] arquivo solicitado: {args.out}", file=sys.stderr)
        else:
            print(markdown)
        return 0
    except Exception as exc:
        print(f"[erro] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
