"""Integration probe for the Hermes checkpoint candidate.

The probe composes existing state recovery with the candidate-specific replay
guard, then routes structured functional evidence through the shared Symbiont
handoff. It remains controlled and never mutates canonical ELO.
"""
from __future__ import annotations

from .checkpoint_loop_harness import evaluate_checkpoint_loop_harness
from .hermes_current_extensions import build_candidate
from .hermes_functional_value_proof import classify
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .hermes_governed_loop import (
    ImplementationGovernanceContext,
    close_approved_candidate,
    advance_to_implementation,
)
from .symbiont_adaptation import refine_capability
from .symbiont_implementation_view import ImplementationOwnership


def _functional_evidence(measurement):
    return classify(
        "EXT-CHECKPOINT-HERMES",
        baseline=measurement.baseline["unsafe_replay_block_rate"],
        adapted=measurement.adapted["unsafe_replay_block_rate"],
        metric="unsafe_replay_block_rate",
        direction="maximize",
        repeatable=measurement.repeatable,
        regressions=measurement.regressions,
        attribution=(
            "CANDIDATE_ATTRIBUTED"
            if measurement.candidate_incremental_effect_isolated
            else "OWNER_ATTRIBUTED"
        ),
        proof_scope=(
            "controlled stale-checkpoint replay prevention; existing ELO State Recovery "
            "remains responsible for ordinary recovery"
        ),
        provenance_refs=(
            "controlled-eval:checkpoint/replay-guard/baseline",
            "controlled-eval:checkpoint/replay-guard/adapted",
        ),
    )


def run_checkpoint_loop_probe(*, tenant_scope: str = "loop-tenant", repeats: int = 5):
    candidate = build_candidate("EXT-CHECKPOINT-HERMES")
    measurement = evaluate_checkpoint_loop_harness(
        tenant_scope=tenant_scope,
        repeats=repeats,
    )
    candidate_measurement = measurement.to_candidate_measurement()

    adaptation = refine_capability(
        "HERMES-CHECKPOINT",
        {
            "controlled_test": True,
            "outcome": {
                "integrity": True,
                "continuity": True,
                "unsafe_replay_blocked": measurement.adapted["unsafe_replay_block_rate"] == 1.0,
            },
        },
    )

    evidence = measurement_to_implementation_evidence(
        candidate,
        candidate_measurement,
        metric_directions=measurement.metric_directions or {},
        provenance_refs=(
            "controlled-eval:checkpoint/replay-guard/baseline",
            "controlled-eval:checkpoint/replay-guard/adapted",
        ),
        boundary_integrity=True,
    )

    handoff = advance_to_implementation(
        candidate,
        adaptation,
        evidence.baseline,
        evidence.adapted,
        repeatable=evidence.repeatable,
        regressions=evidence.regressions,
        metric_directions=evidence.metric_directions,
        provenance_refs=evidence.provenance_refs,
        boundary_integrity=evidence.boundary_integrity,
        functional_value_evidence=_functional_evidence(measurement),
    )
    return evidence, handoff.implementation


def close_checkpoint_approved_candidate(
    *,
    tenant_scope: str = "loop-tenant",
    repeats: int = 5,
    evolution_gate_approved: bool = False,
    elo_implementation_approved: bool = False,
):
    """Run checkpoint evidence through the governed approval closure.

    Approval flags are explicit inputs. The function never defaults to approval,
    and canonical mutation remains disabled by the governed handoff.
    """
    candidate = build_candidate("EXT-CHECKPOINT-HERMES")
    measurement = evaluate_checkpoint_loop_harness(
        tenant_scope=tenant_scope,
        repeats=repeats,
    )
    candidate_measurement = measurement.to_candidate_measurement()
    adaptation = refine_capability(
        "HERMES-CHECKPOINT",
        {
            "controlled_test": True,
            "outcome": {
                "integrity": True,
                "continuity": True,
                "unsafe_replay_blocked": measurement.adapted["unsafe_replay_block_rate"],
            },
        },
    )
    evidence = measurement_to_implementation_evidence(
        candidate,
        candidate_measurement,
        metric_directions=measurement.metric_directions or {},
        provenance_refs=(
            "controlled-eval:checkpoint/replay-guard/baseline",
            "controlled-eval:checkpoint/replay-guard/adapted",
        ),
        boundary_integrity=True,
    )
    handoff = close_approved_candidate(
        candidate,
        adaptation,
        evidence.baseline,
        evidence.adapted,
        metric_directions=evidence.metric_directions,
        repeatable=evidence.repeatable,
        regressions=evidence.regressions,
        provenance_refs=evidence.provenance_refs,
        boundary_integrity=evidence.boundary_integrity,
        evolution_gate_approved=evolution_gate_approved,
        elo_implementation_approved=elo_implementation_approved,
        governance_context=ImplementationGovernanceContext(
            functional_branch="Cognitive/Symbiont/Implementation",
            capability="ELO State Recovery",
            source_ref="hermes:checkpoint",
            source_commit="controlled-eval:checkpoint-replay-guard",
            specialization="pre-mutation checkpoint replay guard",
            ownership=ImplementationOwnership.EXTENSION,
            related_contracts=("Evolution Gate", "Implementation Loop"),
            dependencies=("ELO State Recovery",),
        ),
    )
    return evidence, handoff


__all__ = ["run_checkpoint_loop_probe", "close_checkpoint_approved_candidate"]
