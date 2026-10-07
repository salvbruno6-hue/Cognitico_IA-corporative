#!/usr/bin/env python3
"""Renderizador mínimo e seguro da PTS Técnica.

A PTS Técnica organiza o TR antes do orçamento. Não audita orçamento pronto.
"""

import argparse
import json
from pathlib import Path
import re

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).parent
TEMPLATE_NAME = "PTS_TECNICA_TEMPLATE.md.j2"


def carregar_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def resolver_so_do_contexto(dados: dict) -> dict:
    """Consume a SO já atribuída pela autoridade e valida sua identidade.

    Este renderer não atribui, gera, incrementa, reinicia ou corrige SO.
    A autoridade pela atribuição do número é o Analista de Orçamento.
    """
    identificacao = dict(dados.get("identificacao") or {})
    contexto = dict(dados.get("contexto_projeto") or {})

    so = (
        identificacao.get("so_resolvida")
        or contexto.get("so")
        or identificacao.get("so")
    )
    if not so:
        raise ValueError(
            "PTS Técnica exige a SO atribuída pelo Analista de Orçamento."
        )

    so = str(so).strip()
    match = re.fullmatch(r"SO\s+(\d{3})\.(\d{2})", so, re.IGNORECASE)
    if not match:
        raise ValueError(
            "SO inválida. Informe a SO atribuída no formato canônico SO NNN.AA."
        )

    identificacao["so_resolvida"] = f"SO {match.group(1)}.{match.group(2)}"
    dados["identificacao"] = identificacao
    return dados


def render(dados: dict) -> str:
    if not isinstance(dados, dict):
        raise TypeError("PTS Técnica deve ser um objeto JSON.")
    dados = resolver_so_do_contexto(dados)
    ambiente = Environment(
        loader=FileSystemLoader(ROOT),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return ambiente.get_template(TEMPLATE_NAME).render(**dados)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dados", type=Path)
    parser.add_argument("-o", "--out", type=Path)
    args = parser.parse_args()
    markdown = render(carregar_json(args.dados))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
