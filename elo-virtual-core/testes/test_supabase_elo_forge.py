from integracoes.supabase_elo_forge import ForgeConfig, ForgeRetrievalError, SupabaseEloForge


def test_mlt_alias_resolves_to_canonical_model():
    assert SupabaseEloForge.canonical_model_code("MLT.M01") == "M01"
    assert SupabaseEloForge.canonical_model_code("m01") == "M01"


def test_unknown_alias_is_not_guessed():
    assert SupabaseEloForge.canonical_model_code("MLT.M999") == "MLT.M999"


def test_config_requires_server_side_credentials(monkeypatch):
    monkeypatch.delenv("ELO_FORGE_SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("ELO_FORGE_SUPABASE_SERVICE_ROLE_KEY", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    try:
        ForgeConfig.from_environment()
    except ForgeRetrievalError as exc:
        assert "credentials" in str(exc)
    else:
        raise AssertionError("missing credentials must fail closed")


def test_read_table_rejects_non_allowlisted_table():
    forge = object.__new__(SupabaseEloForge)
    forge.config = ForgeConfig("https://example.supabase.co", "test")
    try:
        forge.read_table("users")
    except ForgeRetrievalError as exc:
        assert "table_not_allowed" in str(exc)
    else:
        raise AssertionError("non-allowlisted table must be rejected")


def test_router_contract_points_to_relationship_aware_adapter():
    from regras.roteador_consultas import route_query

    result = route_query("Qual é a composição do MLT.M01?")
    assert result["source"] == "supabase_elo_forge"
    assert result["adapter"] == "integracoes.supabase_elo_forge"
    assert result["retrieval_contract"] == "read_only_relationship_aware"
    assert result["must_query_source"] is True


def test_model_context_traverses_full_relationship_chain_with_bounded_calls(monkeypatch):
    forge = object.__new__(SupabaseEloForge)
    forge.config = ForgeConfig("https://example.supabase.co", "test")
    forge.timeout = 15.0

    ids = {
        "model": "model-01",
        "taxonomia": "tax-01",
        "dimensao": "dim-01",
        "kit": "kit-01",
        "kit2": "kit-02",
        "item": "item-01",
        "item2": "item-02",
        "lista": "lista-01",
        "lista2": "lista-02",
        "estrutura": "estrutura-01",
        "estrutura2": "estrutura-02",
        "estrutura_item": "estrutura-item-01",
        "estrutura_item2": "estrutura-item-02",
    }
    calls = []

    rows = {
        ("modelos", "codigo", "M01"): [{
            "id": ids["model"],
            "codigo": "M01",
            "taxonomia_id": ids["taxonomia"],
            "dimensao_id": ids["dimensao"],
        }],
        ("taxonomia", "id", ids["taxonomia"]): [{"id": ids["taxonomia"], "codigo": "MLT.M01"}],
        ("dimensoes", "id", ids["dimensao"]): [{"id": ids["dimensao"], "referencia": "20 pés"}],
        ("kits", "modelo_id", ids["model"]): [
            {"id": ids["kit"], "codigo": "KIT-M01"},
            {"id": ids["kit2"], "codigo": "KIT-M01-2"},
        ],
        ("kit_itens", "kit_id", ids["kit"]): [{
            "id": ids["item"],
            "kit_id": ids["kit"],
            "lista_mae_id": ids["lista"],
            "quantidade": 1,
        }],
        ("kit_itens", "kit_id", ids["kit2"]): [{
            "id": ids["item2"],
            "kit_id": ids["kit2"],
            "lista_mae_id": ids["lista2"],
            "quantidade": 2,
        }],
        ("lista_mae", "id", ids["lista"]): [{
            "id": ids["lista"],
            "cod_item": "MAT-01",
            "descricao_oficial": "Material teste",
        }],
        ("lista_mae", "id", ids["lista2"]): [{
            "id": ids["lista2"],
            "cod_item": "MAT-02",
            "descricao_oficial": "Material teste 2",
        }],
        ("estrutura_modular", "modelo_id", ids["model"]): [
            {"id": ids["estrutura"], "modelo_id": ids["model"]},
            {"id": ids["estrutura2"], "modelo_id": ids["model"]},
        ],
        ("estrutura_modular_itens", "estrutura_modular_id", ids["estrutura"]): [{
            "id": ids["estrutura_item"],
            "estrutura_modular_id": ids["estrutura"],
            "modelo_id": ids["model"],
        }],
        ("estrutura_modular_itens", "estrutura_modular_id", ids["estrutura2"]): [{
            "id": ids["estrutura_item2"],
            "estrutura_modular_id": ids["estrutura2"],
            "modelo_id": ids["model"],
        }],
    }

    def fake_read_table(table, *, filters=None, limit=100, order_by=None):
        assert filters and len(filters) == 1
        column, expression = next(iter(filters.items()))
        if expression.startswith("eq."):
            values = {expression.removeprefix("eq.")}
        elif expression.startswith("in.(") and expression.endswith(")"):
            values = set(expression[4:-1].split(","))
        else:
            raise AssertionError(f"unexpected filter expression: {expression}")
        calls.append((table, column, expression, limit))
        result = []
        for (row_table, row_column, row_value), table_rows in rows.items():
            if row_table == table and row_column == column and row_value in values:
                result.extend(table_rows)
        return result

    monkeypatch.setattr(forge, "read_table", fake_read_table)
    result = forge.model_context("MLT.M01")

    relationships = result["relationships"]
    assert relationships["taxonomia"][0]["codigo"] == "MLT.M01"
    assert relationships["dimensoes"][0]["referencia"] == "20 pés"
    assert relationships["kits"][0]["codigo"] == "KIT-M01"
    assert {item["id"] for item in relationships["kit_itens"]} == {ids["item"], ids["item2"]}
    assert {item["cod_item"] for item in relationships["lista_mae"]} == {"MAT-01", "MAT-02"}
    assert {item["codigo_item"] for item in result["kit_composition"]} == {None}

    assert relationships["estrutura_modular"][0]["id"] == ids["estrutura"]
    assert relationships["estrutura_modular_itens"][0]["id"] == ids["estrutura_item"]
    assert result["source"] == "supabase_elo_forge"
    assert result["provenance"]["read_only"] is True
    assert result["provenance"]["guessed"] is False
    assert result["entity"]["requested_reference"] == "MLT.M01"
    assert result["entity"]["canonical_code"] == "M01"
    assert len(calls) <= 8


def test_model_context_fails_closed_on_non_unique_identity(monkeypatch):
    forge = object.__new__(SupabaseEloForge)
    forge.config = ForgeConfig("https://example.supabase.co", "test")
    monkeypatch.setattr(
        forge,
        "read_table",
        lambda table, **kwargs: [{"id": "1", "codigo": "M01"}, {"id": "2", "codigo": "M01"}],
    )
    try:
        forge.resolve_model("MLT.M01")
    except ForgeRetrievalError as exc:
        assert "not_unique" in str(exc)
    else:
        raise AssertionError("duplicate model identity must fail closed")



def test_governed_source_registry_is_the_only_expansion_path(monkeypatch):
    forge = object.__new__(SupabaseEloForge)
    forge.config = ForgeConfig("https://example.supabase.co", "test")
    calls = []

    def fake_read_table(table, *, filters=None, limit=100, order_by=None):
        calls.append((table, filters))
        if table == "elo_aprendizado_fontes":
            return [
                {
                    "schema_name": "public",
                    "table_name": "fornecedores",
                    "enabled": True,
                    "extracao_ativa": True,
                    "dominio_codigo": "compras",
                }
            ]
        if table == "fornecedores":
            return [{"id": "f-1", "nome": "Fornecedor teste"}]
        raise AssertionError(f"unexpected table: {table}")

    monkeypatch.setattr(forge, "read_table", fake_read_table)

    sources = forge.governed_sources(domain="compras")
    assert sources[0]["table_name"] == "fornecedores"
    assert forge.read_governed_source("fornecedores")[0]["nome"] == "Fornecedor teste"
    assert calls[0][0] == "elo_aprendizado_fontes"
    assert calls[1][0] == "elo_aprendizado_fontes"
    assert calls[2][0] == "fornecedores"


def test_governed_source_rejects_registered_but_disabled_table(monkeypatch):
    forge = object.__new__(SupabaseEloForge)
    forge.config = ForgeConfig("https://example.supabase.co", "test")

    monkeypatch.setattr(
        forge,
        "read_table",
        lambda table, **kwargs: (
            [{
                "schema_name": "public",
                "table_name": "fornecedores",
                "enabled": False,
                "extracao_ativa": False,
            }]
            if table == "elo_aprendizado_fontes"
            else []
        ),
    )

    try:
        forge.read_governed_source("fornecedores")
    except ForgeRetrievalError as exc:
        assert "source_not_governed" in str(exc)
    else:
        raise AssertionError("disabled source must fail closed")


def test_arbitrary_table_remains_rejected_even_with_governed_reader():
    forge = object.__new__(SupabaseEloForge)
    forge.config = ForgeConfig("https://example.supabase.co", "test")
    forge.governed_sources = lambda **kwargs: ()

    try:
        forge.read_governed_source("users")
    except ForgeRetrievalError as exc:
        assert "source_not_governed" in str(exc)
    else:
        raise AssertionError("arbitrary table must remain forbidden")
