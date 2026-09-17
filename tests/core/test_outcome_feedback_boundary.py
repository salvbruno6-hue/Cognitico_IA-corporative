from datetime import datetime, timezone

from elo.core.outcome_feedback import OutcomeFeedback as OperationalOutcomeFeedback
from elo.core.outcome_feedback_boundary import (
    translate_outcome_feedback,
    to_systemic_outcome_feedback,
)


def test_translation_preserves_operational_feedback_and_evidence():
    operational = OperationalOutcomeFeedback(
        decision_id="decision-001",
        outcome_id="outcome-001",
        expected="action completes",
        observed="action completed",
        assessment="success",
        evidence_ids=("evidence-001", "evidence-002"),
    )

    observed_at = datetime(2026, 9, 16, 21, 0, tzinfo=timezone.utc)
    translated = translate_outcome_feedback(
        operational,
        variance="none observed",
        observed_at=observed_at,
    )

    assert translated.operational == operational
    assert translated.systemic.decision_id == operational.decision_id
    assert translated.systemic.expected == operational.expected
    assert translated.systemic.observed == operational.observed
    assert translated.systemic.variance == "none observed"
    assert translated.systemic.evidence_ids == operational.evidence_ids
    assert translated.systemic.observed_at == observed_at


def test_translation_does_not_infer_variance_from_assessment():
    operational = OperationalOutcomeFeedback(
        decision_id="decision-002",
        outcome_id="outcome-002",
        expected="action completes",
        observed="action completed",
        assessment="success",
    )

    systemic = to_systemic_outcome_feedback(operational)

    assert systemic.variance is None
    assert systemic.decision_id == operational.decision_id


def test_translation_is_non_mutating():
    operational = OperationalOutcomeFeedback(
        decision_id="decision-003",
        outcome_id="outcome-003",
        expected="target",
        observed="result",
        assessment="partial",
        evidence_ids=("evidence-003",),
    )

    systemic = to_systemic_outcome_feedback(operational, variance="partial deviation")

    assert operational.outcome_id == "outcome-003"
    assert operational.assessment == "partial"
    assert operational.evidence_ids == ("evidence-003",)
    assert systemic.evidence_ids == operational.evidence_ids
