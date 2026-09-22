"""Protocolo e helpers comuns aos handlers do CRL."""
from __future__ import annotations
from typing import Any
from ..crl import CRLContext

def require(ctx: CRLContext, key: str) -> Any:
    if key not in ctx.stage_results and key not in ctx.payload:
        raise ValueError(f"CRL: campo obrigatório ausente: {key}")
    return ctx.payload.get(key) or ctx.stage_results.get(key)
