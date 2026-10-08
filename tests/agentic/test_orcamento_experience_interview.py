from src.elo.agentic.orcamento_experience_interview import (
    BudgetPhase,
    BudgetSourceRef,
    build_experience_capture,
    build_persistence_plan,
    close_interview,
    continue_interview,
    start_interview,
)


def test_start_checkpoint_focuses_on_context():
    interview = start_interview("SO-TEST-001")
    assert interview.phase is BudgetPhase.START
    assert {q.id for q in interview.questions} >= {
        "context_objective",
        "context_requirements",
        "context_uncertainty",
    }


def test_middle_checkpoint_captures_reasoning_and_correction():
    interview = continue_interview("SO-TEST-001")
    assert interview.phase is BudgetPhase.MIDDLE
    ids = {q.id for q in interview.questions}
    assert {"decision_alternative", "knowledge_used", "evidence_calculation", "problem_gap"} <= ids


def test_end_checkpoint_targets_final_drivers_and_reuse():
    interview = close_interview("SO-TEST-001")
    assert interview.phase is BudgetPhase.END
    ids = {q.id for q in interview.questions}
    assert {"result_final_driver", "result_key_decisions", "evidence_final", "knowledge_reusable"} <= ids


def test_capture_maps_to_existing_experience_fields_without_promotion():
    capture = build_experience_capture(
        "SO-TEST-001",
        BudgetPhase.END,
        {
            "result_final_driver": "modelo base + adaptação elétrica",
            "result_key_decisions": ["usar MLT.M01"],
            "evidence_final": "planilha revisada",
            "knowledge_reusable": "comparar elétrica antes de precificar",
        },
    )
    assert capture["resultado"]["result_final_driver"]
    assert capture["decisoes"]["result_key_decisions"]
    assert capture["verificacoes"]["evidence_final"]
    assert capture["learning_candidate"] is False
    assert capture["canonical_mutation"] is False
    assert capture["status_validacao"] == "OBSERVADA"


def test_persistence_plan_targets_existing_learning_tables_and_preserves_origin():
    plan = build_persistence_plan(
        "SO-TEST-001",
        BudgetPhase.END,
        {
            "context_objective": "precificar uma solução modular",
            "result_final_driver": "modelo + restrição logística",
            "result_confidence": 0.8,
            "evidence_final": "planilha revisada",
        },
        [
            BudgetSourceRef(
                table_name="elo_orcamento_memoria",
                record_key="memoria:123",
                source_id="9f631f70-62a8-4e29-b178-a6ce6a33579c",
            ),
            BudgetSourceRef(
                table_name="elo_orcamento_calculos_aprendidos",
                record_key="learning:456",
                source_id="49ef14d8-5cd4-4959-b890-3196dd45be01",
            ),
        ],
    )
    assert plan["target"]["experience_table"] == "elo_aprendizado_experiencias"
    assert plan["target"]["extraction_table"] == "elo_aprendizado_extracoes"
    assert plan["target"]["relation_table"] == "elo_aprendizado_relacoes"
    assert plan["experience"]["origem"] == "elo_orcamento_memoria"
    assert plan["experience"]["origem_referencia"] == "elo_orcamento_memoria:memoria:123"
    assert len(plan["extractions"]) == 2
    assert plan["extractions"][0]["fonte_id"] == "9f631f70-62a8-4e29-b178-a6ce6a33579c"
    assert plan["relations"][0]["relation_type"] == "derived_from"
    assert plan["governance"]["learning_candidate"] is False
    assert plan["governance"]["canonical_mutation"] is False


def test_persistence_plan_requires_real_source_identity():
    try:
        build_persistence_plan("SO-TEST-001", BudgetPhase.END, {}, [])
    except ValueError as exc:
        assert str(exc) == "budget_source_required"
    else:
        raise AssertionError("source identity must never be invented")


def test_unknown_question_is_rejected():
    interview = start_interview("SO-TEST-001")
    try:
        interview.record("not-a-question", "x")
    except ValueError as exc:
        assert str(exc) == "question_not_in_phase:not-a-question"
    else:
        raise AssertionError("unknown questions must be rejected")
