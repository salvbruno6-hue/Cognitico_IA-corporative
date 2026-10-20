from elo.agent_intake.scan_investigation_gate import build_investigation_gate, classify_concept


def valid_request(**overrides):
    request = {
        "objective": "determine whether demand cascades into PCP and production constraints",
        "scope": ["demand records", "PCP records", "production records"],
        "success_criteria": ["identify supported relationships with evidence"],
        "expected_output": "structured investigation result",
        "relevant_source_domains": ["planejamento_demanda", "planejamento_pcp", "producao_fluxo_modular"],
        "hypotheses": [
            {"id": "H1", "statement": "demand is propagated to PCP and production", "probability": 0.8},
            {"id": "H2", "statement": "the apparent relation is structural only", "probability": 0.2},
        ],
        "prohibited_actions": ["canonical mutation", "automatic learning promotion"],
    }
    request.update(overrides)
    return request


def test_missing_objective_is_blocked():
    result = build_investigation_gate(valid_request(objective=""))
    assert result.action == "BLOCKED"
    assert result.concept_outcome == "INSUFFICIENT_EVIDENCE"


def test_missing_success_criteria_is_blocked():
    result = build_investigation_gate(valid_request(success_criteria=[]))
    assert result.action == "BLOCKED"


def test_probability_does_not_select_conclusion():
    result = build_investigation_gate(valid_request())
    assert result.concept_outcome == "UNRESOLVED"
    assert result.hypotheses[0]["probability"] == 0.8


def test_cross_domain_investigation_builds_cascade_plan():
    result = build_investigation_gate(valid_request())
    pairs = {(x["from_domain"], x["to_domain"]) for x in result.relation_plan}
    assert ("planejamento_demanda", "planejamento_pcp") in pairs
    assert ("planejamento_pcp", "producao_fluxo_modular") in pairs
    assert all(x["causality_established"] is False for x in result.relation_plan)


def test_unknown_cross_domain_without_known_relation_is_blocked():
    result = build_investigation_gate(valid_request(
        relevant_source_domains=["dominio_a", "dominio_b"]
    ))
    assert result.action == "BLOCKED"


def test_provenance_and_promotion_boundaries_are_preserved():
    result = build_investigation_gate(valid_request())
    assert result.learning_candidate == {
        "promotion_state": "candidate_only",
        "canonical_mutation": False,
    }
    assert any("provenance" in x for x in result.evidence_requirements)


def test_same_request_is_idempotent():
    request = valid_request()
    assert build_investigation_gate(request) == build_investigation_gate(request)


def test_concept_classification_requires_evidence():
    assert classify_concept(evidence_count=0, coherent=True) == "INSUFFICIENT_EVIDENCE"
    assert classify_concept(evidence_count=1, coherent=True) == "SUPPORTED"
    assert classify_concept(evidence_count=1, coherent=False) == "PARTIALLY_SUPPORTED"
    assert classify_concept(evidence_count=1, coherent=None) == "UNRESOLVED"
    assert classify_concept(evidence_count=1, coherent=True, contradicted=True) == "CONTRADICTED"
