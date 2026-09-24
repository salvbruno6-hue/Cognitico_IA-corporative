"""Tests for the mandatory Symbiont implementation governance views."""

from elo.agent_intake.hermes_current_extensions import build_candidate
from elo.agent_intake.hermes_governed_loop import (
    ImplementationGovernanceContext,
    advance_to_implementation,
)
from elo.agent_intake.symbiont_adaptation import SymbiontAdaptation
from elo.agent_intake.symbiont_implementation_view import ImplementationOwnership, ImplementationViewPhase, render_tree


def _adaptation() -> SymbiontAdaptation:
    return SymbiontAdaptation(
        candidate_id="EXT-HOOK-HERMES",
        target="ELO Workflow/Automation",
        mechanism="event hooks",
        adaptation="bounded lifecycle evidence",
        risks=(),
        evidence_refs=("evidence:test",),
    )


def _context() -> ImplementationGovernanceContext:
    return ImplementationGovernanceContext(
        functional_branch="Cognitive/Symbiont/Implementation",
        capability="ELO Workflow/Automation",
        source_ref="hermes:event-hooks",
        source_commit="abc123",
        specialization="lifecycle evidence",
        ownership=ImplementationOwnership.EXTENSION,
        related_contracts=("Evolution Gate", "Implementation Loop"),
        dependencies=("ELO Workflow/Automation",),
    )


def test_start_and_end_views_are_always_emitted_for_linked_loop():
    handoff = advance_to_implementation(
        build_candidate("EXT-HOOK-HERMES"),
        _adaptation(),
        {"latency": 10.0},
        {"latency": 8.0},
        metric_directions={"latency": "minimize"},
        repeatable=True,
        provenance_refs=("evidence:test",),
        governance_context=_context(),
    )

    assert handoff.start_view.phase is ImplementationViewPhase.START
    assert handoff.end_view.phase is ImplementationViewPhase.END
    assert handoff.start_view.functional_branch == "Cognitive/Symbiont/Implementation"
    assert handoff.end_view.owner == "ELO Workflow/Automation"
    assert handoff.start_view.canonical_mutation is False
    assert handoff.end_view.canonical_mutation is False
    assert handoff.end_view.evidence_refs == ("evidence:test",)
    assert handoff.end_view.evolution_level >= 1
    assert handoff.end_view.evolution_levels_total == 8


def test_missing_linkage_is_visible_and_blocks_progression():
    handoff = advance_to_implementation(
        build_candidate("EXT-HOOK-HERMES"),
        _adaptation(),
        {"latency": 10.0},
        {"latency": 8.0},
        metric_directions={"latency": "minimize"},
        repeatable=True,
        provenance_refs=("evidence:test",),
    )

    assert handoff.next_state == "GOVERNANCE_LINK_REQUIRED"
    assert handoff.start_view.phase is ImplementationViewPhase.START
    assert handoff.end_view.phase is ImplementationViewPhase.END
    assert handoff.end_view.ownership is ImplementationOwnership.UNRESOLVED
    assert handoff.end_view.functional_branch == "UNRESOLVED"


def test_view_cannot_claim_canonical_mutation():
    from elo.agent_intake.symbiont_implementation_view import create_implementation_view

    try:
        create_implementation_view(
            implementation_id="i1",
            phase=ImplementationViewPhase.START,
            candidate_id="c1",
            owner="owner",
            functional_branch="branch",
            capability="capability",
            source_ref="source",
            source_commit="commit",
            loop_stage="OBSERVED",
            canonical_mutation=True,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("governance view must never authorize mutation")


def test_view_exposes_tree_path_and_rendered_location():
    handoff = advance_to_implementation(
        build_candidate("EXT-HOOK-HERMES"), _adaptation(),
        {"latency": 10.0}, {"latency": 8.0},
        metric_directions={"latency": "minimize"}, repeatable=True,
        provenance_refs=("evidence:test",), governance_context=_context(),
    )
    assert handoff.start_view.tree_path == ("ELO", "Cognitive", "Symbiont", "Implementation", "ELO Workflow/Automation")
    tree = render_tree(handoff.end_view)
    assert "◄ IMPLEMENTAÇÃO symbiont:EXT-HOOK-HERMES" in tree
    assert "NÍVEL/ESTADO:" in tree
