from elo.agent_intake.hermes_current_extensions import build_candidate
from elo.agent_intake.hermes_governed_loop import (
    ImplementationGovernanceContext,
    advance_to_implementation,
)
from elo.agent_intake.symbiont_adaptation import SymbiontAdaptation
from elo.agent_intake.symbiont_implementation_view import ImplementationOwnership


def test_authorized_tool_search_enters_existing_implementation_stage():
    candidate = build_candidate("EXT-TOOL-SEARCH-HERMES")
    adaptation = SymbiontAdaptation(
        capability_id="HERMES-TOOL-SEARCH",
        existing_capacity="ELO Model/Tool Routing",
        mechanism="progressive tool-schema disclosure",
        adjustment="select only the relevant tool schema before execution",
        rationale=(
            "Reuse the existing ELO Model/Tool Routing authority.",
            "Keep disclosure bounded and deterministic.",
        ),
        expected_gain=("reduce representation footprint", "preserve task quality"),
        source_experience=("Hermes: tool_search/progressive tool schemas",),
        evidence_quality="controlled_verified",
    )
    context = ImplementationGovernanceContext(
        functional_branch="feat/implement-tool-search-routing-20260925",
        capability="ELO Model/Tool Routing",
        source_ref="EXT-TOOL-SEARCH-HERMES",
        source_commit="447c7cc8430b8d4f8846fe64605e1248050307bf",
        specialization="progressive tool-schema disclosure",
        ownership=ImplementationOwnership.EXTENSION,
        related_contracts=(
            "HERMES_TOOL_SEARCH_REPEATABILITY_2026_09_25",
            "ELO Review Issue #734",
        ),
        environment="CONTROLLED_TEST",
        evolution_gate_status="APPROVED",
        governance_status="IMPLEMENTATION_AUTHORIZED",
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
            "PR #730",
            "PR #732",
            "PR #733",
            "Issue #734",
        ),
        boundary_integrity=True,
        elo_approved=True,
        evolution_gate_approved=True,
        governance_context=context,
    )

    assert handoff.next_state == "IMPLEMENTATION_AUTHORIZED"
    assert handoff.implementation.result == "IMPLEMENTATION_AUTHORIZED"
    assert handoff.implementation.canonical_mutation is False
    assert handoff.canonical_mutation is False
    assert handoff.start_view.candidate_id == "EXT-TOOL-SEARCH-HERMES"
    assert handoff.end_view.loop_stage == "IMPLEMENTATION_AUTHORIZED"
    assert handoff.end_view.loop_result == "IMPLEMENTATION_AUTHORIZED"
