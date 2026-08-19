"""Governance invariants for canonical knowledge consolidation.

These tests intentionally validate the migration rules without touching the
ELO runtime. They protect the architecture while the physical tree is audited.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC = REPO_ROOT / "Docs" / "CANONICAL_KNOWLEDGE_AUDIT_MATRIX.md"
IMPACT = REPO_ROOT / "Docs" / "CANONICAL_KNOWLEDGE_REFERENCE_IMPACT.md"
ADDRESS = REPO_ROOT / "Docs" / "CANONICAL_KNOWLEDGE_ADDRESS_SPEC.md"
REGISTRY = REPO_ROOT / "Docs" / "CANONICAL_KNOWLEDGE_REGISTRY.md"


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


def test_registry_does_not_invent_identity_before_audit() -> None:
    content = REGISTRY.read_text(encoding="utf-8")
    assert "status = AUDIT_REQUIRED" in content
    assert "classification = PENDING" in content
    assert "review_required = true" in content
    assert "Nenhum valor `PENDING` deve ser substituído por suposição." in content


def test_registry_preserves_runtime_authority_boundary() -> None:
    content = REGISTRY.read_text(encoding="utf-8")
    assert "não substitui nem duplica a autoridade runtime do `SourceResolver`" in content
    assert "não alterar `src/elo/`" in content


def test_runtime_is_outside_this_migration_gate() -> None:
    content = SPEC.read_text(encoding="utf-8")
    assert "não altera `src/elo/`" in content
