from elo.agent_intake.hermes_code_exec_evaluation import evaluate
from elo.agent_intake.hermes_current_extensions import build_candidate
from elo.agent_intake.implementation_loop import ImplementationStage, run_implementation_loop
from elo.agent_intake.symbiont_adaptation import refine_capability

def test_code_exec_enters_governed_loop_without_promotion():
    result=evaluate()
    candidate=build_candidate("EXT-CODE-EXEC-HERMES")
    adaptation=refine_capability("HERMES-TOOLSETS", {"controlled_test": True, "outcome": {"boundary": True, "provenance": True}})
    decision=run_implementation_loop(
        candidate, adaptation,
        {"boundary_accuracy": result["baseline_rate"]},
        {"boundary_accuracy": result["adapted_rate"]},
        repeatable=result["repeatable"],
        metric_directions={"boundary_accuracy":"maximize"},
    )
    assert decision.stage == ImplementationStage.ELO_REVIEW
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
