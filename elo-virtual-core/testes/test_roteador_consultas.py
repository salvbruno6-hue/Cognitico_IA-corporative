import pytest

from regras.roteador_consultas import route_query


def test_taxonomia_routes_to_supabase():
    result = route_query("Quais são os dados da taxonomia MLT.M02?")
    assert result["source"] == "supabase_elo_forge"
    assert result["must_query_source"] is True
    assert "taxonomia" in result["tables"]
    assert "project_ref" not in result
    assert "project_id" not in result


def test_kit_routes_to_supabase():
    result = route_query("Kit elétrica M01")
    assert result["source"] == "supabase_elo_forge"
    assert "kits" in result["tables"]
    assert "kit_itens" in result["tables"]
    assert "lista_mae" in result["tables"]
    assert "project_ref" not in result
    assert "project_id" not in result


def test_structure_routes_to_supabase():
    result = route_query("Qual é a estrutura modular do M01?")
    assert result["source"] == "supabase_elo_forge"
    assert "estrutura_modular" in result["tables"]
    assert "project_ref" not in result


def test_unrelated_query_uses_local_fallback():
    result = route_query("Simule um cenário matemático sem dados do ELO Forge")
    assert result["source"] == "local"
    assert result["must_query_source"] is False
    assert "project_ref" not in result


def test_empty_query_fails_closed():
    with pytest.raises(ValueError, match="query is required"):
        route_query("   ")
