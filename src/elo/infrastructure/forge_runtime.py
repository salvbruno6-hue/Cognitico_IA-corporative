"""Runtime loader for the canonical Forge adapter.

The adapter remains owned by elo-virtual-core/integracoes. This module only
makes that existing infrastructure adapter reachable from the installed ELO
package; it does not duplicate source governance or create another authority.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any


def load_forge_adapter() -> Any:
    root = Path(__file__).resolve().parents[3]
    adapter_path = root / "elo-virtual-core" / "integracoes" / "supabase_elo_forge.py"
    if not adapter_path.is_file():
        raise RuntimeError(f"canonical Forge adapter not found: {adapter_path}")

    spec = importlib.util.spec_from_file_location("elo_canonical_forge_adapter", adapter_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load canonical Forge adapter")
    module: ModuleType = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.SupabaseEloForge()
