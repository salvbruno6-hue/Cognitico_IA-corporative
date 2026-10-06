import importlib.util
import sys
from pathlib import Path


def _adapter():
    path = Path(__file__).resolve().parents[2] / "elo-virtual-core" / "integracoes" / "supabase_elo_forge.py"
    spec = importlib.util.spec_from_file_location("test_dynamic_forge_adapter", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.SupabaseEloForge


def test_selection_is_derived_from_registry_metadata():
    Adapter = _adapter()
    adapter = Adapter.__new__(Adapter)
    adapter.governed_sources = lambda: [
        {
            "table_name": "elo_sim_demanda",
            "dominio_codigo": "planejamento_demanda",
            "prioridade": 71,
            "regra_extracao": {"tipo": "demanda"},
        },
        {
            "table_name": "elo_sim_demanda_recursos",
            "dominio_codigo": "planejamento_pcp",
            "prioridade": 73,
            "regra_extracao": {"tipo": "demanda_recurso"},
        },
        {
            "table_name": "fornecedores",
            "dominio_codigo": "compras",
            "prioridade": 80,
            "regra_extracao": {"tipo": "fornecedor"},
        },
    ]

    selected = adapter.discover_sources("demanda de recursos")
    tables = [row["table_name"] for row in selected]

    assert "elo_sim_demanda_recursos" in tables
    assert "elo_sim_demanda" in tables
    assert "fornecedores" not in tables
