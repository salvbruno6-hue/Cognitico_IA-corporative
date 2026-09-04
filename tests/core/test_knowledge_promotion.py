from elo.core.evolution_gate import EvolutionClassification, EvolutionDecision
from elo.core.knowledge_promotion import (
    BLOCKED_STATUS,
    FACULTY_CANDIDATE_STATUS,
    PROMOTABLE_STATUS,
    promote_validated_learning,
)


def _decision(classification=EvolutionClassification.COMPATIBLE, mutation=False):
    return EvolutionDecision(
        proposal_id="proposal-001",
        classification=classification,
        canonical_mutation_allowed=mutation,
        preserve_as_alternative=False,
        human_decision_required=False,
        rationale="test",
        evidence_ids=("e-001",),
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
        "evolution_decision": _decision(),
    }
    values.update(overrides)
    return values


def test_validated_learning_becomes_reusable_knowledge_only_after_real_gate_decision():
    decision = promote_validated_learning(**_kwargs())
    assert decision.status == PROMOTABLE_STATUS
    assert decision.payload["promotion"] == "VALIDATED_LEARNING_TO_REUSABLE_KNOWLEDGE"
    assert decision.payload["evolution_gate_proposal_id"] == "proposal-001"


def test_missing_evolution_decision_blocks_promotion():
    decision = promote_validated_learning(**_kwargs(evolution_decision=None))
    assert decision.status == BLOCKED_STATUS
    assert decision.reason == "evolution_gate_decision_missing"


def test_non_compatible_evolution_decision_blocks_promotion():
    decision = promote_validated_learning(
        **_kwargs(evolution_decision=_decision(EvolutionClassification.ADAPT_REQUIRED))
    )
    assert decision.status == BLOCKED_STATUS
    assert decision.reason == "evolution_gate_not_compatible:ADAPT_REQUIRED"


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


def test_promotion_cannot_grant_mutation_authority():
    decision = promote_validated_learning(**_kwargs(evolution_decision=_decision(mutation=True)))
    assert decision.status == BLOCKED_STATUS
    assert decision.reason == "unexpected_gate_mutation_authority"
