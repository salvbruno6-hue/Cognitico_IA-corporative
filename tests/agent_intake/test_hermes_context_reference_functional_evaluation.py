from src.elo.agent_intake.hermes_context_reference_functional_adapter import admit_message
from src.elo.agent_intake.hermes_context_reference_functional_evaluation import evaluate


def test_malformed_context_references_are_rejected():
    assert admit_message("@file:README.md:20-10")[0].accepted is False
    assert admit_message("@file:README.md:0-4")[0].accepted is False


def test_valid_context_references_remain_admissible():
    assert admit_message("@file:README.md:10-20")[0].accepted is True
    assert admit_message("@folder:src/elo")[0].accepted is True


def test_contextref_functional_gain_is_repeatable_and_gate_bounded():
    result = evaluate()
    assert result.baseline_unsafe_admission_rate == 0.4
    assert result.adapted_unsafe_admission_rate == 0.0
    assert result.repeatable is True
    assert result.boundary_integrity_rate == 1.0
    assert result.result == "EVOLUTION_GATE_REQUIRED"
