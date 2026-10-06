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


def test_read_table_rejects_non_allowlisted_table(monkeypatch):
    forge = object.__new__(SupabaseEloForge)
    forge.config = ForgeConfig("https://example.supabase.co", "test")
    monkeypatch.setattr(forge, "governed_sources", lambda: [])
    try:
        forge.read_table("users")
    except ForgeRetrievalError as exc:
        assert "table_not_governed" in str(exc)
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


def test_governed_source_catalog_controls_table_access(monkeypatch):
    forge = object.__new__(SupabaseEloForge)
    forge.config = ForgeConfig("https://example.supabase.co", "test")
    forge.timeout = 15.0
    monkeypatch.setattr(
        forge,
        "governed_sources",
        lambda: [{"schema_name": "public", "table_name": "fornecedores", "enabled": True, "extracao_ativa": True}],
    )
    assert forge._is_governed_table("fornecedores") is True
    assert forge._is_governed_table("users") is False


def test_discovery_uses_catalog_domains_not_static_table_allow_list():
    forge = object.__new__(SupabaseEloForge)
    monkeypatch_sources = [
        {"schema_name": "public", "table_name": "fluxo_produtivo_modular", "dominio_codigo": "producao_fluxo_modular", "prioridade": 60, "enabled": True, "extracao_ativa": True},
        {"schema_name": "public", "table_name": "fornecedores", "dominio_codigo": "compras", "prioridade": 80, "enabled": True, "extracao_ativa": True},
    ]
    forge.governed_sources = lambda: monkeypatch_sources
    found = forge.discover_sources("O que temos para produção do M01 e quais fornecedores podem ser consultados?")
    names = [item["table_name"] for item in found]
    assert "fluxo_produtivo_modular" in names
    assert "fornecedores" in names


def test_governed_model_context_preserves_family_wide_modular_flow_boundary(monkeypatch):
    forge = object.__new__(SupabaseEloForge)
    context = {
        "source": "supabase_elo_forge",
        "entity": {"requested_reference": "M01", "canonical_code": "M01", "model_id": "model-01"},
        "model": {"id": "model-01", "codigo": "M01", "nome": "Habitacional Amplo 20 pés", "ativo": True},
        "relationships": {
            "taxonomia": [{"id": "tax-01", "codigo": "MLT.M01"}],
            "dimensoes": [{"id": "dim-01", "referencia": "20 pés"}],
            "kits": [{"id": "kit-01"}],
            "kit_itens": [{"id": "item-01", "lista_mae_id": "lista-01", "cod_item": "MAT-01"}],
            "lista_mae": [{"id": "lista-01", "cod_item": "MAT-01"}],
            "estrutura_modular": [],
            "estrutura_modular_itens": [],
        },
        "provenance": {"read_only": True, "guessed": False},
    }
    forge.model_context = lambda reference: context
    forge.governed_sources = lambda: [
        {"schema_name": "public", "table_name": "fluxo_produtivo_modular", "dominio_codigo": "producao_fluxo_modular", "prioridade": 60, "enabled": True, "extracao_ativa": True},
        {"schema_name": "public", "table_name": "fluxo_produtivo_modular_etapas", "dominio_codigo": "producao_fluxo_modular", "prioridade": 61, "enabled": True, "extracao_ativa": True},
    ]
    rows = {
        "fluxo_produtivo_modular": [
            {"id": "flow-01", "modelo_id": None, "ativo": True, "nome": "Fluxo modular de referência"}
        ],
        "fluxo_produtivo_modular_etapas": [
            {"id": f"stage-{i}", "fluxo_id": "flow-01", "ordem": i}
            for i in range(1, 18)
        ],
    }
    forge._read_raw_table = lambda table, **kwargs: rows.get(table, [])
    result = forge.governed_model_context("M01", "Explique o M01 e o que temos para produção")
    linked = result["governed_discovery"]["linked_records"]
    assert linked["fluxo_produtivo_modular"][0]["modelo_id"] is None
    assert len(linked["fluxo_produtivo_modular_etapas"]) == 17
    assert result["governed_discovery"]["applicability"]["fluxo_produtivo_modular"][0]["scope"] == "family_wide_modular"
    assert result["governed_discovery"]["applicability"]["fluxo_produtivo_modular"][0]["model_specific"] is False
    assert result["provenance"]["guessed"] is False


