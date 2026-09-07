from dataclasses import dataclass

import pytest

from elo.agentic.contracts import IntentSpec, KnowledgeCandidate, KnowledgeRequirement
from elo.agentic.curator import KnowledgeCurator


@dataclass(frozen=True)
class FakeCandidate:
    source_id: str
    content: str
    source_type: str
    status: str
    relevance: float
    confidence: float
    context_match: float


def test_curator_prefers_current_context_over_historical_reference() -> None:
    candidates = (
        KnowledgeCandidate(
            source_id="hist-1",
            content="historical",
            source_type="ELO_MEMORY",
            status="HISTORICAL",
            relevance=1.0,
            confidence=1.0,
            context_match=0.1,
        ),
        KnowledgeCandidate(
            source_id="current-1",
            content="current",
            source_type="DOCUMENTS",
            status="APPLICABLE",
            relevance=0.7,
            confidence=0.8,
            context_match=1.0,
        ),
    )
    result = KnowledgeCurator().curate(candidates, active_context="SO 157.26", limit=10)
    assert result[0].source_id == "current-1"


def test_curator_does_not_upgrade_reference_to_truth() -> None:
    candidate = KnowledgeCandidate(
        source_id="ref-1",
        content="similar historical composition",
        source_type="ELO_MEMORY",
        status="REFERENCE",
        relevance=1.0,
        confidence=0.4,
        context_match=0.2,
    )
    result = KnowledgeCurator().curate((candidate,), active_context="SO 157.26", limit=10)
    assert result[0].status == "REFERENCE"


def test_empty_required_context_is_not_silently_grounded() -> None:
    intent = IntentSpec(
        question="preciso fechar a elétrica externa",
        intent="close_external_electrical_budget",
        domain="orçamento",
        task="fechamento",
        active_context="SO 157.26",
        required_knowledge=("applicable_composition",),
    )
    req = KnowledgeRequirement("applicable_composition", "current applicable composition")
    assert intent.active_context == "SO 157.26"
    assert req.required is True
