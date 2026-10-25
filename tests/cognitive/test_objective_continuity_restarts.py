from __future__ import annotations

from elo.cognitive.objective_continuity import ObjectiveContinuityAdapter, ObjectiveLoopDecision
from elo.cognitive.symbiont_execution import SymbiontExecutionStore
from elo.contracts.okr import Objective


def test_repetitive_flow_completes_across_restart_on_every_cycle(tmp_path) -> None:
    path = str(tmp_path / "repeatable-objective.sqlite")
    obj = Objective(
        tenant_id="tenant-repeat",
        objective_id="obj-six-batches",
        title="Concluir seis lotes sem perder o objetivo",
        owner_ref="elo-cognitivo",
        evidence_refs=("evidence://objective/six-batches",),
    )

    final = None
    execution_id = None
    for batch in range(1, 7):
        store = SymbiontExecutionStore(path)
        adapter = ObjectiveContinuityAdapter(store)
        checkpoint = adapter.start_or_resume(
            obj,
            workstream_id="production-batches",
            initial_action="PROCESS_BATCH",
            max_cycles=10,
        )
        if execution_id is None:
            execution_id = checkpoint.execution_id
        else:
            assert checkpoint.execution_id == execution_id
        if batch > 1:
            assert checkpoint.last_progress_token == f"batch:{batch - 1}"

        final = adapter.record_cycle(
            obj,
            workstream_id="production-batches",
            expected_state_version=checkpoint.state_version,
            progress_token=f"batch:{batch}",
            evidence_refs=(f"evidence://batch/{batch}",),
            proposed_next_action="PROCESS_BATCH",
            objective_satisfied=batch == 6,
        )
        store.close()

    assert final is not None
    assert final.decision is ObjectiveLoopDecision.COMPLETE
    assert final.checkpoint.status == "COMPLETED"
    assert final.checkpoint.last_progress_token == "batch:6"
    assert final.checkpoint.no_progress_streak == 0
