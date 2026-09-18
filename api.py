"""Vercel deployment adapter for the ELO Cognitive FastAPI application."""

from pathlib import Path
import sys


_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from elo.interface.api import app  # noqa: E402


__all__ = ["app"]
