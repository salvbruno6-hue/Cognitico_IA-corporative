from elo.agent_intake.supabase_relationship_resolver import resolve_fk_edges

def test_resolves_fk_into_provenance_backed_edge():
    edges = resolve_fk_edges(
        [{"source_table":"compras_fornecedor","source_column":"fornecedor_id",
          "target_table":"fornecedores","target_column":"id","constraint_name":"cf_fornecedor_fk"}],
        {
            "compras_fornecedor":[{"id":"c1","fornecedor_id":"f1"}],
            "fornecedores":[{"id":"f1"}],
        },
        tenant_scope="T1",
    )
    assert edges == ({
        "source":"compras_fornecedor:c1",
        "target":"fornecedores:f1",
        "relation_type":"requires",
        "provenance":"fk:cf_fornecedor_fk",
        "tenant_scope":"T1",
    },)

def test_unresolved_fk_is_not_invented():
    edges = resolve_fk_edges(
        [{"source_table":"a","source_column":"b_id","target_table":"b","target_column":"id","constraint_name":"a_b_fk"}],
        {"a":[{"id":"a1","b_id":"missing"}],"b":[]},
    )
    assert edges == ()
