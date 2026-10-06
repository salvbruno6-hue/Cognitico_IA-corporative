"""Runtime access to the canonical Forge infrastructure adapter.

This is only a loading bridge. Source governance remains owned by
elo_aprendizado_fontes and the adapter under elo-virtual-core/integracoes.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_forge_adapter():
    root = Path(__file__).resolve().parents[3]
    path = root / "elo-virtual-core" / "integracoes" / "supabase_elo_forge.py"
    if not path.is_file():
        raise RuntimeError(f"canonical Forge adapter not found: {path}")
    spec = importlib.util.spec_from_file_location("elo_canonical_forge_adapter", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load canonical Forge adapter")
    module: ModuleType = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.SupabaseEloForge()
