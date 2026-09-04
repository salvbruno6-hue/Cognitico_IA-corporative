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
