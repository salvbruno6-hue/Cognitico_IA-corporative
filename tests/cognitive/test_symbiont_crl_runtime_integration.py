from __future__ import annotations

from elo.cognitive.runtime.crl import CRLContext, CognitiveRuntimeLoop, Stage
from elo.cognitive.runtime.symbiont_checkpoint import checkpoint_for_crl
from elo.cognitive.symbiont_execution import SymbiontExecutionStore


def test_crl_can_project_existing_symbiont_checkpoint_without_new_stage() -> None:
    store = SymbiontExecutionStore()
    store.create_execution(
        execution_id="runtime-checkpoint-1",
        candidate_id="candidate-1",
        capability_id="capability-1",
        owner="elo-cognitive",
        current_stage="ANALYZE",
        next_action="RUN_ANALYSIS",
    )

    captured = {}

    def analyze(ctx: CRLContext) -> CRLContext:
        captured["checkpoint"] = checkpoint_for_crl(store, "runtime-checkpoint-1")
        return ctx

    crl = CognitiveRuntimeLoop()
    crl.register(Stage.ANALYZE, analyze)

    context = crl.run(CRLContext(request_id="runtime-checkpoint-1"))

    checkpoint = captured["checkpoint"]
    assert checkpoint.execution_id == context.request_id
    assert checkpoint.stage == "ANALYZE"
    assert checkpoint.next_action == "RUN_ANALYSIS"
    assert [item["stage"] for item in context.audit].count("analyze") == 1
    assert all(stage in {s.value for s in CognitiveRuntimeLoop.STAGES_ORDER} for stage in [item["stage"] for item in context.audit])