def test_governed_model_context_traverses_external_orders_and_modular_repairs(monkeypatch):
    forge = object.__new__(SupabaseEloForge)
    base = {
        "source": "supabase_elo_forge",
        "entity": {"requested_reference": "M01", "canonical_code": "M01", "model_id": "model-01"},
        "model": {"id": "model-01", "codigo": "M01", "ativo": True},
        "relationships": {
            "taxonomia": [{"id": "tax-01", "codigo": "MLT.M01"}],
            "kits": [],
            "kit_itens": [],
            "lista_mae": [],
            "estrutura_modular": [],
        },
        "provenance": {"read_only": True, "guessed": False},
    }
    forge.model_context = lambda reference: base
    forge.governed_sources = lambda: [
        {"schema_name": "public", "table_name": "mt_pedidos_venda_itens", "dominio_codigo": "operacoes_externas", "prioridade": 82, "enabled": True, "extracao_ativa": True},
        {"schema_name": "public", "table_name": "mt_ordens_montagem_externa", "dominio_codigo": "operacoes_externas", "prioridade": 83, "enabled": True, "extracao_ativa": True},
        {"schema_name": "public", "table_name": "mt_equipe_montagem_externa", "dominio_codigo": "operacoes_externas", "prioridade": 84, "enabled": True, "extracao_ativa": True},
        {"schema_name": "public", "table_name": "mt_funcoes_montagem", "dominio_codigo": "operacoes_externas", "prioridade": 85, "enabled": True, "extracao_ativa": True},
        {"schema_name": "public", "table_name": "mt_unidades_modulares", "dominio_codigo": "reparos_modulares", "prioridade": 103, "enabled": True, "extracao_ativa": True},
        {"schema_name": "public", "table_name": "mt_ordens_reparo", "dominio_codigo": "reparos_modulares", "prioridade": 104, "enabled": True, "extracao_ativa": True},
    ]
    rows = {
        "mt_pedidos_venda_itens": [{"id": "pvi-01", "pedido_venda_id": "pedido-01", "modelo_id": "model-01"}],
        "mt_ordens_montagem_externa": [{"id": "ext-01", "pedido_venda_id": "pedido-01", "status": "PLANEJADO"}],
        "mt_equipe_montagem_externa": [{"id": "team-01", "ordem_montagem_externa_id": "ext-01", "funcao_montagem_id": "func-01"}],
        "mt_funcoes_montagem": [{"id": "func-01", "codigo": "MONT-01", "nome": "Montador"}],
        "mt_unidades_modulares": [{"id": "unit-01", "modelo_id": "model-01", "codigo_unidade": "UM-01"}],
        "mt_ordens_reparo": [{"id": "rep-01", "unidade_modular_id": "unit-01", "status": "EM_REPARO"}],
    }
    forge._read_raw_table = lambda table, **kwargs: rows.get(table, [])
    result = forge.governed_model_context("M01", "Quais operações externas e reparos modulares existem para o M01?")
    linked = result["governed_discovery"]["linked_records"]
    assert linked["mt_pedidos_venda_itens"][0]["modelo_id"] == "model-01"
    assert linked["mt_ordens_montagem_externa"][0]["id"] == "ext-01"
    assert linked["mt_equipe_montagem_externa"][0]["id"] == "team-01"
    assert linked["mt_funcoes_montagem"][0]["id"] == "func-01"
    assert linked["mt_unidades_modulares"][0]["id"] == "unit-01"
    assert linked["mt_ordens_reparo"][0]["id"] == "rep-01"
    assert result["governed_discovery"]["applicability"]["operacoes_externas"]["model_specific"] is True
    assert result["governed_discovery"]["applicability"]["reparos_modulares"]["model_specific"] is True
    assert result["provenance"]["read_only"] is True
    assert result["provenance"]["guessed"] is False
