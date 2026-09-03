from elo.core.knowledge_promotion import (
    BLOCKED_STATUS,
    FACULTY_CANDIDATE_STATUS,
    PROMOTABLE_STATUS,
    promote_validated_learning,
)


def _kwargs(**overrides):
    values = {
        "learning_id": "learning-001",
        "knowledge_key": "ORCAMENTO.REGRA.PADRAO",
        "title": "Regra reutilizável de dimensionamento",
        "concept": "Dimensionar por precedente equivalente e validar contra a evidência.",
        "provenance": {"source": "SO 120.26", "document": "TR"},
        "scope": "ORCAMENTO",
        "evidence_refs": ("SO120.26:TR:03",),
        "confidence": 0.95,
        "evolution_gate_approved": True,
    }
    values.update(overrides)
    return values


def test_validated_learning_becomes_reusable_knowledge_only_after_gate():
    decision = promote_validated_learning(**_kwargs())
    assert decision.status == PROMOTABLE_STATUS
    assert decision.payload["promotion"] == "VALIDATED_LEARNING_TO_REUSABLE_KNOWLEDGE"


def test_missing_evolution_gate_blocks_promotion():
    decision = promote_validated_learning(**_kwargs(evolution_gate_approved=False))
    assert decision.status == BLOCKED_STATUS
    assert decision.reason == "evolution_gate_not_approved"


def test_duplicate_blocks_promotion():
    decision = promote_validated_learning(**_kwargs(duplicate_found=True))
    assert decision.status == BLOCKED_STATUS
    assert decision.reason == "duplicate_or_parallel_knowledge"


def test_open_conflict_blocks_promotion():
    decision = promote_validated_learning(**_kwargs(conflict_open=True))
    assert decision.status == BLOCKED_STATUS
    assert decision.reason == "unresolved_conflict"


def test_faculty_is_only_a_candidate_after_knowledge_promotion_gates():
    decision = promote_validated_learning(**_kwargs(faculty_relevant=True))
    assert decision.status == FACULTY_CANDIDATE_STATUS
    assert decision.payload["status"] == FACULTY_CANDIDATE_STATUS
