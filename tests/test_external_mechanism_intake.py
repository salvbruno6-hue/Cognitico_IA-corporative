import pytest

from elo.core.learning_governance import GovernedLearningService, LearningGovernanceError


def test_external_mechanism_intake_creates_candidate_only():
    candidate = GovernedLearningService.ingest_external_mechanism(
        source_name="TraceGate",
        source_kind="repository",
        source_ref="ducminhle1904/TraceGate",
        mechanism_id="tool-contract-replay",
        mechanism="tool-call contracts, JSONL trace and deterministic replay",
        proposed_capability="CAP-TRACE-DE-EXECUCAO",
        existing_owner="existing audit/provenance infrastructure",
        disposition="STRENGTHEN",
        evidence_refs=("repo:TraceGate/tests", "repo:TraceGate/README"),
        scope="general ELO execution governance",
        generalized=True,
    )
    assert candidate.state == "CANDIDATE"
    assert candidate.disposition == "STRENGTHEN"
    assert candidate.generalized is True
    assert candidate.evidence_refs


def test_external_mechanism_create_requires_proven_absence():
    with pytest.raises(LearningGovernanceError, match="proven absence"):
        GovernedLearningService.ingest_external_mechanism(
            source_name="SafeAI",
            source_kind="zip",
            source_ref="SafeAI-main.zip",
            mechanism_id="capability-escalation",
            mechanism="capability escalation detection",
            proposed_capability="CAP-DETECCAO-DE-ESCALADA-DE-CAPACIDADE",
            existing_owner="Capability Registry",
            disposition="CREATE",
            evidence_refs=("zip:SafeAI-main.zip",),
            scope="general ELO capability governance",
            generalized=True,
        )


def test_external_mechanism_create_requires_generalization():
    with pytest.raises(LearningGovernanceError, match="generalized mechanism"):
        GovernedLearningService.ingest_external_mechanism(
            source_name="local-tool",
            source_kind="zip",
            source_ref="local-tool.zip",
            mechanism_id="company-specific-rule",
            mechanism="company-specific workflow rule",
            proposed_capability="LOCAL_RULE",
            existing_owner="NONE",
            disposition="CREATE",
            evidence_refs=("zip:local-tool.zip",),
            scope="company only",
            generalized=False,
        )


def test_external_mechanism_requires_evidence():
    with pytest.raises(LearningGovernanceError, match="evidence_refs"):
        GovernedLearningService.ingest_external_mechanism(
            source_name="OpenLore",
            source_kind="repository",
            source_ref="clay-good/OpenLore",
            mechanism_id="orientation",
            mechanism="contextual orientation",
            proposed_capability="CAP-ORIENTACAO-CONTEXTUAL",
            existing_owner="existing context/knowledge graph",
            disposition="STRENGTHEN",
            evidence_refs=(),
            scope="general ELO cognition",
            generalized=True,
        )
