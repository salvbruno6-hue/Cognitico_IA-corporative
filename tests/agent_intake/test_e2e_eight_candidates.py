"""E2E laboratory for the eight ELO capability candidates.

The scenario is deliberately inert: it validates operation, evidence, tenant
isolation, duplicate/authority boundaries, and learning safety without calling
Hermes, changing canonical knowledge, or performing business operations.
"""

from elo.agent_intake.native_capabilities import CAPABILITY_IDS, NativeELORuntime, execute_candidate


TENANT = "multiteiner"
SCENARIO = "lab-pre-budget-administrative-room"

EXPECTED_OPERATIONS = {
    "HERMES-MEMORY": "write_read",
    "HERMES-SKILLS": "skill_execute",
    "HERMES-TOOLSETS": "allowlist_enforced",
    "HERMES-CONTEXT": "precedence",
    "HERMES-DELEGATION": "result_returned",
    "HERMES-AUTOMATION": "registered",
    "HERMES-MCP": "trust_boundary_enforced",
    "HERMES-CHECKPOINT": "restored",
}


def test_e2e_eight_candidates_complete_the_controlled_scenario():
    results = [
        execute_candidate(candidate, request_id=f"{SCENARIO}-{index:02d}", tenant_scope=TENANT)
        for index, candidate in enumerate(CAPABILITY_IDS, 1)
    ]

    assert len(results) == 8
    assert tuple(result.capability_id for result in results) == CAPABILITY_IDS

    for result in results:
        assert result.status == "completed"
        assert result.evidence
        assert all(result.outcome.values())
        assert result.learning_candidate == {
            "promotion_state": "candidate_only",
            "canonical_mutation": False,
        }


def test_e2e_eight_candidates_prove_the_expected_operation_for_each_candidate():
    for index, candidate in enumerate(CAPABILITY_IDS, 1):
        result = execute_candidate(candidate, request_id=f"{SCENARIO}-operation-{index:02d}", tenant_scope=TENANT)
        evidence = result.evidence[0]
        operation = evidence.get("operation")
        if operation is not None:
            assert operation == EXPECTED_OPERATIONS[candidate]
        assert any(result.outcome.values())


def test_e2e_duplicate_and_authority_boundary_is_preserved():
    runtime = NativeELORuntime()

    runtime.memory("tenant-a", "shared-probe", "A", write=True)
    runtime.memory("tenant-b", "shared-probe", "B", write=True)
    assert runtime.memory("tenant-a", "shared-probe") == "A"
    assert runtime.memory("tenant-b", "shared-probe") == "B"

    runtime.register_toolset(TENANT, "lab-tools", ("read",))
    assert runtime.resolve_tool(TENANT, "lab-tools", "read") is True
    assert runtime.resolve_tool(TENANT, "lab-tools", "write") is False


def test_e2e_checkpoint_restore_is_scoped_and_noncanonical():
    runtime = NativeELORuntime()
    state = {"scenario": SCENARIO, "canonical_mutation": False}

    snapshot = runtime.checkpoint(TENANT, "lab-checkpoint", state)
    restored = runtime.restore(TENANT, "lab-checkpoint")

    assert snapshot == state
    assert restored == state
    assert restored["canonical_mutation"] is False


def test_e2e_context_and_delegation_remain_local_to_the_controlled_lab():
    runtime = NativeELORuntime()
    context = runtime.assemble_context(
        {"domain": "commercial", "shared": "parent"},
        {"scenario": SCENARIO, "shared": "child"},
    )
    assert context["domain"] == "commercial"
    assert context["scenario"] == SCENARIO
    assert context["shared"] == "child"

    delegated = runtime.delegate(
        TENANT,
        lambda payload: {"scenario": payload["scenario"]},
        {"scenario": SCENARIO},
    )
    assert delegated == {"tenant_scope": TENANT, "result": {"scenario": SCENARIO}}


def test_e2e_candidate_set_has_no_duplicate_capability_ids():
    assert len(CAPABILITY_IDS) == 8
    assert len(set(CAPABILITY_IDS)) == len(CAPABILITY_IDS)
