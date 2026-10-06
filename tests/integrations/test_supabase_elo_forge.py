import importlib.util
import sys
from pathlib import Path


def _load_adapter():
    path = Path(__file__).resolve().parents[2] / "elo-virtual-core" / "integracoes" / "supabase_elo_forge.py"
    spec = importlib.util.spec_from_file_location("test_forge_adapter", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.SupabaseEloForge


def test_source_selection_uses_registry_metadata_without_static_table_allowlist():
    Adapter = _load_adapter()
    adapter = Adapter.__new__(Adapter)
    adapter.discover_sources = lambda: [
        {
            "schema_name": "public",
            "table_name": "modelos",
            "dominio_codigo": "produtos",
            "prioridade": 54,
            "enabled": True,
            "extracao_ativa": True,
            "extraction_mode": "registro_para_experiencia",
            "regra_extracao": {"tipo": "modelo"},
        },
        {
            "schema_name": "public",
            "table_name": "fluxo_produtivo_modular",
            "dominio_codigo": "producao_fluxo_modular",
            "prioridade": 60,
            "enabled": True,
            "extracao_ativa": True,
            "extraction_mode": "registro_para_experiencia",
            "regra_extracao": {"tipo": "fluxo"},
        },
        {
            "schema_name": "public",
            "table_name": "fornecedores",
            "dominio_codigo": "compras",
            "prioridade": 80,
            "enabled": True,
            "extracao_ativa": True,
            "extraction_mode": "registro_para_experiencia",
            "regra_extracao": {"tipo": "fornecedor"},
        },
    ]

    selected = adapter.select_sources(
        "como o M01 entra na produção?",
        entity_code="M01",
    )
    tables = {row["table_name"] for row in selected}
    assert "modelos" in tables
    assert "fluxo_produtivo_modular" in tables
    assert "fornecedores" not in tables


def test_disabled_source_is_never_selected():
    Adapter = _load_adapter()
    adapter = Adapter.__new__(Adapter)
    adapter.discover_sources = lambda: [
        {
            "schema_name": "public",
            "table_name": "fornecedores",
            "dominio_codigo": "compras",
            "prioridade": 80,
            "enabled": False,
            "extracao_ativa": True,
            "extraction_mode": "registro_para_experiencia",
            "regra_extracao": {"tipo": "fornecedor"},
        }
    ]
    assert adapter.select_sources("fornecedor M01", entity_code="M01") == []
