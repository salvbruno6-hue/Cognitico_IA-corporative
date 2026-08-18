from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "forge" / "SPECIALIST_SKILL_REGISTRY.yaml"
DOCUMENT = ROOT / "forge" / "SPECIALIST_SKILL_REGISTRY.md"


def test_registry_contract_exists_and_declares_canonical_boundaries():
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))

    assert data["owner"] == "Forge"
    assert data["authority"] == "ELO_COGNITIVO"
    assert data["shared_faculty"] == "Core"
    assert data["promotion_gate"] == "Evolution_Gate"
    assert data["rules"]["specialist_is_parallel_core"] is False
    assert data["rules"]["specialist_is_canonical_authority"] is False
    assert data["rules"]["direct_forge_to_core_promotion"] is False
    assert data["rules"]["provenance_required"] is True
    assert data["rules"]["authorization_required"] is True
    assert data["rules"]["executable_tests_required"] is True


def test_registry_covers_initial_domain_families_without_creating_domain_cores():
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    ids = {item["id"] for item in data["domain_families"]}

    assert {
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
    } <= ids
    assert all("core" not in item["name"].lower() for item in data["domain_families"])


def test_registry_skill_contract_requires_governance_and_evidence_fields():
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    required = set(data["skill_contract"]["required_fields"])

    assert {"skill_id", "domain_family", "scope", "boundaries"} <= required
    assert {"authorized_inputs", "authorized_sources", "evidence_requirements"} <= required
    assert {"provenance_requirements", "uncertainty_rules", "escalation_rules"} <= required
    assert {"test_references", "maturity", "version", "history"} <= required
    assert {"learning_candidates", "promotion_candidates"} <= required


def test_document_preserves_the_forge_to_core_promotion_boundary():
    text = DOCUMENT.read_text(encoding="utf-8")

    assert "Forge → Core" in text
    assert "Evolution Gate" in text
    assert "historical experience" in text.lower()
    assert "provenance" in text.lower()
    assert "authorization" in text.lower()
