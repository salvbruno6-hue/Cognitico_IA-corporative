import pytest

from regras.roteador_consultas import route_query
from integracoes.supabase_elo_forge import SupabaseEloForge


def test_taxonomia_routes_to_supabase():
    result = route_query("Quais são os dados da taxonomia MLT.M02?")
    assert result["source"] == "supabase_elo_forge"
    assert result["layer"] == "forge"
    assert result["architectural_parent"] == "ELO Cognitivo"
    assert result["must_query_source"] is True
    assert "taxonomia" in result["tables"]
    assert "elo_orcamento_associacoes" in result["tables"]
    assert "elo_orcamento_decisoes" in result["tables"]
    assert "project_ref" not in result
    assert "project_id" not in result


def test_kit_routes_to_supabase():
    result = route_query("Kit elétrica M01")
    assert result["source"] == "supabase_elo_forge"
    assert result["layer"] == "forge"
    assert "kits" in result["tables"]
    assert "kit_itens" in result["tables"]
    assert "lista_mae" in result["tables"]
    assert "project_ref" not in result
    assert "project_id" not in result


def test_structure_routes_to_supabase():
    result = route_query("Qual é a estrutura modular do M01?")
    assert result["source"] == "supabase_elo_forge"
    assert result["layer"] == "forge"
    assert "estrutura_modular" in result["tables"]
    assert "project_ref" not in result


def test_budget_governance_routes_to_supabase():
    result = route_query("Consultar decisão arbitrada e associação de orçamento")
    assert result["source"] == "supabase_elo_forge"
    assert result["layer"] == "forge"
    assert "elo_orcamento_associacoes" in result["tables"]
    assert "elo_orcamento_decisoes" in result["tables"]
    assert result["retrieval_contract"] == "read_only_relationship_aware"


def test_unrelated_query_uses_local_fallback():
    result = route_query("Simule um cenário matemático sem dados do ELO Forge")
    assert result["source"] == "local"
    assert result["must_query_source"] is False
    assert "project_ref" not in result


def test_empty_query_fails_closed():
    with pytest.raises(ValueError, match="query is required"):
        route_query("   ")


def test_kit_presentation_contains_required_columns_and_values():
    presented = SupabaseEloForge.present_kit_item(
        {
            "cod_item": "ELE024",
            "cod_produt": None,
            "descricao_oficial": "descrição do kit",
            "un": "PÇ",
            "quantidade": 1,
            "valor_unitario": 999,
            "valor_total": 999,
            "lista_mae_id": "lm-1",
        },
        {
            "cod_produt": "3300300024",
            "descricao_oficial": "Barramento bifásico 80A 440V",
            "un": "PÇ",
            "valor_unitario": "10.28",
        },
    )
    assert presented["codigo_item"] == "ELE024"
    assert presented["cod_produto"] == "3300300024"
    assert presented["descricao"] == "Barramento bifásico 80A 440V"
    assert presented["un"] == "PÇ"
    assert presented["qtd"] == 1
    assert presented["valor_unitario"] == "10.28"
    assert presented["valor_total"] == 999


def test_missing_product_code_is_preserved_as_null():
    presented = SupabaseEloForge.present_kit_item(
        {
            "cod_item": "ELE085",
            "cod_produt": None,
            "descricao_oficial": "Disjuntor monopolar 16A",
            "un": "un",
            "quantidade": 1,
            "valor_total": 8.44,
        },
        {
            "cod_produt": None,
            "descricao_oficial": "Disjuntor monopolar 16A",
            "un": "un",
            "valor_unitario": "8.44",
        },
    )
    assert presented["codigo_item"] == "ELE085"
    assert presented["cod_produto"] is None
    assert presented["descricao"] == "Disjuntor monopolar 16A"
    assert presented["un"] == "un"
    assert presented["qtd"] == 1
    assert presented["valor_unitario"] == "8.44"
    assert presented["valor_total"] == 8.44
