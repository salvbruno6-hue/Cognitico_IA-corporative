from elo.agent_intake.relationship_investigator import investigate_relationships

def test_demand_cascade_is_bounded_and_noncausal():
    records = [{"id": "demand"}, {"id": "pcp"}, {"id": "production"}, {"id": "rh"}]
    edges = [
        {"source":"demand","target":"pcp","relation_type":"requires","provenance":"fk:demanda->pcp","tenant_scope":"T1"},
        {"source":"pcp","target":"production","relation_type":"depends_on","provenance":"fk:pcp->production","tenant_scope":"T1"},
        {"source":"pcp","target":"rh","relation_type":"requires","provenance":"fk:pcp->rh","tenant_scope":"T1"},
    ]
    result = investigate_relationships(records, edges, tenant_scope="T1", max_depth=3)
    assert any(p.nodes == ("demand","pcp","production") for p in result.paths)
    assert result.causality_established is False
    assert result.learning_eligible is False

def test_supplier_inventory_purchase_chain_requires_provenance():
    records = [{"id":"supplier"},{"id":"purchase"},{"id":"stock"}]
    edges = [
        {"source":"supplier","target":"purchase","provenance":"fk:supplier"},
        {"source":"purchase","target":"stock","provenance":"fk:purchase-stock"},
    ]
    result = investigate_relationships(records, edges, tenant_scope="T1")
    assert result.paths
    assert "structural relationships do not establish causality" in result.evidence_gaps

def test_tenant_isolation_rejects_foreign_edges():
    records = [{"id":"a"},{"id":"b"}]
    edges = [{"source":"a","target":"b","provenance":"fk:x","tenant_scope":"T2"}]
    result = investigate_relationships(records, edges, tenant_scope="T1")
    assert result.paths == ()
    assert result.learning_eligible is False

def test_missing_provenance_is_not_a_relationship():
    records = [{"id":"a"},{"id":"b"}]
    edges = [{"source":"a","target":"b","tenant_scope":"T1"}]
    result = investigate_relationships(records, edges, tenant_scope="T1")
    assert result.paths == ()
