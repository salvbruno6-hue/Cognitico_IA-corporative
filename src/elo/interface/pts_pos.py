"""Adapter da Interface para o owner canônico da PTS Pós-Orçamento.

A interface somente transporta o documento e devolve o resultado do renderer.
Não arbitra, persiste, promove aprendizado nem cria uma autoridade paralela.
"""
from __future__ import annotations
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[3]
_PTS_ROOT = _REPO_ROOT / "08-ai" / "ELO" / "DIRETRIZES" / "PTS"
if str(_PTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_PTS_ROOT))
from POS_ORCAMENTO_RENDER import preparar_documento, render_prepared  # noqa: E402

def render_pts_pos(dados: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    preparado = preparar_documento(dados)
    markdown = render_prepared(preparado)
    integracao = preparado.get("integracao")
    if not isinstance(integracao, dict):
        raise RuntimeError("PTS Pós sem integração canônica no documento preparado.")
    return markdown, integracao
