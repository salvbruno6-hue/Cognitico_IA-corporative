from elo.agent_intake.hermes_current_extensions import build_candidate
from elo.agent_intake.hermes_plugin_catalog_evaluation import evaluate
from elo.agent_intake.implementation_loop import ImplementationStage, run_implementation_loop
from elo.agent_intake.symbiont_adaptation import refine_capability


def test_plugin_catalog_enters_existing_implementation_loop_without_promotion():
    evaluation = evaluate()
    candidate = build_candidate("EXT-PLUGIN-CATALOG-HERMES")
    adaptation = refine_capability(
        "HERMES-TOOLSETS",
        {
            "controlled_test": True,
            "outcome": {"authorization": True, "provenance": True},
        },
    )
    decision = run_implementation_loop(
        candidate,
        adaptation,
        {"authorization_precision": evaluation.baseline_rate},
        {"authorization_precision": evaluation.adapted_rate},
        repeatable=evaluation.repeatable,
        metric_directions={"authorization_precision": "maximize"},
    )
    assert decision.stage == ImplementationStage.ELO_REVIEW
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
