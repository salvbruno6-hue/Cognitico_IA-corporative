from src.elo.orcamento import BudgetExecutionEngine


def test_canonical_model_keeps_standard_items_and_accepts_excesses():
    engine = BudgetExecutionEngine()
    result = engine.execute(
        {
            "excess_items": [
                {"code": "EX.JANELA", "description": "Janela adicional", "quantity": 3, "unit": "un"}
            ]
        },
        {
            "code": "MLT.M01",
            "standard_items": [
                {"code": "M01.TOMADA", "description": "Tomada padrão", "quantity": 4, "unit": "un"}
            ],
        },
    )
    assert result.base_model == "MLT.M01"
    assert len(result.items) == 2
    assert result.items[1].source == "request_excess"
    assert result.decision == "AUTO"


def test_pending_relationships_escalate_to_specialist():
    result = BudgetExecutionEngine().execute(
        {"relationship_checks_pending": True},
        {"code": "MLT.M01", "standard_items": []},
    )
    assert result.decision == "SPECIALIST"
    assert result.specialist_question
    assert any(f.rule == "RELATIONSHIP_AUDIT" for f in result.findings)


def test_missing_model_blocks_automatic_budgeting():
    result = BudgetExecutionEngine().execute({}, None)
    assert result.decision == "BLOCKED"
    assert result.specialist_question is None
    assert any(f.rule == "MODEL_MATCH_REQUIRED" for f in result.findings)


def test_missing_model_remains_blocked_even_with_excess_items():
    result = BudgetExecutionEngine().execute(
        {
            "excess_items": [
                {"code": "EX.JANELA", "description": "Janela adicional", "quantity": 1, "unit": "un"}
            ]
        },
        None,
    )
    assert result.decision == "BLOCKED"
    assert any(f.rule == "MODEL_MATCH_REQUIRED" for f in result.findings)
