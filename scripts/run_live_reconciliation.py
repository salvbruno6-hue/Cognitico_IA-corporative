"""Executor da reconciliação live via CLI.

Roda o harness de reconciliação contra Supabase e imprime
resultado. Read-only.

Uso:
    python scripts/run_live_reconciliation.py

Variáveis de ambiente obrigatórias:
    SUPABASE_URL
    SUPABASE_SERVICE_ROLE_KEY

Refs: ELO_LIVE_STATE_RECONCILIATION_CONTRACT
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()

    if not url or not key:
        print(
            "ERRO: SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY "
            "são obrigatórias.",
            file=sys.stderr,
        )
        return 1

    from elo.infrastructure.live_state_reconciliation import (
        LiveStateReconciliation,
    )
    from elo.infrastructure.supabase_rls_reader import (
        SupabaseRLSStateReader,
    )

    reader = SupabaseRLSStateReader(url, key)
    harness = LiveStateReconciliation()

    try:
        report = harness.reconcile(reader)
    except Exception as exc:
        print(
            f"ERRO na reconciliação: {exc}", file=sys.stderr
        )
        return 2

    output = report.to_dict()
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
