from elo.agent_intake.hermes_functional_value_proof import classify
from elo.agent_intake.symbiont_capability_filter import (
    CapabilityEvolutionProposal,
    FilterDisposition,
    evaluate_capability_evolution,
)


def _proposal(**overrides):
    values = dict(
        candidate_id="candidate",
        existing_owner="ELO Context",
        proposed_owner="ELO Context",
        mechanism_objective="increase retrieval precision",
        owner_objective="assemble relevant context",
        objective_alignment_confirmed=True,
    )
    values.update(overrides)
    return CapabilityEvolutionProposal(**values)


def _evidence(candidate_id="candidate"):
    return classify(
        candidate_id,
        baseline=0.5,
        adapted=0.0,
        metric="error_rate",
        direction="minimize",
        repeatable=True,
        regressions=(),
        attribution="CANDIDATE_ATTRIBUTED",
        proof_scope="controlled fixture",
        provenance_refs=("fixture:1", "fixture:2"),
    )


def test_accepts_only_owner_aligned_measured_evolution():
    result = evaluate_capability_evolution(_proposal(), _evidence())
    assert result.disposition is FilterDisposition.ACCEPT
    assert result.owner_preserved is True
    assert result.objective_preserved is True
    assert result.functional_gain_proven is True


def test_rejects_parallel_owner_or_new_authority():
    assert evaluate_capability_evolution(
        _proposal(proposed_owner="Parallel Context"), _evidence()
    ).disposition is FilterDisposition.REJECT
    assert evaluate_capability_evolution(
        _proposal(creates_new_authority=True), _evidence()
    ).disposition is FilterDisposition.REJECT


def test_rejects_duplicate_or_objective_drift():
    assert evaluate_capability_evolution(
        _proposal(duplicates_existing_capability=True), _evidence()
    ).disposition is FilterDisposition.REJECT
    assert evaluate_capability_evolution(
        _proposal(changes_owner_objective=True), _evidence()
    ).disposition is FilterDisposition.REJECT


def test_retests_without_candidate_attributed_functional_gain():
    result = evaluate_capability_evolution(_proposal(), None)
    assert result.disposition is FilterDisposition.RETEST
    assert result.functional_gain_proven is False
