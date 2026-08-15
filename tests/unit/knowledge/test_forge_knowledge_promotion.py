from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / "docs/knowledge/forge/MULTITEINER_KNOWLEDGE_PROMOTION_REGISTRY.md"
PROTOCOL = ROOT / "docs/governance/ELO_FORGE_KNOWLEDGE_PROMOTION_PROTOCOL.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_registry_and_protocol_exist() -> None:
    assert REGISTRY.is_file()
    assert PROTOCOL.is_file()


def test_registry_is_curated_not_a_full_source_copy() -> None:
    registry = _read(REGISTRY)
    assert "Este registro é uma seleção governada" in registry
    assert "MULTITEINER_ORGANIZATIONAL_CONTEXT.md" in registry
    assert "REUSE" in registry
    assert "EXTEND" in registry
    assert "ROADMAP" in registry
    assert "CONFLICT" in registry


def test_promotion_requires_provenance_and_validation() -> None:
    protocol = _read(PROTOCOL)
    required = [
        "possui proveniência",
        "não é duplicação conhecida",
        "não possui conflito aberto não resolvido",
        "possui evidência suficiente",
        "passou pelo gate de evolução",
    ]
    for phrase in required:
        assert phrase in protocol


def test_detach_preserves_promoted_knowledge() -> None:
    protocol = _read(PROTOCOL)
    assert "fonte removida → conhecimento promovido permanece" in protocol
    assert "Core íntegro" in protocol


def test_source_system_is_not_a_core_dependency() -> None:
    protocol = _read(PROTOCOL)
    assert "fazer o Core depender do sistema de origem" in protocol
    assert "O Forge é fonte de conhecimento e histórico. Não é o Cognitive Core." in protocol
