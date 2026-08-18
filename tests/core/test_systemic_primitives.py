import pytest

from elo.core.systemic_primitives import (
    CausalAssessment,
    DecisionRecord,
    OutcomeFeedback,
    Scenario,
    SystemicModel,
    SystemicRelation,
    TemporalValidity,
    UncertaintyAssessment,
)


def test_systemic_model_preserves_evidence_backed_relations():
    relation = SystemicRelation("demand", "drives", "capacity", ("e1",), 0.8)
    model = SystemicModel(("demand", "capacity"), (relation,), ("e1",))
    assert model.relations[0].evidence_ids == ("e1",)


def test_causal_assessment_requires_bounded_confidence():
    with pytest.raises(ValueError):
        CausalAssessment("a", "b", 1.2)


def test_decision_record_keeps_rationale_and_authority_separate():
    decision = DecisionRecord("d1", "replan", "capacity gap", authority="manager")
    assert decision.authority == "manager"
    assert decision.rationale == "capacity gap"


def test_outcome_feedback_compares_expected_and_observed():
    feedback = OutcomeFeedback("d1", "deliver 100", "deliver 82", "-18", ("e2",))
    assert feedback.variance == "-18"


def test_temporal_validity_rejects_inverted_window():
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    with pytest.raises(ValueError):
        TemporalValidity(now, now - timedelta(days=1))


def test_uncertainty_and_scenario_are_non_executing_values():
    uncertainty = UncertaintyAssessment(0.6, "MEDIUM", ("e3",))
    scenario = Scenario("recovery", ("demand stable",), ("reduce backlog",), ("e3",), uncertainty)
    assert scenario.name == "recovery"
    assert scenario.uncertainty.confidence == 0.6
