"""Fronteira única de execução da PTS Pós-Orçamento.

Toda nova emissão de PTS Pós deve atravessar este adapter e o owner canônico em
08-ai/ELO/DIRETRIZES/PTS. A interface somente transporta o documento e devolve
o resultado do renderer; não arbitra, persiste, promove aprendizado nem cria
autoridade paralela.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[3]
_PTS_ROOT = _REPO_ROOT / "08-ai" / "ELO" / "DIRETRIZES" / "PTS"
_CANONICAL_RENDERER = _PTS_ROOT / "POS_ORCAMENTO_RENDER.py"
_CANONICAL_TEMPLATE = _PTS_ROOT / "POS_ORCAMENTO_TEMPLATE.md.j2"
_CANONICAL_SCHEMA = _PTS_ROOT / "POS_ORCAMENTO_SCHEMA.json"


def _assert_canonical_owner() -> None:
    """Falha fechada se o contrato canônico não estiver disponível."""
    missing = [
        str(path.relative_to(_REPO_ROOT))
        for path in (_CANONICAL_RENDERER, _CANONICAL_TEMPLATE, _CANONICAL_SCHEMA)
        if not path.is_file()
    ]
    if missing:
        raise RuntimeError(
            "PTS Pós bloqueada: owner canônico incompleto. Ausentes: "
            + ", ".join(missing)
        )


_assert_canonical_owner()
if str(_PTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_PTS_ROOT))

# Import deliberadamente único: nenhuma implementação alternativa é aceita.
from POS_ORCAMENTO_RENDER import preparar_documento, render_prepared  # noqa: E402


def render_pts_pos(dados: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Renderiza exclusivamente pelo owner canônico; falhas bloqueiam a emissão."""
    _assert_canonical_owner()
    preparado = preparar_documento(dados)
    markdown = render_prepared(preparado)
    integracao = preparado.get("integracao")
    if not isinstance(integracao, dict):
        raise RuntimeError("PTS Pós sem integração canônica no documento preparado.")
    return markdown, integracao
