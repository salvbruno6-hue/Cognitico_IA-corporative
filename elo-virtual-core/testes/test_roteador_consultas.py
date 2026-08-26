from regras.roteador_consultas import route_query


def test_taxonomia_routes_to_supabase():
    result = route_query("Quais são os dados da taxonomia MLT.M02?")
    assert result["source"] == "supabase_elo_forge"
    assert result["must_query_source"] is True
    assert "taxonomia" in result["tables"]


def test_kit_routes_to_supabase():
    result = route_query("Consulte os itens do kit M01")
    assert result["source"] == "supabase_elo_forge"
    assert "kits" in result["tables"]
    assert "kit_itens" in result["tables"]


def test_structure_routes_to_supabase():
    result = route_query("Qual é a estrutura modular do M01?")
    assert result["source"] == "supabase_elo_forge"
    assert "estrutura_modular" in result["tables"]


def test_unrelated_query_uses_local_fallback():
    result = route_query("Simule um cenário matemático sem dados do ELO Forge")
    assert result["source"] == "local"
    assert result["must_query_source"] is False
