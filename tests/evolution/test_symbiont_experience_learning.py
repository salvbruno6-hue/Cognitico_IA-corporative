from elo.core.learning_governance import ExperienceRecord
from elo.cognitive.symbiont_experience_learning import (
    LearningTrigger,
    detect_learning_trigger,
    trigger_learning,
)


class MemoryStub:
    def remember(self, **kwargs):
        return None


class ServiceStub:
    def propose_candidate(self, experience, *, dataset_version, hypothesis):
        return type(
            "Candidate",
            (),
            {
                "candidate_id": "learning-1",
                "experience_id": experience.experience_id,
                "state": "CANDIDATE",
                "hypothesis": hypothesis,
            },
        )()


def experience(evidence=("e1",)):
    return ExperienceRecord(
        experience_id="exp-1",
        tenant_id="tenant-a",
        domain="elo",
        decision_id="decision-1",
        expected_outcome="expected",
        observed_outcome="observed",
        evidence_ids=evidence,
        captured_at=1.0,
    )


def test_positive_experience_creates_learning_candidate():
    signal = trigger_learning(
        ServiceStub(),
        experience=experience(),
        dataset_version="v1",
    )
    assert signal.trigger is LearningTrigger.POSITIVE_GAIN
    assert signal.action == "RETAIN_AND_TEST"
    assert signal.learning_candidate is not None
    assert not signal.canonical_mutation
    assert not signal.authorization_granted


def test_repeated_experience_aggregates_before_reuse():
    signal = trigger_learning(
        ServiceStub(),
        experience=experience(),
        dataset_version="v1",
        repeated=True,
    )
    assert signal.trigger is LearningTrigger.REPEATED_OUTCOME
    assert signal.action == "AGGREGATE_EXPERIENCE"
    assert signal.learning_candidate is not None


def test_regression_creates_bounded_correction_candidate():
    signal = trigger_learning(
        ServiceStub(),
        experience=experience(),
        dataset_version="v1",
        regression=True,
    )
    assert signal.trigger is LearningTrigger.REGRESSION
    assert signal.action == "DIAGNOSE_AND_CORRECT"
    assert signal.learning_candidate is not None


def test_boundary_violation_never_becomes_learning_candidate():
    signal = trigger_learning(
        ServiceStub(),
        experience=experience(),
        dataset_version="v1",
        boundary_violation=True,
    )
    assert signal.trigger is LearningTrigger.BOUNDARY_VIOLATION
    assert signal.learning_candidate is None


def test_missing_evidence_never_becomes_learning_candidate():
    signal = trigger_learning(
        ServiceStub(),
        experience=experience(evidence=()),
        dataset_version="v1",
        evidence_complete=False,
    )
    assert signal.trigger is LearningTrigger.MISSING_EVIDENCE
    assert signal.learning_candidate is None


def test_trigger_priority_is_deterministic():
    assert detect_learning_trigger(
        experience=experience(evidence=()),
        repeated=True,
        regression=True,
        boundary_violation=True,
        evidence_complete=False,
    ) is LearningTrigger.MISSING_EVIDENCE

    assert detect_learning_trigger(
        experience=experience(),
        repeated=True,
        regression=True,
        boundary_violation=True,
    ) is LearningTrigger.BOUNDARY_VIOLATION
