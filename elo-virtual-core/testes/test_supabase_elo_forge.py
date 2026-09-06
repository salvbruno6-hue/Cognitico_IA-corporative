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
        "item": "item-01",
        "lista": "lista-01",
        "estrutura": "estrutura-01",
        "estrutura_item": "estrutura-item-01",
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
        ("kits", "modelo_id", ids["model"]): [{"id": ids["kit"], "codigo": "KIT-M01"}],
        ("kit_itens", "kit_id", ids["kit"]): [{
            "id": ids["item"],
            "kit_id": ids["kit"],
            "lista_mae_id": ids["lista"],
            "quantidade": 1,
        }],
        ("lista_mae", "id", ids["lista"]): [{
            "id": ids["lista"],
            "cod_item": "MAT-01",
            "descricao_oficial": "Material teste",
        }],
        ("estrutura_modular", "modelo_id", ids["model"]): [{"id": ids["estrutura"], "modelo_id": ids["model"]}],
        ("estrutura_modular_itens", "estrutura_modular_id", ids["estrutura"]): [{
            "id": ids["estrutura_item"],
            "estrutura_modular_id": ids["estrutura"],
            "modelo_id": ids["model"],
        }],
    }

    def fake_read_table(table, *, filters=None, limit=100, order_by=None):
        assert filters and len(filters) == 1
        column, expression = next(iter(filters.items()))
        value = expression.removeprefix("eq.")
        calls.append((table, column, value, limit))
        return rows.get((table, column, value), [])

    monkeypatch.setattr(forge, "read_table", fake_read_table)
    result = forge.model_context("MLT.M01")

    relationships = result["relationships"]
    assert relationships["taxonomia"][0]["codigo"] == "MLT.M01"
    assert relationships["dimensoes"][0]["referencia"] == "20 pés"
    assert relationships["kits"][0]["codigo"] == "KIT-M01"
    assert relationships["kit_itens"][0]["lista_mae_id"] == ids["lista"]
    assert relationships["lista_mae"][0]["cod_item"] == "MAT-01"
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
