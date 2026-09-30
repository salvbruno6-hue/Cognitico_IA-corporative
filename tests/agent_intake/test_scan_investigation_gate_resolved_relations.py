from elo.agent_intake.scan_investigation_gate import build_investigation_gate

def test_gate_consumes_resolved_edges():
    result = build_investigation_gate({
        "objective":"investigate demand cascade",
        "scope":["demand","pcp","production"],
        "success_criteria":["trace evidence"],
        "expected_output":"bounded cascade",
        "relevant_source_domains":["planejamento_demanda","planejamento_pcp","producao_fluxo_modular"],
        "hypotheses":[{"id":"H1","statement":"demand propagates to production","probability":0.7}],
        "tenant_scope":"T1",
        "records":[{"id":"d"},{"id":"p"},{"id":"o"}],
        "relationship_edges":[
            {"source":"d","target":"p","relation_type":"requires","provenance":"fk:d-p","tenant_scope":"T1"},
            {"source":"p","target":"o","relation_type":"depends_on","provenance":"fk:p-o","tenant_scope":"T1"},
        ],
    })
    assert result.action == "INVESTIGATE"
    resolved = [x for x in result.evidence if "resolved_paths" in x]
    assert resolved and resolved[0]["resolved_paths"] >= 2
    assert resolved[0]["causality_established"] is False

def test_gate_does_not_turn_structural_edge_into_learning():
    result = build_investigation_gate({
        "objective":"investigate supplier chain",
        "scope":["supplier","purchase"],
        "success_criteria":["identify relationship"],
        "expected_output":"relationship evidence",
        "relevant_source_domains":["compras","produtos"],
        "hypotheses":[{"statement":"supplier affects purchase outcome","probability":0.5}],
        "tenant_scope":"T1",
        "records":[{"id":"s"},{"id":"p"}],
        "relationship_edges":[{"source":"s","target":"p","provenance":"fk:s-p","tenant_scope":"T1"}],
    })
    assert result.learning_candidate["promotion_state"] == "candidate_only"
    assert result.learning_candidate["canonical_mutation"] is False
