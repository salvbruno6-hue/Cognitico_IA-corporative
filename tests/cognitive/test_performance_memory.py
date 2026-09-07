from elo.cognitive.routing.performance_memory import ExecutionSignature, PerformanceMemory, PerformanceObservation


def test_performance_memory_aggregates_quality_and_outcome_per_signature():
    memory = PerformanceMemory()
    signature = ExecutionSignature(
        mission_type="budget",
        specialist_id="budget-specialist",
        model_id="fake:test-model",
        tool_ids=("calculator",),
        context_profile="budget-v1",
        method_id="decompose-validate-calculate",
    )
    memory.record(
        PerformanceObservation(
            observation_id="o1",
            tenant_id="tenant-a",
            signature=signature,
            result_status="completed",
            quality_score=0.8,
            outcome_score=1.0,
            evidence_ids=("e1",),
        )
    )
    memory.record(
        PerformanceObservation(
            observation_id="o2",
            tenant_id="tenant-a",
            signature=signature,
            result_status="completed",
            quality_score=1.0,
            outcome_score=0.6,
            evidence_ids=("e2",),
        )
    )
    summary = memory.summarize("tenant-a", "budget")
    assert summary[signature] == 0.85


def test_performance_memory_does_not_cross_tenants():
    memory = PerformanceMemory()
    signature = ExecutionSignature("budget", "specialist", "fake:model")
    memory.record(
        PerformanceObservation("a", "tenant-a", signature, "completed", quality_score=1.0)
    )
    memory.record(
        PerformanceObservation("b", "tenant-b", signature, "completed", quality_score=0.0)
    )
    assert len(memory.list_for_mission("tenant-a", "budget")) == 1
    assert len(memory.list_for_mission("tenant-b", "budget")) == 1
