from src.elo.agentic.orcamento_experience_interview import (
    BudgetPhase,
    build_experience_capture,
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


def test_unknown_question_is_rejected():
    interview = start_interview("SO-TEST-001")
    try:
        interview.record("not-a-question", "x")
    except ValueError as exc:
        assert str(exc) == "question_not_in_phase:not-a-question"
    else:
        raise AssertionError("unknown questions must be rejected")
