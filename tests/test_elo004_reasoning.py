from elo.reasoning import ClaimStatus, EvidenceItem, FindingType
from elo.reasoning.engine import ReasoningEngine
from elo.reasoning.policy import ReasoningPolicyError, validate_reasoning_result


def test_reasoning_requires_evidence_for_supported_claim():
    result = ReasoningEngine().reason("maintenance risk is elevated", evidence=[
        EvidenceItem("e1", "maintenance incidents increased", quality=0.9, relevance=0.9),
    ])
    finding = result.findings[0]
    assert finding.finding_type is FindingType.INFERENCE
    assert finding.status is ClaimStatus.SUPPORTED
    assert "e1" in finding.evidence_refs
    assert result.critiques[0].alternative_hypotheses
    validate_reasoning_result(result)


def test_reasoning_exposes_contradictory_evidence():
    result = ReasoningEngine().reason("the intervention is effective", evidence=[
        EvidenceItem("e1", "cost decreased", quality=0.9, relevance=0.9, supports=True),
        EvidenceItem("e2", "incidents increased", quality=0.9, relevance=0.9, supports=False),
    ])
    finding = result.findings[0]
    assert finding.status is ClaimStatus.PARTIALLY_SUPPORTED
    assert finding.contradictions == ("e2",)
    assert result.critiques[0].recommendation == "REVIEW"


def test_no_evidence_never_becomes_fact():
    result = ReasoningEngine().reason("there is a root cause", evidence=[])
    finding = result.findings[0]
    assert finding.finding_type is FindingType.UNKNOWN
    assert finding.status is ClaimStatus.UNVERIFIED
    assert finding.confidence == 0.0
    assert result.critiques[0].recommendation == "GATHER_EVIDENCE"


def test_policy_rejects_unsupported_high_confidence():
    result = ReasoningEngine().reason("unknown", evidence=[])
    finding = result.findings[0]
    object.__setattr__(finding, "confidence", 0.9)
    try:
        validate_reasoning_result(result)
    except ReasoningPolicyError:
        pass
    else:
        raise AssertionError("policy must reject unsupported high confidence")
