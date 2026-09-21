#!/usr/bin/env python3
"""Renderizador mínimo e seguro da PTS Técnica.

A PTS Técnica organiza o TR antes do orçamento. Não audita orçamento pronto.
"""

import argparse
import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).parent
TEMPLATE_NAME = "PTS_TECNICA_TEMPLATE.md.j2"


def carregar_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def render(dados: dict) -> str:
    if not isinstance(dados, dict):
        raise TypeError("PTS Técnica deve ser um objeto JSON.")
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
