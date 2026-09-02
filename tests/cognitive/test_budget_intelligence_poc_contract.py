from pathlib import Path


def test_budget_poc_contract_preserves_single_authority_chain():
    text = Path("docs/architecture/ELO_BUDGET_INTELLIGENCE_POC_CONTRACT.md").read_text(encoding="utf-8")
    required = (
        "TENANT → MISSION → CONTEXT → CAPABILITY → EXECUTION ROUTER → INTELLIGENCE ROUTER",
        "EVIDENCE → BUDGET → CRITIQUE → DECISION → OUTCOME → LEARNING LAB → EVOLUTION GATE",
        "existing governed budgeting capability",
        "MUST NOT create a second budget engine, router, memory authority, provider registry or Evolution Gate",
    )
    for marker in required:
        assert marker in text


def test_budget_poc_requires_provenance_and_outcome_chain():
    text = Path("docs/architecture/ELO_BUDGET_INTELLIGENCE_POC_CONTRACT.md").read_text(encoding="utf-8")
    for marker in (
        "request and tenant identity",
        "provider and model",
        "evidence identifiers and provenance",
        "budget version and formula version",
        "final result",
        "expected and observed outcome",
        "learning observation identifier",
    ):
        assert marker in text
