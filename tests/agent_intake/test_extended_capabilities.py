from __future__ import annotations

from elo.agent_intake.extended_capabilities import (
    EXTENSIONS,
    extend_capability,
    extension_is_eligible_for_test,
    measure_evolution,
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


def test_positive_evolution_requires_gain_and_repeatability_without_regression():
    candidate = extend_capability(
        "EXT-MEM-HERMES",
        {"controlled_test": True, "outcome": {"retrieval": True}},
    )
    measurement = measure_evolution(
        candidate,
        {"retrieval_accuracy": 0.70, "context_recall": 0.60},
        {"retrieval_accuracy": 0.82, "context_recall": 0.66},
        repeatable=True,
    )
    assert measurement.result == "STRENGTHEN"
    assert measurement.measured_gain == {
        "retrieval_accuracy": 0.12,
        "context_recall": 0.06,
    }
    assert candidate.promotion_state == "candidate_only"
    assert candidate.canonical_mutation is False


def test_regression_rejects_even_when_another_metric_improves():
    candidate = extend_capability(
        "EXT-MEM-OPENCLAW",
        {"controlled_test": True, "outcome": {"retrieval": True}},
    )
    measurement = measure_evolution(
        candidate,
        {"relevance": 0.70, "cost_efficiency": 0.80},
        {"relevance": 0.90, "cost_efficiency": 0.75},
        regressions=("cost_efficiency",),
        repeatable=True,
    )
    assert measurement.result == "REJECT"
    assert measurement.measured_gain == {"relevance": 0.20}


def test_non_repeatable_gain_requires_retest():
    candidate = extend_capability(
        "EXT-SKILL-OPENCLAW",
        {"controlled_test": True, "outcome": {"execution": True}},
    )
    measurement = measure_evolution(
        candidate,
        {"execution_success": 0.80},
        {"execution_success": 0.90},
        repeatable=False,
    )
    assert measurement.result == "RETEST"


def test_unverified_reference_cannot_produce_positive_evolution():
    candidate = extend_capability("EXT-CONTEXT-HERMES", {"source_reference": True})
    measurement = measure_evolution(
        candidate,
        {"context_relevance": 0.70},
        {"context_relevance": 0.95},
        repeatable=True,
    )
    assert measurement.result == "REJECT"
    assert measurement.measured_gain == {}
