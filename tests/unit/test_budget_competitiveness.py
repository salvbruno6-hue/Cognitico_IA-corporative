from elo.cognitive.orcamento.competitividade import BudgetCompetitivenessAnalyzer
from elo.cognitive.orcamento.competitividade.abc import classify_abc
from elo.cognitive.orcamento.competitividade.models import BudgetItem


def test_abc_thresholds_are_deterministic():
    assert classify_abc(0.80) == "A"
    assert classify_abc(0.81) == "B"
    assert classify_abc(0.95) == "B"
    assert classify_abc(0.951) == "C"


def test_analyzer_prioritizes_class_a_without_mutation():
    items = [
        BudgetItem(item_id="A", total_value=800.0),
        BudgetItem(item_id="B", total_value=150.0),
        BudgetItem(item_id="C", total_value=50.0),
    ]
    result = BudgetCompetitivenessAnalyzer().analyze(items)
    assert result["canonical_mutation"] is False
    assert result["authority"] == "analysis_only"
    assert result["priority_items"][0]["item_id"] == "A"


def test_zero_budget_is_rejected():
    items = [BudgetItem(item_id="A", total_value=0.0)]
    try:
        BudgetCompetitivenessAnalyzer().analyze(items)
    except ValueError as exc:
        assert "positive" in str(exc)
    else:
        raise AssertionError("zero budget must be rejected")
