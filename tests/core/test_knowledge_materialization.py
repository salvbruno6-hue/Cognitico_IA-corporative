from elo.core.knowledge_materialization import (
    KnowledgeMaterializationError,
    materialize_promotion_package,
)
from elo.core.learning_governance import PromotionPackage


def _package(status="PROMOTABLE_KNOWLEDGE", **overrides):
    payload = {
        "knowledge_key": "orcamento.validado.v1",
        "title": "Critério validado de orçamento",
        "concept": "Aplicar o critério validado no contexto definido.",
        "source_learning_id": "learning-123",
        "provenance": {"type": "validated_learning", "source": "SO-123"},
        "scope": "orcamento",
        "evidence_refs": ("evidence-1",),
        "confidence": 0.95,
        "evolution_gate_classification": "COMPATIBLE",
        "evolution_gate_proposal_id": "proposal-123",
        "promotion": "VALIDATED_LEARNING_TO_REUSABLE_KNOWLEDGE",
    }
    payload.update(overrides)
    return PromotionPackage(status, "eligible_after_all_governance_gates", "learning-123", payload["knowledge_key"], payload)


def test_materializes_only_eligible_package():
    result = materialize_promotion_package(_package())
    assert result.path == "08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/orcamento.validado.v1.json"
    assert "ELO_VALIDATED_LEARNING_KNOWLEDGE_CANDIDATE_V1" in result.content
    assert "learning-123" in result.content
    assert "mutation_authority" in result.content


def test_faculty_candidate_is_materializable_without_creating_faculty_authority():
    result = materialize_promotion_package(_package(status="FACULTY_CANDIDATE"))
    assert result.knowledge_key == "orcamento.validado.v1"
    assert "CANDIDATE_ARTIFACT_ONLY" in result.content


def test_blocked_package_is_refused():
    try:
        materialize_promotion_package(_package(status="PROMOTION_BLOCKED"))
    except KnowledgeMaterializationError as exc:
        assert str(exc) == "promotion_package_not_eligible"
    else:
        raise AssertionError("blocked package must not be materialized")


def test_path_traversal_key_is_refused():
    try:
        materialize_promotion_package(_package(knowledge_key="../unsafe"))
    except KnowledgeMaterializationError as exc:
        assert str(exc) == "knowledge_key_invalid"
    else:
        raise AssertionError("unsafe knowledge key must be rejected")


def test_incomplete_package_is_refused():
    package = _package()
    payload = dict(package.payload)
    payload.pop("evidence_refs")
    incomplete = PromotionPackage(package.status, package.reason, package.source_learning_id, package.knowledge_key, payload)
    try:
        materialize_promotion_package(incomplete)
    except KnowledgeMaterializationError as exc:
        assert "evidence_refs" in str(exc)
    else:
        raise AssertionError("incomplete package must be rejected")
