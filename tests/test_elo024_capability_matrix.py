import json
from pathlib import Path


MATRIX = Path("docs/governance/ELO_024_BUDGETING_CAPABILITY_MATRIX.json")
REQUIRED = {
    "demand",
    "capacity",
    "cost",
    "pricing",
    "margin",
    "forecast",
    "resource_planning",
    "risk",
    "quotation",
    "specialist_feedback",
    "budget_vs_actual",
    "post_budget_learning",
}


def load_matrix():
    return json.loads(MATRIX.read_text(encoding="utf-8"))


def test_elo024_capability_matrix_is_complete_and_explicit():
    document = load_matrix()
    capabilities = {item["name"]: item for item in document["capabilities"]}
    assert REQUIRED == set(capabilities)
    assert all(item["owner"] and item["evidence"] for item in capabilities.values())
    assert all(item["status"] in {"IMPLEMENTED", "CONTRACT", "GAP"} for item in capabilities.values())


def test_elo024_does_not_claim_missing_forecast_or_risk_engines_as_implemented():
    capabilities = {item["name"]: item for item in load_matrix()["capabilities"]}
    assert capabilities["forecast"]["status"] == "CONTRACT"
    assert capabilities["risk"]["status"] == "CONTRACT"
    assert "Dedicated" in capabilities["forecast"]["limitation"]
    assert "Dedicated" in capabilities["risk"]["limitation"]


def test_elo024_governance_invariants_are_present():
    invariants = load_matrix()["non_negotiable"]
    text = " ".join(invariants)
    assert "GAP" in text
    assert "Provenance" in text
    assert "Forge" in text
    assert "Recommendation" in text
    assert "second Core" in text
