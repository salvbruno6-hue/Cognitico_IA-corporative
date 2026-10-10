"""Governed Symbiont confrontation for the validated OKR Forecast + Scenario lab.

This test promotes only the evidence classification from UNCONFIRMED to PARTIAL
after two controlled contexts and successful regression/evolution gates. It does
not promote canonical learning or claim productive efficacy.
"""

from elo.cognitive.symbionte_lab import SymbiontLabAdapter, SymbiontLabObservation
from elo.core.learning_governance import ExperienceRecord, LearningCandidate


class _LearningProbe:
    """Repository-owned probe: observes canonical learning calls without promotion."""

    def __init__(self) -> None:
        self.captured = 0
        self.proposed = 0

    def capture_outcome(self, **kwargs):
        self.captured += 1
        return ExperienceRecord(
            "exp-okr-forecast-scenario-partial",
            kwargs["tenant_id"],
            kwargs["domain"],
            kwargs["decision_id"],
            kwargs["expected_outcome"],
            kwargs["observed_outcome"],
            kwargs["evidence_ids"],
            0.0,
        )

    def propose_candidate(self, experience, *, dataset_version, hypothesis, provenance=None):
        self.proposed += 1
        return LearningCandidate(
            "cand-okr-forecast-scenario-partial",
            experience.experience_id,
            experience.tenant_id,
            experience.domain,
            hypothesis,
            dataset_version,
            {"experience_id": experience.experience_id},
        )


def _observation() -> SymbiontLabObservation:
    return SymbiontLabObservation(
        observation_id="obs-okr-forecast-scenario-partial",
        tenant_id="tenant-lab",
        domain="strategic_okr",
        decision_id="decision-okr-forecast-scenario-lab",
        expected_outcome="Forecast and Scenario remain bounded across distinct OKR contexts",
        observed_outcome=(
            "Two controlled contexts preserved deterministic forecast, bounded scenario, "
            "fail-closed evidence gaps and regression-free validation"
        ),
        evidence_ids=(
            "commit:3cef0a0572a13a0a6b0b444adf7aee81a52f57b9",
            "commit:98099560673589ade18994cf6bc895491032149b",
            "workflow:evolution-gate:38083074764",
            "workflow:baseline-evidence:38083074714",
            "workflow:behavioral-validation:38083074756",
        ),
        source_ref="pr:962",
        source_commit="98099560673589ade18994cf6bc895491032149b",
        hypothesis=(
            "Existing GovernedForecastFaculty and Scenario can incrementally strengthen "
            "strategic_okr without creating parallel authority"
        ),
        baseline="OkrEvaluationService owns deterministic OKR evaluation; forecast initially absent",
        experiment=(
            "Compare increasing and decreasing KR trajectories with different windows and horizons, "
            "preserving fail-closed behavior"
        ),
        result="Both controlled contexts passed repository regression and evolution gates",
        regression_status="PASS",
        generalization_status="PARTIAL",
        risk="LOW",
        existing_owner=None,
        scope="strategic_okr:forecast+scenario:incremental-composition",
        tenant_scope="tenant-lab",
        source_kind="pr",
    )


def test_partial_generalization_enters_existing_symbiont_without_automatic_promotion():
    learning = _LearningProbe()
    evaluation = SymbiontLabAdapter(learning).evaluate(
        _observation(),
        principal_id="principal-lab",
        dataset_version="okr-forecast-scenario-lab-v2",
    )

    assert evaluation.state == "LAB_ONLY"
    assert evaluation.observation.generalization_status == "PARTIAL"
    assert evaluation.experience is not None
    assert evaluation.candidate is not None
    assert evaluation.candidate.candidate_id == "cand-okr-forecast-scenario-partial"
    assert learning.captured == 1
    assert learning.proposed == 1
    assert evaluation.disposition in {"CANDIDATE_FOR_GOVERNED_LEARNING", "STRENGTHEN"}


def test_partial_generalization_does_not_claim_confirmed_or_productive_learning():
    observation = _observation()
    assert observation.generalization_status != "CONFIRMED"
    assert observation.source_kind == "pr"
    assert "productive" not in observation.result.lower()
