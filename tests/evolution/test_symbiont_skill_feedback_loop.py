from elo.core.learning_governance import ExperienceRecord
from elo.cognitive.symbiont_experience_learning import LearningTrigger
from elo.cognitive.symbiont_skill_feedback_loop import (
    SkillExecutionContext,
    observe_skill_batch,
    observe_skill_outcome,
)


class ServiceStub:
    def __init__(self):
        self.captured = []

    def capture_outcome(self, **kwargs):
        self.captured.append(kwargs)
        return ExperienceRecord(
            experience_id=f"exp-{len(self.captured)}",
            tenant_id=kwargs["tenant_id"],
            domain=kwargs["domain"],
            decision_id=kwargs["decision_id"],
            expected_outcome=kwargs["expected_outcome"],
            observed_outcome=kwargs["observed_outcome"],
            evidence_ids=tuple(kwargs["evidence_ids"]),
            captured_at=1.0,
        )

    def propose_candidate(self, experience, *, dataset_version, hypothesis):
        return type(
            "Candidate",
            (),
            {
                "candidate_id": f"candidate-{experience.experience_id}",
                "experience_id": experience.experience_id,
                "state": "CANDIDATE",
                "hypothesis": hypothesis,
            },
        )()


def context(*, skill_id="EXT-LEARN-HERMES", evidence=("e1",)):
    return SkillExecutionContext(
        skill_id=skill_id,
        tenant_id="tenant-a",
        domain="FORGE",
        principal_id="symbiont-test",
        decision_id=f"decision-{skill_id}",
        expected_outcome="skill outcome improves decision",
        observed_outcome="skill outcome improved decision",
        evidence_ids=evidence,
        dataset_version="test-v1",
    )


def test_skill_outcome_enters_experience_trigger_loop():
    service = ServiceStub()
    feedback = observe_skill_outcome(service, context())

    assert feedback.skill_id == "EXT-LEARN-HERMES"
    assert feedback.experience.tenant_id == "tenant-a"
    assert feedback.experience.domain == "FORGE"
    assert feedback.trigger is LearningTrigger.POSITIVE_GAIN
    assert feedback.learning_candidate is not None
    assert not feedback.canonical_mutation
    assert not feedback.authorization_granted


def test_regression_becomes_bounded_correction():
    feedback = observe_skill_outcome(
        ServiceStub(),
        context(skill_id="EXT-ROUTE-HERMES"),
        regression=True,
    )

    assert feedback.trigger is LearningTrigger.REGRESSION
    assert feedback.signal.action == "DIAGNOSE_AND_CORRECT"
    assert feedback.learning_candidate is not None


def test_missing_evidence_blocks_learning():
    feedback = observe_skill_outcome(
        ServiceStub(),
        context(skill_id="EXT-MEMPROVIDER-HERMES", evidence=()),
        evidence_complete=False,
    )

    assert feedback.trigger is LearningTrigger.MISSING_EVIDENCE
    assert feedback.learning_candidate is None


def test_boundary_violation_blocks_learning():
    feedback = observe_skill_outcome(
        ServiceStub(),
        context(skill_id="EXT-HOOK-HERMES"),
        boundary_violation=True,
    )

    assert feedback.trigger is LearningTrigger.BOUNDARY_VIOLATION
    assert feedback.learning_candidate is None


def test_batch_applies_same_contract_to_multiple_skills():
    service = ServiceStub()
    feedback = observe_skill_batch(
        service,
        (
            context(skill_id="EXT-CONTEXT-PLUGIN-HERMES"),
            context(skill_id="EXT-WORKTREE-HERMES"),
            context(skill_id="EXT-MULTIAGENT-HERMES"),
        ),
        repeated_skill_ids=frozenset({"EXT-WORKTREE-HERMES"}),
        regression_skill_ids=frozenset({"EXT-MULTIAGENT-HERMES"}),
    )

    assert tuple(item.skill_id for item in feedback) == (
        "EXT-CONTEXT-PLUGIN-HERMES",
        "EXT-WORKTREE-HERMES",
        "EXT-MULTIAGENT-HERMES",
    )
    assert feedback[0].trigger is LearningTrigger.POSITIVE_GAIN
    assert feedback[1].trigger is LearningTrigger.REPEATED_OUTCOME
    assert feedback[2].trigger is LearningTrigger.REGRESSION
    assert len(service.captured) == 3
