"""Governed implementation-loop probe for EXT-LEARN-HERMES."""
from __future__ import annotations
from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_learning_adapter import adapt_skill_learning
from .hermes_learning_boundary import SkillLearningSignal
from .hermes_learning_evaluation import evaluate
from .hermes_learning_functional_evaluation import evaluate_learning_functional_gain
from .hermes_functional_value_proof import classify
from .hermes_governed_loop import advance_to_implementation
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .symbiont_adaptation import refine_capability

def run_learning_loop_probe() -> tuple[object, object]:
    candidate=build_candidate("EXT-LEARN-HERMES")
    evaluation=evaluate()
    functional=evaluate_learning_functional_gain()
    signals=tuple(SkillLearningSignal(
        f"learn-loop-{i}","multiteiner",(f"controlled-eval:learn/{i}",),
        f"skill-{i}",f"digest-{i}",True,True
    ) for i in range(1,6))
    contracts=tuple(adapt_skill_learning(s) for s in signals)
    refs=tuple(ref for c in contracts if c is not None for ref in c.source_refs)
    boundary_integrity=all(
        c is not None and c.promotion_authority is False and c.canonical_mutation is False
        for c in contracts
    )
    adaptation=refine_capability(
        "HERMES-SKILLS",
        {"controlled_test": True, "outcome": {
            "candidate_bounded": boundary_integrity,
            "promotion_blocked": boundary_integrity,
            "canonical_mutation_blocked": boundary_integrity,
        }},
    )
    measurement=CandidateMeasurement(
        candidate.candidate_id,
        {"unsafe_skill_admission_block_rate": functional.baseline_unsafe_admission_block_rate},
        {"unsafe_skill_admission_block_rate": functional.adapted_unsafe_admission_block_rate},
        (), evaluation.repeatable, evaluation.result,
    )
    evidence=measurement_to_implementation_evidence(
        candidate,measurement,
        metric_directions={"unsafe_skill_admission_block_rate":"maximize"},
        provenance_refs=functional.provenance_refs,boundary_integrity=functional.boundary_integrity,
    )
    handoff=advance_to_implementation(
        candidate,adaptation,evidence.baseline,evidence.adapted,
        metric_directions=evidence.metric_directions,repeatable=evidence.repeatable,
        regressions=evidence.regressions,provenance_refs=evidence.provenance_refs,
        boundary_integrity=evidence.boundary_integrity,
        functional_value_evidence=classify(
            "EXT-LEARN-HERMES",
            baseline=functional.baseline_unsafe_admission_block_rate,
            adapted=functional.adapted_unsafe_admission_block_rate,
            metric="unsafe_skill_admission_block_rate",
            direction="maximize",
            repeatable=functional.repeatable,
            regressions=(),
            attribution="CANDIDATE_ATTRIBUTED",
            proof_scope="controlled verified-versus-unverified skill admission prevention",
            provenance_refs=functional.provenance_refs,
        ),
    )
    return handoff.implementation,evidence

__all__=["run_learning_loop_probe"]
