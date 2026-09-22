import pytest

from src.elo.learning.evolution_gate import (
    Evidence,
    EvolutionGate,
    GateDecision,
    GateInput,
)


def passing_input(**overrides):
    data = dict(
        experience_id="exp-1",
        pattern_id="pattern-1",
        evidence=[
            Evidence("ev-1", source="SO-001.26", kind="EXPERIENCE"),
            Evidence("ev-2", source="test-suite", kind="TEST"),
        ],
        test_result="PASS",
        regression_passed=True,
        reproducible=True,
        confidence=0.9,
        applicability="escopo validado",
    )
    data.update(overrides)
    return GateInput(**data)


class TestEvolutionGate:
    def test_requests_more_evidence_when_insufficient(self):
        result = EvolutionGate().evaluate(
            GateInput(evidence=[Evidence("ev-1", "source-a")])
        )
        assert result.decision == GateDecision.SOLICITAR_MAIS_EVIDENCIA

    def test_duplicate_source_evidence_does_not_fake_independence(self):
        result = EvolutionGate().evaluate(
            passing_input(
                evidence=[
                    Evidence("ev-1", "same-source", independent_key="case-1"),
                    Evidence("ev-2", "same-source", independent_key="case-1"),
                ]
            )
        )
        assert result.decision == GateDecision.SOLICITAR_MAIS_EVIDENCIA

    def test_rejects_contradiction(self):
        result = EvolutionGate().evaluate(passing_input(contradictions=["rule-1"]))
        assert result.decision == GateDecision.REJEITAR

    def test_replans_duplicates(self):
        result = EvolutionGate().evaluate(passing_input(duplicates=["concept-1"]))
        assert result.decision == GateDecision.REPLAN

    @pytest.mark.parametrize("test_result", ["FAIL", "PARTIAL", None])
    def test_retains_without_approved_test(self, test_result):
        result = EvolutionGate().evaluate(passing_input(test_result=test_result))
        assert result.decision == GateDecision.RETER

    def test_retains_without_regression(self):
        result = EvolutionGate().evaluate(passing_input(regression_passed=False))
        assert result.decision == GateDecision.RETER

    def test_requests_more_evidence_when_not_reproducible(self):
        result = EvolutionGate().evaluate(passing_input(reproducible=False))
        assert result.decision == GateDecision.SOLICITAR_MAIS_EVIDENCIA

    def test_retains_below_confidence_threshold(self):
        result = EvolutionGate().evaluate(passing_input(confidence=0.69))
        assert result.decision == GateDecision.RETER

    def test_requests_scope_when_applicability_is_missing(self):
        result = EvolutionGate().evaluate(passing_input(applicability=None))
        assert result.decision == GateDecision.SOLICITAR_MAIS_EVIDENCIA

    def test_promotes_when_all_gate_criteria_are_met(self):
        result = EvolutionGate().evaluate(passing_input())

        assert result.decision == GateDecision.PROMOVER
        assert result.from_level == "VALIDATED"
        assert result.to_level == "CONSOLIDATED"
        assert result.experience_id == "exp-1"
        assert result.pattern_id == "pattern-1"
        assert len(result.evidence_used) == 2

    def test_legacy_string_evidence_remains_supported(self):
        result = EvolutionGate().evaluate(passing_input(evidence=["e1", "e2"]))
        assert result.decision == GateDecision.PROMOVER

    def test_rejects_invalid_confidence(self):
        result = EvolutionGate().evaluate(passing_input(confidence=1.1))
        assert result.decision == GateDecision.REPLAN

    def test_event_payload_preserves_source_ids(self):
        result = EvolutionGate().evaluate(passing_input())
        payload = result.to_evolution_event()

        assert payload["source_experience_id"] == "exp-1"
        assert payload["source_pattern_id"] == "pattern-1"
        assert payload["event_type"] == "PROMOVER"
        assert payload["from_level"] == "VALIDATED"
        assert payload["to_level"] == "CONSOLIDATED"
        assert payload["confidence"] == 0.9
