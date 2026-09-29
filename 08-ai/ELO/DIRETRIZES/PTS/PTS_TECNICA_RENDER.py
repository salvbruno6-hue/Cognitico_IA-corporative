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
    """Resolve a SO do projeto ativo sem exigir redigitação pelo orçamentista."""
    identificacao = dict(dados.get("identificacao") or {})
    contexto = dict(dados.get("contexto_projeto") or {})

    if identificacao.get("so_resolvida"):
        identificacao["so_resolvida"] = str(identificacao["so_resolvida"]).strip()
        dados["identificacao"] = identificacao
        return dados

    so = contexto.get("so") or identificacao.get("so")
    numero = contexto.get("numero_so") or identificacao.get("numero_so")
    ano = contexto.get("ano") or identificacao.get("ano")

    if numero is not None and ano is not None:
        digits = re.sub(r"\D", "", str(numero))
        year_digits = re.sub(r"\D", "", str(ano))
        if digits and year_digits:
            identificacao["so_resolvida"] = f"SO {int(digits):04d}.{year_digits[-2:]}"
    elif so:
        match = re.fullmatch(r"SO[\s_-]*(\d{1,4})[\s_.-]*(\d{2,4})", str(so).strip(), re.IGNORECASE)
        if match:
            identificacao["so_resolvida"] = f"SO {int(match.group(1)):04d}.{match.group(2)[-2:]}"
        else:
            identificacao["so_resolvida"] = str(so).strip()
    else:
        raise ValueError("PTS Técnica exige SO resolvida pelo contexto do projeto ativo.")

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
