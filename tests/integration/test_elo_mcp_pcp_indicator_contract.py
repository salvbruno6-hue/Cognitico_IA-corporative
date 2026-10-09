from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MCP_INDEX = ROOT / "supabase" / "functions" / "elo-mcp" / "index.ts"
MCP_README = ROOT / "supabase" / "functions" / "elo-mcp" / "README.md"
MCP_MAP = ROOT / "05-cognitive-platform" / "MCP_CANONICAL_MAP.md"


def test_mcp_exposes_governed_indicator_tool_with_catalog_gate():
    source = MCP_INDEX.read_text(encoding="utf-8")

    assert 'name: "elo_pcp_indicadores_status"' in source
    assert '"v_elo_pcp_carga_capacidade_periodo"' in source
    assert '"v_elo_pcp_indicadores_montagem_externa"' in source
    assert '"mt_definicoes_kpi"' in source
    assert '"mt_snapshots_kpi"' in source
    assert '.from("elo_aprendizado_fontes")' in source
    assert 'state: "BLOQUEADO_CATALOGO"' in source
    assert 'automatic_kpi_promotion: false' in source
    assert 'formalKpiState' in source
    assert '"SEM_KPI_FORMAL_REGISTRADO"' in source
    assert '"KPI_FORMAL_REGISTRADO"' in source


def test_mcp_indicator_tool_is_documented_in_runtime_and_canonical_map():
    readme = MCP_README.read_text(encoding="utf-8")
    canonical_map = MCP_MAP.read_text(encoding="utf-8")

    assert "`elo_pcp_indicadores_status`" in readme
    assert "`elo_pcp_indicadores_status`" in canonical_map
    assert "BLOQUEADO_CATALOGO" in readme
    assert "automatic_kpi_promotion=false" in readme
    assert "mt_definicoes_kpi" in canonical_map
    assert "mt_snapshots_kpi" in canonical_map
