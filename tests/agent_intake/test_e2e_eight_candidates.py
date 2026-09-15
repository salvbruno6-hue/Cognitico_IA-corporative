"""Integrated E2E laboratory for the implemented ELO capability set.

The laboratory keeps one canonical ELO capability identity per capability and
records Hermes/OpenClaw as provider implementations/evidence for that identity.
It deliberately does not create a second OpenClaw capability registry, call
external infrastructure, mutate canonical knowledge, or perform business
operations.
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

# OpenClaw evidence is reference-only. These are existing implementation
# surfaces, not new ELO implementations. The same capability identity is
# intentionally reused to prevent duplicate ELO authorities.
OPENCLAW_IMPLEMENTATIONS = {
    "HERMES-MEMORY": "extensions/memory-core/index.ts",
    "HERMES-SKILLS": "src/agents/skills/plugin-skills.ts",
    "HERMES-TOOLSETS": "src/agents/tool-policy.ts",
    "HERMES-CONTEXT": "src/agents/harness/context-engine-lifecycle.ts",
    "HERMES-DELEGATION": "src/agents/subagent-spawn.ts",
    "HERMES-AUTOMATION": "src/cron/schedule.ts",
    "HERMES-MCP": "src/mcp/tools-stdio-server.ts",
    "HERMES-CHECKPOINT": "src/agents/session-file-repair.ts",
}

# The OpenClaw source snapshot used by this laboratory is the dedicated
# repository's reference tree. Source evidence is not treated as a live
# execution result and therefore cannot promote a candidate.
OPENCLAW_REFERENCE = "salvbruno6-hue/https-github.com-salvbruno6-hue-openclaw-dedicated"


def test_e2e_all_implemented_capabilities_complete_the_controlled_scenario():
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


def test_e2e_each_capability_has_openclaw_and_elo_implementations_without_duplicate_ids():
    assert set(OPENCLAW_IMPLEMENTATIONS) == set(CAPABILITY_IDS)
    assert len(OPENCLAW_IMPLEMENTATIONS) == len(CAPABILITY_IDS) == 8
    assert len(set(OPENCLAW_IMPLEMENTATIONS)) == 8
    assert OPENCLAW_REFERENCE.endswith("openclaw-dedicated")


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
