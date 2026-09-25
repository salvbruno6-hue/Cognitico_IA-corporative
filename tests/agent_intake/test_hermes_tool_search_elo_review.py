"""Integration evidence for the existing ELO Review handoff of tool-search.

This test reuses the existing governed implementation loop. It does not create
a new approval authority and does not authorize canonical mutation.
"""

from elo.agent_intake.hermes_current_extensions import build_candidate
from elo.agent_intake.hermes_governed_loop import (
    ImplementationGovernanceContext,
    advance_to_implementation,
)
from elo.agent_intake.symbiont_adaptation import SymbiontAdaptation
from elo.agent_intake.symbiont_implementation_view import ImplementationOwnership


def _tool_search_adaptation() -> SymbiontAdaptation:
    return SymbiontAdaptation(
        capability_id="HERMES-TOOL-SEARCH",
        existing_capacity="ELO Model/Tool Routing",
        mechanism="progressive tool-schema disclosure",
        adjustment="discover only the relevant tool schema before execution",
        rationale=(
            "Reuse the existing ELO Model/Tool Routing authority.",
            "Keep tool discovery bounded and evidence-driven.",
            "Require Evolution Gate and ELO authorization before implementation.",
        ),
        expected_gain=("reduce representation footprint", "preserve task quality"),
        source_experience=("Hermes: tool_search/progressive tool schemas",),
        evidence_quality="controlled_verified",
    )


def test_tool_search_reaches_existing_elo_review_without_new_authority():
    candidate = build_candidate("EXT-TOOL-SEARCH-HERMES")
    adaptation = _tool_search_adaptation()
    context = ImplementationGovernanceContext(
        functional_branch="evo/elo-review-tool-search-20260925",
        capability="ELO Model/Tool Routing",
        source_ref="EXT-TOOL-SEARCH-HERMES",
        source_commit="447c7cc8430b8d4f8846fe64605e1248050307bf",
        specialization="progressive tool-schema disclosure",
        ownership=ImplementationOwnership.EXTENSION,
        related_contracts=("HERMES_TOOL_SEARCH_REPEATABILITY_2026_09_25",),
        environment="CONTROLLED_TEST",
        evolution_gate_status="REQUIRED",
        governance_status="READY_FOR_ELO_REVIEW",
        runtime_status="NOT_DEPLOYED",
    )
    handoff = advance_to_implementation(
        candidate,
        adaptation,
        {"representation_footprint_chars": 300.0},
        {"representation_footprint_chars": 30.0},
        metric_directions={"representation_footprint_chars": "minimize"},
        repeatable=True,
        regressions=(),
        provenance_refs=(
            "docs/evolution/HERMES_TOOL_SEARCH_2026_09_24.md",
            "docs/evolution/HERMES_TOOL_SEARCH_TASK_QUALITY_2026_09_25.md",
            "docs/evolution/HERMES_TOOL_SEARCH_REPEATABILITY_2026_09_25.md",
        ),
        boundary_integrity=True,
        elo_approved=False,
        evolution_gate_approved=False,
        governance_context=context,
    )

    assert handoff.next_state == "ELO_REVIEW"
    assert handoff.implementation.result == "READY_FOR_ELO_REVIEW"
    assert handoff.implementation.canonical_mutation is False
    assert handoff.canonical_mutation is False
    assert handoff.loop_readiness.ready_for_loop is True
    assert handoff.start_view.candidate_id == "EXT-TOOL-SEARCH-HERMES"
    assert handoff.end_view.end_stage == "ELO_REVIEW"
    assert handoff.end_view.end_result == "READY_FOR_ELO_REVIEW"
