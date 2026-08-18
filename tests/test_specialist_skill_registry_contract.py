from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "forge" / "SPECIALIST_SKILL_REGISTRY.yaml"
DOCUMENT = ROOT / "forge" / "SPECIALIST_SKILL_REGISTRY.md"


def registry_text() -> str:
    return REGISTRY.read_text(encoding="utf-8")


def test_registry_contract_exists_and_declares_canonical_boundaries():
    text = registry_text()

    assert "schema: ELO-FORGE-SPECIALIST-SKILL-REGISTRY.v1" in text
    assert "owner: Forge" in text
    assert "authority: ELO_COGNITIVO" in text
    assert "shared_faculty: Core" in text
    assert "promotion_gate: Evolution_Gate" in text
    assert "specialist_is_parallel_core: false" in text
    assert "specialist_is_canonical_authority: false" in text
    assert "direct_forge_to_core_promotion: false" in text
    assert "provenance_required: true" in text
    assert "authorization_required: true" in text
    assert "executable_tests_required: true" in text


def test_registry_covers_initial_domain_families_without_creating_domain_cores():
    text = registry_text()

    for domain_id in (
        "HR",
        "BUDGETING",
        "PCP",
        "PROCUREMENT",
        "LOGISTICS",
        "COMMERCIAL",
        "FINANCE",
        "ENGINEERING",
        "QUALITY",
        "RISK",
        "PROCESS_ANALYSIS",
        "DATA_ANALYSIS",
    ):
        assert f"id: {domain_id}" in text

    assert "name: HR / People / Labor" in text
    assert "name: PCP / Production Planning and Control" in text
    assert "name: Data Analysis / Calculation / Simulation" in text


def test_registry_skill_contract_requires_governance_and_evidence_fields():
    text = registry_text()

    for field in (
        "skill_id",
        "domain_family",
        "scope",
        "boundaries",
        "authorized_inputs",
        "authorized_sources",
        "evidence_requirements",
        "provenance_requirements",
        "uncertainty_rules",
        "escalation_rules",
        "test_references",
        "maturity",
        "version",
        "history",
        "learning_candidates",
        "promotion_candidates",
    ):
        assert f"    - {field}" in text


def test_document_preserves_the_forge_to_core_promotion_boundary():
    text = DOCUMENT.read_text(encoding="utf-8")

    assert "Forge → Core" in text
    assert "Evolution Gate" in text
    assert "historical experience" in text.lower()
    assert "provenance" in text.lower()
    assert "authorization" in text.lower()
