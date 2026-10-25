from elo.cognitive.learning_memory_router import MemoryEntry, RouteAction
from elo.cognitive.reasoning.analytical_integrity import IntegrityFinding, IntegritySeverity
from elo.cognitive.reasoning.analytical_learning_feedback import (
    AnalyticalFeedbackLedger,
    EAIFLearningFeedbackBridge,
    FeedbackOutcome,
    capture_integrity_feedback,
    detect_recurring_divergence,
)


def finding():
    return IntegrityFinding(
        code="ELO-AI-004-HISTORICAL-AS-CURRENT",
        severity=IntegritySeverity.BLOCK,
        subject="fiber_capacity",
        message="historical capacity used as current",
        corrective_action="revalidate current capacity before current-state claim",
    )


def event(n: int, *, corrected: bool = False):
    return capture_integrity_feedback(
        finding(),
        tenant_id="tenant-a",
        domain="PCP",
        control_id="PCP.CAPACITY.CURRENTNESS",
        corrected_before_output=corrected,
        evidence_ids=(f"e-{n}",),
        source_ref=f"runtime://analysis/{n}",
        source_commit="abc123",
        observation_id=f"obs-{n}",
    )


def test_feedback_classifies_avoided_error_and_divergence():
    avoided = event(1, corrected=True)
    divergence = event(2, corrected=False)
    assert avoided.outcome is FeedbackOutcome.ERROR_AVOIDED
    assert divergence.outcome is FeedbackOutcome.DIVERGENCE_OCCURRED


def test_ledger_is_append_only_and_rejects_duplicate_observation():
    ledger = AnalyticalFeedbackLedger()
    item = event(1)
    ledger.append(item)
    try:
        ledger.append(item)
    except ValueError as exc:
        assert "duplicate" in str(exc)
    else:
        raise AssertionError("duplicate feedback observation must be rejected")


def test_recurrence_below_threshold_does_not_create_candidate():
    assert detect_recurring_divergence((event(1), event(2))) == ()


def test_three_divergences_create_candidate_and_avoided_error_strengthens_evidence():
    candidate = detect_recurring_divergence((event(1), event(2), event(3), event(4, corrected=True)))[0]
    assert candidate.state == "CANDIDATE"
    assert candidate.divergence_count == 3
    assert candidate.avoided_count == 1
    assert candidate.occurrences == 4
    assert candidate.evidence_ids == ("e-1", "e-2", "e-3", "e-4")
    assert candidate.concept_key.startswith("EAIF::ELO-AI-004")


def test_candidate_routes_to_existing_evolution_memory_owner_without_promotion():
    candidate = detect_recurring_divergence((event(1), event(2), event(3)))[0]
    handoff = EAIFLearningFeedbackBridge().route(candidate, ())
    assert handoff.action is RouteAction.CANDIDATE
    assert handoff.destination_id == "EVOLUTION_MEMORY"
    assert handoff.learning_admission == "CANDIDATE_FOR_GOVERNED_LEARNING"
    assert handoff.requires_lab is True
    assert handoff.canonical_mutation is False


def test_existing_matching_memory_is_reused_instead_of_parallel_candidate():
    candidate = detect_recurring_divergence((event(1), event(2), event(3)))[0]
    memory = MemoryEntry(
        memory_id="mem-1", tenant_scope="tenant-a", domain="EVOLUTION",
        learning_kind="experience", concept_key=candidate.concept_key,
        source_ref="memory/evolution/eaif", status="VALIDATED",
        destination_id="EVOLUTION_MEMORY", relation_keys=("EAIF", "ANALYTICAL_ANTI_PATTERN"),
    )
    handoff = EAIFLearningFeedbackBridge().route(candidate, (memory,))
    assert handoff.action is RouteAction.REUSE
    assert handoff.duplicate_memory_ids == ("mem-1",)
    assert handoff.requires_lab is False


def test_lab_observation_keeps_candidate_noncanonical_and_evidence_bound():
    candidate = detect_recurring_divergence((event(1), event(2), event(3)))[0]
    observation = EAIFLearningFeedbackBridge.lab_observation(candidate, source_commit="abc123")
    assert observation.domain == "EVOLUTION"
    assert observation.generalization_status == "PARTIAL"
    assert observation.evidence_ids == candidate.evidence_ids
    assert observation.existing_owner is None
    assert observation.scope == "EAIF_ANALYTICAL_ANTI_PATTERN"


def test_candidate_enters_existing_lab_path_only_after_router_admits_candidate():
    candidate = detect_recurring_divergence((event(1), event(2), event(3)))[0]

    class FakeLab:
        def evaluate(self, observation, *, principal_id, dataset_version):
            assert principal_id == "principal-a"
            assert dataset_version == "eaif-feedback-v1"
            assert observation.observation_id == candidate.candidate_id
            return "LAB_EVALUATED"

    result = EAIFLearningFeedbackBridge().route_to_governed_learning(
        candidate,
        (),
        laboratory=FakeLab(),
        principal_id="principal-a",
        dataset_version="eaif-feedback-v1",
        source_commit="abc123",
    )
    assert result.routing.action is RouteAction.CANDIDATE
    assert result.entered_lab is True
    assert result.evaluation == "LAB_EVALUATED"
