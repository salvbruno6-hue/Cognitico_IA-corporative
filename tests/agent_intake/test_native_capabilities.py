from elo.agent_intake.native_capabilities import CAPABILITY_IDS, execute_candidate


def test_all_eight_candidates_execute_natively_without_hermes():
    results = [
        execute_candidate(candidate, request_id=f"native-{index:02d}", tenant_scope="multiteiner")
        for index, candidate in enumerate(CAPABILITY_IDS, 1)
    ]
    assert len(results) == 8
    assert {result.capability_id for result in results} == set(CAPABILITY_IDS)
    assert all(result.status == "completed" for result in results)
    assert all(result.evidence for result in results)
    assert all(all(result.outcome.values()) for result in results)


def test_native_execution_never_promotes_or_mutates_canonical_knowledge():
    for index, candidate in enumerate(CAPABILITY_IDS, 1):
        result = execute_candidate(candidate, request_id=f"safety-{index:02d}", tenant_scope="multiteiner")
        assert result.learning_candidate["promotion_state"] == "candidate_only"
        assert result.learning_candidate["canonical_mutation"] is False


def test_native_runtime_keeps_tenant_state_isolated():
    from elo.agent_intake.native_capabilities import NativeELORuntime

    runtime = NativeELORuntime()
    runtime.memory("tenant-a", "probe", "A", write=True)
    runtime.memory("tenant-b", "probe", "B", write=True)
    assert runtime.memory("tenant-a", "probe") == "A"
    assert runtime.memory("tenant-b", "probe") == "B"
