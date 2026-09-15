"""SPC-01 critical maturity integration evidence.

This is a deterministic Forge-lab execution of the existing specialist -> skill ->
 evidence -> feedback -> learning -> Evolution Gate chain. It intentionally does
not claim real-world specialist/human validation (see issue #137).
"""

import pytest

from elo.core.evolution_gate import EvolutionClassification, EvolutionGate, EvolutionProposal
from elo.core.learning_governance import GovernedLearningService, LearningGovernanceError
from elo.core.specialist_feedback import SpecialistFeedback, SpecialistFeedbackRegistry
from elo.core.specialist_skill_resolution import SpecialistSkill, SpecialistSkillResolver


class RecordingMemory:
    """Minimal in-process adapter proving the canonical learning call boundary."""

    def __init__(self) -> None:
        self.records = []

    def remember(self, **payload):
        self.records.append(payload)
        return payload


def _resolve_specialist():
    resolver = SpecialistSkillResolver(
        [
            SpecialistSkill(
                skill_id="forge.specialist.fixture",
                domain_family="operations",
                maturity="GOVERNED",
                scope="tenant:lab",
                boundaries="evidence-only",
                authorization_required=True,
            )
        ]
    )
    return resolver.resolve(
        domain_family="operations",
        authorized=lambda skill: skill.scope == "tenant:lab" and skill.boundaries == "evidence-only",
        minimum_maturity="GOVERNED",
    )


def _gate_decision():
    proposal = EvolutionProposal(
        proposal_id="spc01-lab-proposal",
        tenant_id="tenant-lab",
        source_id="spc01-lab",
        summary="Convert validated specialist feedback into reusable learning candidate",
        purpose_alignment=True,
        identity_compatible=True,
        architecture_compatible=True,
        governance_compatible=True,
        evidence_ids=("E-SPC01-001", "E-SPC01-002"),
        maturity_score=0.9,
        provenance={"source": "spc01-lab", "environment": "github-actions"},
    )
    return EvolutionGate().evaluate(proposal)


def test_spc01_specialist_skill_feedback_learning_governed_chain():
    resolution = _resolve_specialist()
    assert resolution.resolved
    assert resolution.skill_id == "forge.specialist.fixture"
    assert resolution.maturity == "GOVERNED"

    feedback_registry = SpecialistFeedbackRegistry()
    feedback = SpecialistFeedback(
        feedback_id="FB-SPC01-001",
        specialist_id=resolution.skill_id,
        tenant_id="tenant-lab",
        domain="operations",
        source_reference="fixture://spc01",
        observation="Specialist confirmed the bounded evidence-only procedure",
        evidence_ids=("E-SPC01-001",),
        provenance={"environment": "github-actions", "kind": "lab-fixture"},
    )
    feedback_registry.ingest(feedback)
    assert feedback_registry.list(tenant_id="tenant-lab", domain="operations") == (feedback,)

    memory = RecordingMemory()
    learning = GovernedLearningService(memory)
    experience = learning.capture_outcome(
        tenant_id="tenant-lab",
        domain="operations",
        principal_id="spc01-lab-principal",
        decision_id="D-SPC01-001",
        expected_outcome="bounded specialist procedure",
        observed_outcome=feedback.observation,
        evidence_ids=feedback.evidence_ids,
    )
    assert experience.evidence_ids == ("E-SPC01-001",)
    assert memory.records[0]["source_id"] == experience.experience_id
    assert memory.records[0]["provenance"]["type"] == "outcome_feedback"

    candidate = learning.propose_candidate(
        experience,
        dataset_version="spc01-fixture-v1",
        hypothesis="bounded specialist feedback improves the reusable procedure",
    )
    evaluation = learning.evaluate(
        candidate,
        metric="fixture_validation",
        score=0.95,
        threshold=0.8,
        evaluator="github-actions-spc01",
    )
    assert candidate.state == "CANDIDATE"

    decision = _gate_decision()
    assert decision.classification is EvolutionClassification.COMPATIBLE
    assert decision.canonical_mutation_allowed is False

    package = learning.prepare_knowledge_promotion(
        learning_id=candidate.candidate_id,
        knowledge_key="operations.bounded-specialist-procedure",
        title="Bounded specialist procedure",
        concept="evidence-first specialist feedback",
        provenance={"candidate_id": candidate.candidate_id, "feedback_id": feedback.feedback_id},
        scope="tenant-lab/operations",
        evidence_refs=("E-SPC01-001", "E-SPC01-002"),
        confidence=evaluation.score,
        evolution_decision=decision,
        faculty_relevant=False,
    )
    assert package.status == "PROMOTABLE_KNOWLEDGE"
    assert package.payload["source_learning_id"] == candidate.candidate_id


def test_spc01_promotion_requires_human_approval_and_feedback_is_append_only():
    resolution = _resolve_specialist()
    feedback_registry = SpecialistFeedbackRegistry()
    feedback = SpecialistFeedback(
        feedback_id="FB-SPC01-002",
        specialist_id=resolution.skill_id,
        tenant_id="tenant-lab",
        domain="operations",
        source_reference="fixture://spc01-recovery",
        observation="Recovery remained inside the declared boundary",
        evidence_ids=("E-SPC01-003",),
        provenance={"environment": "github-actions", "kind": "lab-fixture"},
    )
    feedback_registry.ingest(feedback)
    with pytest.raises(ValueError, match="historical feedback is immutable"):
        feedback_registry.ingest(feedback)

    memory = RecordingMemory()
    learning = GovernedLearningService(memory)
    experience = learning.capture_outcome(
        tenant_id="tenant-lab",
        domain="operations",
        principal_id="spc01-lab-principal",
        decision_id="D-SPC01-002",
        expected_outcome="bounded recovery",
        observed_outcome=feedback.observation,
        evidence_ids=feedback.evidence_ids,
    )
    candidate = learning.propose_candidate(
        experience,
        dataset_version="spc01-fixture-v1",
        hypothesis="recovery feedback is reusable only after governed validation",
    )
    evaluation = learning.evaluate(
        candidate, metric="fixture_validation", score=0.9, threshold=0.8, evaluator="github-actions-spc01"
    )
    with pytest.raises(LearningGovernanceError, match="human approval is required"):
        learning.approve_for_promotion(candidate, evaluation, human_approved=False)
    assert candidate.state == "CANDIDATE"
