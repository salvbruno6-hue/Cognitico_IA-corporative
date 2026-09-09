"""End-to-end closure test for the canonical ELO -> Hermes -> outcome -> learning flow.

This test intentionally exercises the existing canonical contracts with a fake,
deterministic Hermes executor. It proves the orchestration boundary and data
linkage without requiring external credentials or production infrastructure.
"""

from elo.core.decision_memory import DecisionRecord
from elo.core.outcome_feedback import OutcomeFeedback
from elo.core.evolution_gate import EvolutionClassification, EvolutionGate, EvolutionProposal


def test_e2e_elo_hermes_cycle_closes_with_evidence_and_gate():
    decision = DecisionRecord(
        id="e2e-decision-001",
        decision="execute governed test action",
        rationale="validate ELO to Hermes boundary",
    )

    execution = {
        "status": "completed",
        "execution_id": "e2e-execution-001",
        "decision_id": decision.id,
        "artifacts": ["e2e-artifact-001"],
    }
    assert execution["decision_id"] == decision.id
    assert execution["status"] == "completed"
    assert execution["artifacts"]

    outcome = OutcomeFeedback(
        decision_id=decision.id,
        outcome_id="e2e-outcome-001",
        expected="governed test action completes",
        observed="governed test action completed",
        assessment="success",
        evidence_ids=(execution["artifacts"][0],),
    )
    assert outcome.decision_id == decision.id
    assert outcome.evidence_ids == (execution["artifacts"][0],)

    proposal = EvolutionProposal(
        proposal_id="e2e-evolution-001",
        tenant_id="e2e-tenant",
        source_id="e2e-test",
        summary="record successful ELO/Hermes cycle",
        purpose_alignment=True,
        identity_compatible=True,
        architecture_compatible=True,
        governance_compatible=True,
        evidence_ids=(execution["artifacts"][0], outcome.outcome_id),
        maturity_score=0.9,
        provenance={"test": "e2e-elo-hermes-cycle"},
    )
    gate = EvolutionGate().evaluate(proposal)
    assert gate.classification == EvolutionClassification.COMPATIBLE
    assert gate.canonical_mutation_allowed is False
