import pytest

from elo.reasoning.analysis_models import (
    ClaimType,
    EvidenceEvaluation,
    EvidencePolarity,
    Hypothesis,
    InformationGap,
    Scenario,
)
from elo.reasoning.stage_services import (
    ConsultingService,
    CritiqueService,
    DecisionSupportService,
    EvidenceEvaluator,
)


def test_evidence_evaluation_clamps_relevance_and_preserves_provenance():
    result = EvidenceEvaluator().evaluate(
        evidence_id="e1", claim_id="c1", quality="VERIFIED", relevance=1.4,
        supports=True, rationale="supports claim", provenance={"source": "erp"}
    )
    assert result.relevance == 1.0
    assert result.polarity is EvidencePolarity.SUPPORTS
    assert result.provenance["source"] == "erp"


def test_hypothesis_confidence_is_bounded():
    assert Hypothesis("h1", "route contributes", 1.4).confidence == 1.0
    assert Hypothesis("h2", "route contributes", -0.2).confidence == 0.0


def test_critique_reduces_confidence_when_contradicted():
    items = [
        EvidenceEvaluation("e1", "c1", EvidencePolarity.SUPPORTS, "VERIFIED", 0.8, "support"),
        EvidenceEvaluation("e2", "c1", EvidencePolarity.CONTRADICTS, "SUPPORTED", 0.2, "contradiction"),
    ]
    result = CritiqueService().critique("c1", items, ["alternative"], ["missing input"])
    assert result.revised_confidence == pytest.approx(0.6)
    assert result.contradictions == ("contradiction",)
    assert result.missing_information == ("missing input",)


def test_decision_support_requires_human_owner():
    scenario = Scenario("s1", "Keep current", "Maintain operation", ("stable cost",), ("rework",), 0.7)
    with pytest.raises(ValueError, match="decision_owner"):
        DecisionSupportService().build(
            decision_id="d1", problem="p", scenarios=[scenario], recommended_option="s1",
            rationale="best evidence", decision_owner=None, evidence_refs=["e1"], risks=["r1"]
        )


def test_decision_support_rejects_unknown_recommendation():
    scenario = Scenario("s1", "Keep current", "Maintain operation")
    with pytest.raises(ValueError, match="recommended_option"):
        DecisionSupportService().build(
            decision_id="d1", problem="p", scenarios=[scenario], recommended_option="s2",
            rationale="bad reference", decision_owner="manager-1", evidence_refs=["e1"], risks=["r1"]
        )


def test_decision_support_preserves_human_owner_and_options():
    scenario = Scenario("s1", "Keep current", "Maintain operation", ("stable cost",), ("rework",), 0.7)
    result = DecisionSupportService().build(
        decision_id="d1", problem="p", scenarios=[scenario], recommended_option="s1",
        rationale="best evidence", decision_owner="manager-1", evidence_refs=["e1"], risks=["r1"]
    )
    assert result.decision_owner == "manager-1"
    assert result.recommended_option == "s1"
    assert result.alternatives[0].scenario_id == "s1"


def test_consulting_preserves_unknowns_and_information_gaps():
    result = ConsultingService().assess(
        assessment_id="a1", problem="maintenance cost",
        known=["cost increased"], unknown=["root cause"],
        hypotheses=[Hypothesis("h1", "route contributes", 0.5)],
        information_gaps=[InformationGap("g1", "which route", "needed for comparison")],
        recommendations=["collect route telemetry"], risks=["false attribution"]
    )
    assert result.unknown == ("root cause",)
    assert result.information_gaps[0].gap_id == "g1"


def test_claim_types_include_governed_distinctions():
    assert ClaimType.FACT != ClaimType.HYPOTHESIS
    assert ClaimType.RECOMMENDATION != ClaimType.DECISION
