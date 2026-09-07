from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "docs/architecture/ELO_BUDGET_SYMBIOTIC_POC_CONTRACT.md"


def test_budget_symbiotic_contract_exists_and_preserves_boundaries():
    text = CONTRACT.read_text(encoding="utf-8")
    required = (
        "GovernedBudgetingService",
        "ExecutionRouter",
        "IntelligenceRouter",
        "Learning Laboratory",
        "External AI output remains non-canonical",
        "Recommendation remains separate from approval/commit/execute authority",
    )
    for item in required:
        assert item in text


def test_budget_symbiotic_contract_preserves_end_to_end_trace():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "request_id" in text
    assert "tenant_id" in text
    assert "provider/model" in text
    assert "expected versus observed outcome" in text
