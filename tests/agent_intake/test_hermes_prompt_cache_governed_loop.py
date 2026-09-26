from elo.agent_intake.hermes_current_extensions import build_candidate
from elo.agent_intake.hermes_prompt_cache_evaluation import evaluate
from elo.agent_intake.implementation_loop import ImplementationStage, run_implementation_loop
from elo.agent_intake.symbiont_adaptation import refine_capability

def test_prompt_cache_enters_governed_loop_without_promotion():
    result = evaluate()
    candidate = build_candidate("EXT-PROMPT-CACHE-HERMES")
    adaptation = refine_capability(
        "HERMES-MEMORY",
        {"controlled_test": True, "outcome": {"scope": True, "invalidation": True}},
    )
    decision = run_implementation_loop(
        candidate,
        adaptation,
        {"cache_decision_accuracy": result["baseline_rate"]},
        {"cache_decision_accuracy": result["adapted_rate"]},
        repeatable=result["repeatable"],
        metric_directions={"cache_decision_accuracy": "maximize"},
    )
    assert decision.stage == ImplementationStage.ELO_REVIEW
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
