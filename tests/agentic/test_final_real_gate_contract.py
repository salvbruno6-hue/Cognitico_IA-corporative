from elo.agentic.contracts import IntentSpec, KnowledgeCandidate, KnowledgeContext, KnowledgeGap
from elo.agentic.curation import curate


def candidate(source_id: str, status: str, context_match: float, relevance: float) -> KnowledgeCandidate:
    return KnowledgeCandidate(
        source_id=source_id,
        content=source_id,
        source_type="ELO_MEMORY",
        status=status,
        relevance=relevance,
        confidence=0.9,
        context_match=context_match,
        provenance={"origin": source_id},
    )


def test_active_context_candidate_beats_historical_candidate():
    selected = curate(
        (
            candidate("historical", "HISTORICAL", 0.2, 0.95),
            candidate("active", "APPLICABLE", 1.0, 0.8),
        ),
        limit=2,
    )
    assert selected[0].source_id == "active"


def test_required_gap_blocks_grounding():
    context = KnowledgeContext(
        intent=IntentSpec(question="close external electrical", intent="budget", active_context="SO 157.26"),
        candidates=(candidate("reference", "REFERENCE", 0.5, 0.5),),
        gaps=(KnowledgeGap("current-spec", "current specification not verified", blocks_decision=True),),
    )
    assert context.grounded is False
    assert context.requires_human_decision is True


def test_historical_reference_does_not_become_current_by_curation_alone():
    selected = curate((candidate("history", "HISTORICAL", 1.0, 1.0),), limit=1)
    assert selected[0].status == "HISTORICAL"
