"""Thin, read-only entrypoint for the canonical ELO live reconciler.

Implementation and status policy live in elo.infrastructure.live_state_reconciliation.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from elo.infrastructure.live_state_reconciliation import run_reconciliation_cli as main

if __name__ == "__main__":
    sys.exit(main())
