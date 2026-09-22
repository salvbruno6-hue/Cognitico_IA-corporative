import pytest

from elo.core.evolution_gate import EvolutionClassification
from elo.cognitive.symbiont_pattern_intake import ExternalPatternInput, SkillComponent, SymbiontPatternIntake


def pattern(**overrides):
    values = {
        "pattern_id": "ext-001",
        "tenant_id": "multiteiner",
        "domain": "architecture",
        "source_ref": "NousResearch/hermes-agent",
        "source_commit": "abc123",
        "problem": "repeatable operational capability",
        "mechanism": "on-demand skill with bounded provenance",
        "evidence_ids": ("ev-001",),
    }
    values.update(overrides)
    return ExternalPatternInput(**values)


def test_existing_owner_is_reuse_and_cannot_create_candidate():
    decision = SymbiontPatternIntake().classify(
        pattern(existing_owner="ELO Cognitive")
    )

    assert decision.classification is EvolutionClassification.DUPLICATE_SUPERSEDED
    assert decision.disposition == "REUSE"
    assert not decision.candidate_creation_allowed


def test_external_pattern_enters_lab_candidate_only_after_gate():
    decision = SymbiontPatternIntake().classify(pattern())

    assert decision.classification is EvolutionClassification.COMPATIBLE
    assert decision.disposition == "LAB_CANDIDATE"
    assert decision.candidate_creation_allowed


def test_missing_evidence_is_rejected_before_gate():
    with pytest.raises(ValueError, match="requires evidence"):
        SymbiontPatternIntake().classify(pattern(evidence_ids=()))


def test_pattern_can_be_translated_to_existing_lab_schema():
    observation = SymbiontPatternIntake.to_lab_observation(
        pattern(),
        expected_outcome="improve capability discovery",
        observed_outcome="candidate identified",
        decision_id="decision-001",
        baseline="manual discovery",
        experiment="compare bounded skill intake",
        result="candidate is reproducible",
        regression_status="PASS",
        generalization_status="CONFIRMED",
    )

    assert observation.observation_id == "ext-001"
    assert observation.source_ref == "NousResearch/hermes-agent"
    assert observation.source_commit == "abc123"
    assert observation.scope == "symbiont-lab"


def test_skill_assessment_reuses_existing_owner_before_creation():
    assessment = SymbiontPatternIntake().assess_skill_creation(
        proposed_skill_id="ELO-KE-SKILL-EXAMPLE-001",
        existing_owner="ELO Cognitive / Budgeting",
        components=(
            SkillComponent("memory", "FOUND"),
            SkillComponent("precedent_search", "MISSING"),
        ),
    )
    assert assessment.disposition == "REUSE"
    assert assessment.ready_for_intake is False


def test_skill_assessment_requires_base_when_components_are_partial():
    assessment = SymbiontPatternIntake().assess_skill_creation(
        proposed_skill_id="ELO-KE-SKILL-EXAMPLE-001",
        existing_owner=None,
        components=(
            SkillComponent("memory", "FOUND"),
            SkillComponent("precedent_search", "MISSING", gap="develop search"),
            SkillComponent("renderer", "PARTIAL"),
        ),
    )
    assert assessment.disposition == "DEVELOP_FIRST"
    assert assessment.readiness_score == 0.333


def test_skill_assessment_allows_existing_flow_when_components_are_found():
    assessment = SymbiontPatternIntake().assess_skill_creation(
        proposed_skill_id="ELO-KE-SKILL-EXAMPLE-001",
        existing_owner=None,
        components=(
            SkillComponent("memory", "FOUND"),
            SkillComponent("precedent_search", "FOUND"),
            SkillComponent("renderer", "FOUND"),
        ),
    )
    assert assessment.disposition == "READY_FOR_INTAKE"
    assert assessment.ready_for_intake is True
