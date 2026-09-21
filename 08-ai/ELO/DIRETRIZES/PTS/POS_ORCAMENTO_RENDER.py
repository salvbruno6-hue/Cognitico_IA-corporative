#!/usr/bin/env python3
"""Gera uma PTS Pós-Orçamento em Markdown a partir de um JSON.

Uso:
    python POS_ORCAMENTO_RENDER.py POS_ORCAMENTO_TEMPLATE.json
    python POS_ORCAMENTO_RENDER.py SO_XXX.json -o SO_XXX_POS.md
"""

import argparse
import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).parent
TEMPLATE_NAME = "POS_ORCAMENTO_TEMPLATE.md.j2"


def carregar_json(caminho: Path) -> dict:
    with caminho.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)


def render(dados: dict) -> str:
    ambiente = Environment(
        loader=FileSystemLoader(ROOT),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = ambiente.get_template(TEMPLATE_NAME)
    return template.render(**dados)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera PTS Pós-Orçamento em Markdown."
    )
    parser.add_argument(
        "dados",
        type=Path,
        help="Arquivo JSON com os dados da SO.",
    )
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        default=None,
        help="Arquivo Markdown de saída.",
    )
    args = parser.parse_args()

    try:
        if not args.dados.exists():
            raise FileNotFoundError(f"arquivo não encontrado: {args.dados}")

        dados = carregar_json(args.dados)
        markdown = render(dados)

        saida = args.out or args.dados.with_suffix(".md")
        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_text(markdown, encoding="utf-8")

        print(f"[ok] gerado: {saida}")
        return 0
    except Exception as exc:
        print(f"[erro] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
