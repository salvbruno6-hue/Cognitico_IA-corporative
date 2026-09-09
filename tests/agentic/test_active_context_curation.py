from elo.agentic.contracts import IntentSpec, KnowledgeCandidate
from elo.agentic.curation import curate


def _candidate(source_id: str, *, status: str, active_context: str | None, context_match: float) -> KnowledgeCandidate:
    return KnowledgeCandidate(
        source_id=source_id,
        content=source_id,
        source_type="ELO_MEMORY",
        status=status,
        relevance=0.5,
        confidence=0.8,
        context_match=context_match,
        provenance={},
        metadata={"active_context": active_context} if active_context else {},
    )


def test_active_context_wins_over_historical_candidate() -> None:
    intent = IntentSpec(
        question="fechar a elétrica externa",
        intent="close_budget",
        domain="orçamento",
        entity="SO 157.26",
        active_context="SO 157.26",
    )
    current = _candidate(
        "current",
        status="REFERENCE",
        active_context="SO 157.26",
        context_match=0.2,
    )
    historical = _candidate(
        "historical",
        status="REFERENCE",
        active_context="SO 150.26",
        context_match=0.95,
    )

    result = curate((historical, current), 2, intent=intent)

    assert result[0].source_id == "current"


def test_historical_candidate_is_not_reclassified() -> None:
    intent = IntentSpec(question="x", intent="consult", active_context="SO 157.26")
    historical = _candidate(
        "historical",
        status="HISTORICAL",
        active_context="SO 150.26",
        context_match=0.9,
    )

    result = curate((historical,), 1, intent=intent)

    assert result[0].status == "HISTORICAL"
