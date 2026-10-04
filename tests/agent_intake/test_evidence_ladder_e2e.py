from datetime import datetime, timezone

from elo.agent_intake.hermes_functional_value_proof import classify
from elo.agent_intake.runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeProvenance,
    create_runtime_evidence,
)
from elo.core.evolution_gate import EvolutionGate, EvolutionProposal


def test_evidence_ladder_keeps_controlled_gain_separate_from_production():
    functional = classify(
        "candidate-e2e",
        baseline=10.0,
        adapted=8.0,
        metric="latency",
        direction="minimize",
        repeatable=True,
        regressions=(),
        attribution="CANDIDATE_ATTRIBUTED",
        proof_scope="controlled test",
        provenance_refs=("controlled:1", "controlled:2"),
    )

    assert functional.level == "FUNCTIONAL_CONTROLLED_GAIN"
    assert functional.functional_gain_proven is True
    assert functional.production_proven is False


def test_runtime_evidence_requires_independent_runtime_facts():
    evidence = create_runtime_evidence(
        execution_id="exec-e2e-1",
        candidate_id="candidate-e2e",
        owner="canonical-owner",
        runtime_entrypoint="test.runtime.entrypoint",
        action_observed=True,
        metric="latency",
        direction="minimize",
        baseline=10.0,
        observed_value=8.0,
        attribution="candidate",
        provenance=RuntimeProvenance(
            commit="055a3b68a63f49309187c5fd68d9993e043fdd8f",
            runtime_trace="trace-e2e-1",
            test_run="runtime-test-1",
        ),
        regression=False,
        repeatability=RepeatabilityEvidence(
            executions=2,
            successful=2,
            rate=1.0,
        ),
        timestamp=datetime(2026, 10, 4, tzinfo=timezone.utc),
    )

    assert evidence.operational_outcome_proven is True
    assert evidence.provenance.runtime_trace == "trace-e2e-1"


def test_evolution_gate_does_not_convert_evidence_into_canonical_authority():
    proposal = EvolutionProposal(
        proposal_id="candidate-e2e",
        tenant_id="tenant-e2e",
        source_id="runtime-trace-e2e",
        summary="controlled runtime evidence",
        purpose_alignment=True,
        identity_compatible=True,
        architecture_compatible=True,
        governance_compatible=True,
        evidence_ids=("trace-e2e-1",),
        maturity_score=0.9,
        provenance={"runtime_trace": "trace-e2e-1"},
    )

    decision = EvolutionGate().evaluate(proposal)

    assert decision.classification.value == "COMPATIBLE"
    assert decision.canonical_mutation_allowed is False


def test_missing_runtime_observation_cannot_be_represented_as_operational_outcome():
    try:
        create_runtime_evidence(
            execution_id="exec-e2e-2",
            candidate_id="candidate-e2e",
            owner="canonical-owner",
            runtime_entrypoint="test.runtime.entrypoint",
            action_observed=False,
            metric="latency",
            direction="minimize",
            baseline=10.0,
            observed_value=8.0,
            attribution="candidate",
            provenance=RuntimeProvenance(
                commit="055a3b68a63f49309187c5fd68d9993e043fdd8f",
                runtime_trace="trace-e2e-2",
            ),
            regression=False,
            repeatability=RepeatabilityEvidence(
                executions=2,
                successful=2,
                rate=1.0,
            ),
        )
    except ValueError as exc:
        assert "observed runtime action" in str(exc)
    else:
        raise AssertionError("missing runtime observation must fail closed")
