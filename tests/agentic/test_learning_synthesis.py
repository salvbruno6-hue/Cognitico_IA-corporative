from elo.agentic.learning_synthesis import synthesize_decision_pattern


def test_synthesis_extracts_reusable_pattern_from_missing_arbitration_experience():
    experience = {
        "contexto": "SO 182.26 — sem retorno do cliente aos questionamentos",
        "dependencias": ["SO", "TR", "layout", "composição interna"],
        "decisoes": [
            "prosseguir com orçamento usando premissas internas sustentadas",
            "não assumir rede externa sem evidência",
        ],
        "verificacoes": [
            "separar fato de premissa",
            "registrar pergunta original e decisão",
        ],
        "resultado": [
            "questionamentos sem resposta podem ser convertidos em premissas "
            "somente quando houver base técnica ou documental"
        ],
    }
    pattern = synthesize_decision_pattern(
        experience, experience_id="6df6e179-2430-4f9f-a51e-e74fced24c93"
    )
    assert pattern.status == "CANDIDATO"
    assert "há uma dúvida/requisito sem arbitragem externa suficiente" in pattern.gatilhos
    assert any("verificar equivalência" in step for step in pattern.sequencia)
    assert any("não transformar" in item for item in pattern.limitacoes)
    assert pattern.origem_experiencias == ("6df6e179-2430-4f9f-a51e-e74fced24c93",)


def test_synthesis_does_not_copy_the_source_decision_as_a_canonical_rule():
    experience = {
        "contexto": "decisão técnica com condição identificável",
        "decisoes": ["usar solução X neste projeto"],
        "verificacoes": ["solução X atende à condição observada"],
    }
    pattern = synthesize_decision_pattern(experience)
    assert pattern.status == "CANDIDATO"
    assert "usar solução X neste projeto" not in pattern.regras_decisao
    assert "não aplicar automaticamente sem validação da SO atual" in pattern.limitacoes


def test_synthesis_requires_decision_and_evidence():
    try:
        synthesize_decision_pattern({"contexto": "caso"})
    except ValueError as exc:
        assert "decision" in str(exc)
    else:
        raise AssertionError("expected missing-decision validation")


def test_row_shape_matches_canonical_reasoning_pattern_fields():
    pattern = synthesize_decision_pattern(
        {"contexto": "caso", "decisoes": ["decidir sob condição"], "resultado": ["resultado observado"]}
    )
    row = pattern.as_candidate_payload()
    assert {
        "nome", "gatilhos", "pre_requisitos", "sequencia", "regras_decisao",
        "heuristicas", "evidencias", "status",
    }.issubset(row)
    assert row["status"] == "CANDIDATO"


def test_decision_pattern_candidate_attaches_to_existing_decision_lifecycle_without_learning():
    from elo.core.decision_outcome_loop import DecisionLifecycle
    from elo.core.systemic_primitives import DecisionRecord

    lifecycle = DecisionLifecycle(DecisionRecord("d-pattern", "replan", "capacity gap"))
    pattern = synthesize_decision_pattern({
        "contexto": "capacidade com condição identificável",
        "decisoes": ["replanejar sob condição observada"],
        "verificacoes": ["capacidade e prazo verificados"],
    })

    lifecycle.attach_decision_pattern_candidate(
        pattern.as_candidate_payload(),
        candidate_ref="PATTERN-REF-1",
    )

    assert lifecycle.decision_pattern_candidate["status"] == "CANDIDATO"
    assert lifecycle.decision_pattern_candidate["nome"] == pattern.nome
    assert lifecycle.decision_pattern_candidate_ref == "PATTERN-REF-1"
    assert lifecycle.learning_candidate is None


def test_decision_pattern_candidate_cannot_bypass_evaluation_boundary():
    from elo.core.decision_outcome_loop import DecisionLifecycle, DecisionState
    from elo.core.systemic_primitives import DecisionRecord, OutcomeFeedback

    lifecycle = DecisionLifecycle(DecisionRecord("d-pattern", "replan", "capacity gap"))
    pattern = synthesize_decision_pattern({
        "contexto": "capacidade com condição identificável",
        "decisoes": ["replanejar sob condição observada"],
        "verificacoes": ["capacidade e prazo verificados"],
    })

    lifecycle.attach_decision_pattern_candidate(
        pattern.as_candidate_payload(),
        candidate_ref="PATTERN-REF-1",
    )
    lifecycle.transition(DecisionState.APPROVED)
    lifecycle.transition(DecisionState.EXECUTED)
    lifecycle.transition(DecisionState.OBSERVING)
    lifecycle.attach_outcome(
        OutcomeFeedback("d-pattern", "ok", "ok", evidence_ids=("e-pattern",))
    )
    lifecycle.transition(DecisionState.EVALUATED, evidence_ids=("e-pattern",))

    try:
        lifecycle.attach_decision_pattern_candidate(
            pattern.as_candidate_payload(),
            candidate_ref="PATTERN-REF-1",
        )
    except ValueError as exc:
        assert "before evaluation" in str(exc)
    else:
        raise AssertionError("expected evaluated-state boundary")
