from integracoes.supabase_elo_forge import SupabaseEloForge


def test_governed_model_context_routes_canonical_pcp_read_models():
    forge = object.__new__(SupabaseEloForge)
    forge.model_context = lambda reference: {
        "source": "supabase_elo_forge",
        "entity": {"requested_reference": reference, "canonical_code": "M01", "model_id": "model-01"},
        "model": {"id": "model-01", "codigo": "M01", "ativo": True},
        "relationships": {"taxonomia": [], "kits": [], "kit_itens": [], "lista_mae": [], "estrutura_modular": []},
        "provenance": {"read_only": True, "guessed": False},
    }
    forge.governed_sources = lambda: [
        {"schema_name": "public", "table_name": "v_elo_pcp_cobertura_demanda_externa", "dominio_codigo": "planejamento_pcp", "prioridade": 112, "enabled": True, "extracao_ativa": True},
        {"schema_name": "public", "table_name": "v_elo_pcp_decisao_externa_detalhe", "dominio_codigo": "operacoes_externas", "prioridade": 113, "enabled": True, "extracao_ativa": True},
        {"schema_name": "public", "table_name": "v_elo_pcp_decisao_externa_resumo", "dominio_codigo": "operacoes_externas", "prioridade": 114, "enabled": True, "extracao_ativa": True},
        {"schema_name": "public", "table_name": "v_elo_pcp_dialogo_regras", "dominio_codigo": "planejamento_pcp", "prioridade": 115, "enabled": True, "extracao_ativa": True},
    ]
    rows = {
        "v_elo_pcp_cobertura_demanda_externa": [{"modelo_id": "model-01", "modelo_codigo": "M01", "estado_cobertura": "SEM_PREVISAO", "unidades_em_reparo_recuperaveis": 0}],
        "v_elo_pcp_decisao_externa_detalhe": [{"modelo_id": "model-01", "modelo_codigo": "M01", "estado_cobertura": "SEM_PREVISAO"}],
        "v_elo_pcp_decisao_externa_resumo": [{"estado_decisao": "AGUARDANDO_HISTORICO", "ordens_externas": 0, "modelos_com_gap_reparo": 0}],
        "v_elo_pcp_dialogo_regras": [{"gap_codigo": "SEM_HISTORICO", "gate": "OBSERVAR", "bloqueia_execucao": True}],
    }
    forge._read_raw_table = lambda table, **kwargs: rows.get(table, [])

    result = forge.governed_model_context("M01", "Qual a cobertura de demanda e decisão externa do M01?")
    linked = result["governed_discovery"]["linked_records"]

    assert linked["v_elo_pcp_cobertura_demanda_externa"][0]["modelo_codigo"] == "M01"
    assert linked["v_elo_pcp_decisao_externa_detalhe"][0]["modelo_id"] == "model-01"
    assert linked["v_elo_pcp_decisao_externa_resumo"][0]["estado_decisao"] == "AGUARDANDO_HISTORICO"
    assert linked["v_elo_pcp_dialogo_regras"][0]["gap_codigo"] == "SEM_HISTORICO"
    assert result["provenance"]["read_only"] is True
    assert result["provenance"]["guessed"] is False
    assert result["governed_discovery"]["catalog_authority"] == "elo_aprendizado_fontes"
