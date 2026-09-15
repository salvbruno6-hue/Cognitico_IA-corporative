from __future__ import annotations

from elo.agent_intake.extended_capabilities import (
    EXTENSIONS,
    extend_capability,
    extension_is_eligible_for_test,
)

EXPECTED_OWNERS = {
    "EXT-MEM-HERMES": "ELO Memory",
    "EXT-MEM-OPENCLAW": "ELO Memory",
    "EXT-SKILL-HERMES": "ELO Skills",
    "EXT-SKILL-OPENCLAW": "ELO Skills",
    "EXT-TOOL-HERMES": "ELO Toolset Resolution",
    "EXT-TOOL-OPENCLAW": "ELO Toolset Resolution",
    "EXT-CONTEXT-HERMES": "ELO Context",
    "EXT-CONTEXT-OPENCLAW": "ELO Context",
    "EXT-DELEG-HERMES": "ELO Delegation",
    "EXT-DELEG-OPENCLAW": "ELO Delegation",
    "EXT-AUTO-HERMES": "ELO Automation",
    "EXT-AUTO-OPENCLAW": "ELO Automation",
    "EXT-MCP-HERMES": "ELO External Capability Gateway",
    "EXT-MCP-OPENCLAW": "ELO External Capability Gateway",
    "EXT-STATE-HERMES": "ELO State Recovery",
    "EXT-STATE-OPENCLAW": "ELO State Recovery",
}


def test_all_extensions_attach_to_existing_elo_capacity():
    assert len(EXTENSIONS) == 16
    assert {row[0] for row in EXTENSIONS} == set(EXPECTED_OWNERS)
    for extension_id, expected_owner in EXPECTED_OWNERS.items():
        candidate = extend_capability(extension_id, {"source_reference": True})
        assert candidate.extends_capability == expected_owner
        assert candidate.adapted is True
        assert candidate.promotion_state == "candidate_only"
        assert candidate.canonical_mutation is False
        assert extension_is_eligible_for_test(candidate) is False


def test_both_providers_extend_the_same_owner_without_creating_parallel_capability():
    by_owner: dict[str, set[str]] = {}
    for extension_id, provider, owner, _mechanism in EXTENSIONS:
        by_owner.setdefault(owner, set()).add(provider)
    assert by_owner == {
        "ELO Memory": {"Hermes", "OpenClaw"},
        "ELO Skills": {"Hermes", "OpenClaw"},
        "ELO Toolset Resolution": {"Hermes", "OpenClaw"},
        "ELO Context": {"Hermes", "OpenClaw"},
        "ELO Delegation": {"Hermes", "OpenClaw"},
        "ELO Automation": {"Hermes", "OpenClaw"},
        "ELO External Capability Gateway": {"Hermes", "OpenClaw"},
        "ELO State Recovery": {"Hermes", "OpenClaw"},
    }


def test_only_measured_outcomes_can_enter_refinement_test():
    controlled = extend_capability(
        "EXT-MEM-OPENCLAW",
        {"controlled_test": True, "outcome": {"retrieval": True}},
    )
    assert controlled.evidence_quality == "controlled_verified"
    assert extension_is_eligible_for_test(controlled) is True

    no_outcome = extend_capability("EXT-MEM-OPENCLAW", {"controlled_test": True})
    assert no_outcome.evidence_quality == "insufficient"
    assert extension_is_eligible_for_test(no_outcome) is False

    live = extend_capability(
        "EXT-MEM-OPENCLAW",
        {"live_execution": True, "outcome": {"retrieval": True}},
    )
    assert live.evidence_quality == "execution_verified"
    assert extension_is_eligible_for_test(live) is True
