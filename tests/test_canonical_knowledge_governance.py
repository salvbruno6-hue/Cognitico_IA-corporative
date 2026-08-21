"""Governance invariants for canonical knowledge consolidation.

These tests validate migration rules without touching the ELO runtime. They
protect the architecture while the physical tree is audited.
"""

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC = REPO_ROOT / "Docs" / "CANONICAL_KNOWLEDGE_AUDIT_MATRIX.md"
IMPACT = REPO_ROOT / "Docs" / "CANONICAL_KNOWLEDGE_REFERENCE_IMPACT.md"
ADDRESS = REPO_ROOT / "Docs" / "CANONICAL_KNOWLEDGE_ADDRESS_SPEC.md"
REGISTRY = REPO_ROOT / "Docs" / "CANONICAL_KNOWLEDGE_MIGRATION_REGISTRY.json"


def test_canonical_knowledge_governance_specs_exist() -> None:
    assert SPEC.is_file()
    assert IMPACT.is_file()
    assert ADDRESS.is_file()
    assert REGISTRY.is_file()


def test_classification_model_is_explicit() -> None:
    content = SPEC.read_text(encoding="utf-8")
    for code in ("EQ", "CP", "CF", "EX", "HI", "NR"):
        assert f"| {code} |" in content


def test_migration_order_protects_references() -> None:
    content = SPEC.read_text(encoding="utf-8")
    sequence_start = content.index("## 10. Sequência de execução")
    sequence_end = content.index("## 11. Estado da fase", sequence_start)
    sequence = content[sequence_start:sequence_end]
    expected = [
        "Inventário",
        "Hash/conteúdo",
        "Classificação",
        "Identidade",
        "Mapa de referências",
        "Decisão de migração",
        "Atualização de índices/aliases",
        "Testes",
        "Depreciação",
    ]
    positions = [sequence.index(item) for item in expected]
    assert positions == sorted(positions)


def test_physical_removal_is_gated() -> None:
    content = SPEC.read_text(encoding="utf-8")
    assert "Nenhuma remoção física" in content
    assert "conflito não decidido" in content
    assert "referência quebrada" in content


def test_identity_survives_path_change() -> None:
    content = IMPACT.read_text(encoding="utf-8")
    assert "artifact_id permanece" in content
    assert "concept_id permanece" in content
    assert "canonical_path pode mudar" in content


def test_existing_registry_is_the_single_documentary_registry() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert registry["schema_version"] == "1.2"
    assert registry["runtime_authority"] == "existing SourceResolver"
    assert registry["runtime_change_allowed"] is False
    assert registry["physical_removal_allowed"] is False
    assert len(registry["families"]) == 9


def test_registry_tracks_audit_state_without_fabricating_completion() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    allowed_identity = {"PENDING", "ASSIGNED"}
    allowed_reference = {"PENDING"}
    allowed_provenance = {"PENDING", "PRESERVED"}
    for family in registry["families"]:
        assert family["identity_status"] in allowed_identity
        assert family["reference_status"] in allowed_reference
        assert family["provenance_status"] in allowed_provenance
        assert family["review_required"] is True


def test_registry_preserves_runtime_authority_boundary() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert registry["runtime_authority"] == "existing SourceResolver"
    assert registry["runtime_change_allowed"] is False
    assert "Keep the existing SourceResolver as runtime authority." in registry["rules"]


def test_runtime_is_outside_this_migration_gate() -> None:
    content = SPEC.read_text(encoding="utf-8")
    assert "não altera `src/elo/`" in content
