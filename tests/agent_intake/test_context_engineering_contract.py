from pathlib import Path


ROOT = Path(__file__).parents[2]
CONTRACT = ROOT / "docs/architecture/ELO_CONTEXT_ENGINEERING_CONTRACT.md"
FORGE_CONTRACT = ROOT / "forge/ELO_FORGE_CONSTRUCTOR_CONTRACT.md"
PROMOTION = ROOT / "docs/governance/ELO_FORGE_KNOWLEDGE_PROMOTION_PROTOCOL.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_context_engineering_contract_exists_and_has_two_loops():
    text = read(CONTRACT)
    assert "ELO Context Engineering Contract" in text
    assert "OBSERVE → LOAD CONTEXT → INTERPRET → DECIDE → ROUTE → EXECUTE → EVIDENCE" in text
    assert "OBSERVE\n  ↓\nLOAD CONTEXT" in text
    assert "GOVERN" in text


def test_contract_preserves_existing_forge_and_promotion_boundaries():
    context = read(CONTRACT)
    forge = read(FORGE_CONTRACT)
    promotion = read(PROMOTION)

    assert "Forge has execution authority" in forge
    assert "no canonical authority" in forge
    assert "Forge → Core" in context
    assert "Evolution Gate" in context
    assert "Learning" in promotion


def test_contract_has_no_new_universal_authority():
    text = read(CONTRACT)
    for forbidden in (
        "a second Core",
        "a second Memory Engine",
        "a second Router",
        "a universal context database",
        "an automatic learning promoter",
    ):
        assert forbidden in text


def test_context_contract_requires_idempotence_and_isolation():
    text = read(CONTRACT)
    assert "idempotent" in text
    assert "tenant/domain boundaries" in text
    assert "historical evidence remains immutable" in text
    assert "unknown information is not fabricated" in text


def test_context_contract_separates_decision_evidence_and_learning():
    text = read(CONTRACT)
    assert "FATO → EVIDÊNCIA → HIPÓTESE → ANÁLISE → RECOMENDAÇÃO → DECISÃO" in text
    assert "A successful execution is evidence, not generalized learning." in text
    assert "VALIDATED LEARNING / CORE PROMOTION" in text


def test_context_contract_treats_budget_as_scoped_context_not_universal_truth():
    text = read(CONTRACT)
    assert "Orçamento" in text
    assert "actual-vs-estimated" in text
    assert "universal pricing rule" in text
    assert "source and version" in text
