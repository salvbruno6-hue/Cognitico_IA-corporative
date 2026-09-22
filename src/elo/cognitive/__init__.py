"""Canonical cognitive-core boundary for the ELO prototype.

Lazy import: CognitiveCore só é carregado quando acessado
explicitamente. Isso libera elo.cognitive.runtime de depender
de imports opcionais (hermes, symbiont).
"""
from __future__ import annotations

from typing import Any

__all__ = ["CognitiveCore"]


def __getattr__(name: str) -> Any:
    if name == "CognitiveCore":
        from ._core import CognitiveCore
        return CognitiveCore
    raise AttributeError(f"module 'elo.cognitive' has no attribute '{name}'")
