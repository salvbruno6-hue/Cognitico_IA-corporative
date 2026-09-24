from elo.agent_intake.hermes_current_extensions import build_candidate
from elo.agent_intake.hermes_governed_loop import (
    ImplementationGovernanceContext,
    advance_to_implementation,
    close_approved_candidate,
)
from elo.agent_intake.symbiont_adaptation import refine_capability
from elo.agent_intake.symbiont_implementation_view import ImplementationOwnership


def verified_adaptation():
    return refine_capability(
        "HERMES-CHECKPOINT",
        {"controlled_test": True, "outcome": {"boundary": True}, "source_reference": "hermes-checkpoint"},
    )


def governance_context(capability: str, source_ref: str, source_commit: str) -> ImplementationGovernanceContext:
    return ImplementationGovernanceContext(
        functional_branch="Cognitive/Symbiont/Implementation",
        capability=capability,
        source_ref=source_ref,
        source_commit=source_commit,
        specialization="controlled implementation evidence",
        ownership=ImplementationOwnership.EXTENSION,
        related_contracts=("Evolution Gate", "Implementation Loop"),
        dependencies=(capability,),
    )


def test_incomplete_evidence_stops_before_elo_review():
    result = advance_to_implementation(
        build_candidate("EXT-CHECKPOINT-HERMES"), verified_adaptation(),
        {"latency": 10.0}, {"latency": 10.0},
        metric_directions={"latency": "minimize"}, repeatable=True,
        provenance_refs=("eval-001",),
    )
    assert result.next_state == "MEASURED_GAIN"
    assert result.implementation.result == "RETEST"
    assert not result.implementation.canonical_mutation


def test_positive_repeatable_gain_reaches_elo_review_not_approval():
    result = advance_to_implementation(
        build_candidate("EXT-CHECKPOINT-HERMES"), verified_adaptation(),
        {"latency": 10.0}, {"latency": 8.0},
        metric_directions={"latency": "minimize"}, repeatable=True,
        provenance_refs=("eval-002", "eval-003"),
    )
    assert result.next_state == "ELO_REVIEW"
    assert result.implementation.result == "READY_FOR_ELO_REVIEW"


def test_explicit_elo_approval_reaches_implementation_authorized_only():
    result = advance_to_implementation(
        build_candidate("EXT-CHECKPOINT-HERMES"), verified_adaptation(),
        {"latency": 10.0}, {"latency": 8.0},
        metric_directions={"latency": "minimize"}, repeatable=True,
        provenance_refs=("eval-004", "eval-005"), elo_approved=True, evolution_gate_approved=True,
    )
    assert result.next_state == "IMPLEMENTATION_AUTHORIZED"
    assert result.implementation.result == "IMPLEMENTATION_AUTHORIZED"
    assert not result.implementation.canonical_mutation


def test_approved_candidate_closure_requires_both_governance_and_implementation_authorization():
    result = close_approved_candidate(
        build_candidate("EXT-CHECKPOINT-HERMES"), verified_adaptation(),
        {"recovery_success": 0.0}, {"recovery_success": 1.0},
        metric_directions={"recovery_success": "maximize"},
        repeatable=True,
        provenance_refs=("controlled-eval:checkpoint-loop-harness",),
        evolution_gate_approved=True,
        elo_implementation_approved=False,
        governance_context=governance_context(
            "ELO State Recovery", "hermes:checkpoint", "controlled-eval:checkpoint-loop-harness"
        ),
    )
    assert result.next_state == "ELO_REVIEW"
    assert result.implementation.result == "READY_FOR_ELO_REVIEW"
    assert not result.implementation.canonical_mutation


def test_approved_candidate_closure_reaches_authorized_without_canonical_mutation():
    result = close_approved_candidate(
        build_candidate("EXT-HOOK-HERMES"), verified_adaptation(),
        {"guardrail_interception_coverage": 0.0},
        {"guardrail_interception_coverage": 1.0},
        metric_directions={"guardrail_interception_coverage": "maximize"},
        repeatable=True,
        provenance_refs=("controlled-eval:hook-loop-harness",),
        evolution_gate_approved=True,
        elo_implementation_approved=True,
        governance_context=governance_context(
            "ELO Workflow/Automation", "hermes:event-hooks", "controlled-eval:hook-loop-harness"
        ),
    )
    assert result.next_state == "IMPLEMENTATION_AUTHORIZED"
    assert result.implementation.result == "IMPLEMENTATION_AUTHORIZED"
    assert not result.implementation.canonical_mutation

def test_approved_candidate_closure_requires_governance_linkage():
    result = close_approved_candidate(
        build_candidate("EXT-CHECKPOINT-HERMES"),
        verified_adaptation(),
        {"recovery_success": 0.0},
        {"recovery_success": 1.0},
        metric_directions={"recovery_success": "maximize"},
        repeatable=True,
        provenance_refs=("controlled-eval:checkpoint-loop-harness",),
        evolution_gate_approved=True,
        elo_implementation_approved=True,
    )
    assert result.next_state == "GOVERNANCE_LINK_REQUIRED"
    assert result.implementation.result == "RETEST"
    assert result.start_view.ownership is ImplementationOwnership.UNRESOLVED
    assert result.end_view.ownership is ImplementationOwnership.UNRESOLVED

