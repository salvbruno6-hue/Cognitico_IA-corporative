"""Laboratory proof that the autonomous Symbiont loop can reuse existing skills.

This is intentionally a lab test: it validates orchestration through existing
capabilities without promoting anything to Core or claiming production.
"""

from elo.core.calibration import CalibrationObservation, ConfidenceCalibration
from elo.core.decision_outcome_loop import DecisionLifecycle, DecisionState
from elo.core.learning_governance import EvaluationRecord, GovernedLearningService, LearningCandidate\nfrom elo.core.evolution_gate import (
    EvolutionClassification,
    EvolutionGate,
    EvolutionProposal,
)
from elo.core.systemic_primitives import DecisionRecord, OutcomeFeedback
from elo.agent_intake.implementation_loop import (
    SymbiontAutonomyState,
    run_symbiont_autonomous_adjustment_loop,
)


def _decision_lifecycle() -> DecisionLifecycle:
    return DecisionLifecycle(
        decision=DecisionRecord(
            decision_id="lab-decision-001",
            decision="apply-bounded-adjustment",
            rationale="validated laboratory adjustment",
            expected_outcome="preserve-or-improve",
        )
    )


def test_autonomous_loop_is_validated_by_existing_core_skills():
    lifecycle = _decision_lifecycle()
    calibration = ConfidenceCalibration()
    gate = EvolutionGate()
    events: list[str] = []

    def adjust(iteration: int):
        events.append(f"adjust:{iteration}")
        return True, f"lab-evidence:{iteration}"

    def evaluate(iteration: int):
        lifecycle.state = DecisionState.PROPOSED
        lifecycle.transition(DecisionState.APPROVED, actor="symbiont")
        lifecycle.transition(DecisionState.EXECUTED, actor="symbiont")
        lifecycle.transition(
            DecisionState.OBSERVING,
            evidence_ids=(f"lab-evidence:{iteration}",),
            actor="symbiont",
        )
        lifecycle.attach_outcome(
            OutcomeFeedback(
                decision_id="lab-decision-001",
                expected="preserve-or-improve",
                observed="preserve-or-improve",
                evidence_ids=(f"lab-evidence:{iteration}",),
            )
        )
        lifecycle.transition(
            DecisionState.EVALUATED,
            evidence_ids=(f"lab-evidence:{iteration}",),
            actor="symbiont",
        )

        calibration.add(
            CalibrationObservation(
                confidence=0.90,
                outcome_score=1.0,
                decision_id="lab-decision-001",
            )
        )

        decision = gate.evaluate(
            EvolutionProposal(
                proposal_id="lab-autonomy-001",
                tenant_id="lab",
                source_id="symbiont",
                summary="autonomous adjustment validation",
                purpose_alignment=True,
                identity_compatible=True,
                architecture_compatible=True,
                governance_compatible=True,
                evidence_ids=(f"lab-evidence:{iteration}",),
                maturity_score=0.80,
                existing_owner="existing-symbiont-loop",
                provenance={"mode": "LAB_ONLY"},
            )
        )

        if decision.classification is not EvolutionClassification.DUPLICATE_SUPERSEDED:
            return "BLOCKED", "existing authority was not reused"

        reliability = calibration.reliability()
        if not reliability:
            return "BLOCKED", "calibration produced no evidence"

        return "SUCCESS", None

    result = run_symbiont_autonomous_adjustment_loop(
        adjust=adjust,
        evaluate=evaluate,
        max_iterations=2,
    )

    assert result.state is SymbiontAutonomyState.COMPLETED
    assert result.human_required is False
    assert result.canonical_mutation is False
    assert events == ["adjust:1"]
    assert lifecycle.state is DecisionState.EVALUATED


def test_existing_gate_blocks_canonicalization_without_human_decision():
    decision = EvolutionGate().evaluate(
        EvolutionProposal(
            proposal_id="lab-autonomy-canonicalization-001",
            tenant_id="lab",
            source_id="symbiont",
            summary="attempted canonical promotion",
            purpose_alignment=True,
            identity_compatible=True,
            architecture_compatible=True,
            governance_compatible=True,
            evidence_ids=("lab-evidence:canonical-block",),
            maturity_score=0.95,
            provenance={"mode": "LAB_ONLY"},
        )
    )

    assert decision.classification is EvolutionClassification.COMPATIBLE
    assert decision.canonical_mutation_allowed is False


def test_promotion_remains_human_gated():
    candidate = LearningCandidate(
        candidate_id="candidate-001",
        experience_id="experience-001",
        tenant_id="lab",
        domain="symbiont",
        hypothesis="validated adjustment",
        dataset_version="lab-v1",
        provenance={"mode": "LAB_ONLY"},
    )
    evaluation = EvaluationRecord(
        candidate_id="candidate-001",
        metric="quality",
        score=1.0,
        threshold=0.8,
        evaluator="lab",
        dataset_version="lab-v1",
        evaluated_at=0.0,
    )

    try:
        GovernedLearningService.approve_for_promotion(
            candidate,
            evaluation,
            human_approved=False,
        )
    except ValueError as exc:
        assert "human approval is required" in str(exc)
    else:
        raise AssertionError("promotion must remain blocked without human approval")
