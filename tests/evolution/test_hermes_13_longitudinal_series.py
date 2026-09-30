from elo.agent_intake.hermes_13_implementation_loop import run_hermes_13_implementation_loop
from elo.cognitive.symbiont_longitudinal_measurement import (
    MeasurementStatus,
    measure_implementation_evidence_change,
)


def test_real_hermes_13_runs_feed_longitudinal_measurement():
    baseline = run_hermes_13_implementation_loop()
    current = run_hermes_13_implementation_loop()

    baseline_by_id = {item.candidate_id: item for item in baseline.results}
    current_by_id = {item.candidate_id: item for item in current.results}

    assert len(baseline_by_id) == 13
    assert len(current_by_id) == 13

    for candidate_id, baseline_item in baseline_by_id.items():
        current_item = current_by_id[candidate_id]
        assert baseline_item.evidence is not None
        assert current_item.evidence is not None

        measurement = measure_implementation_evidence_change(
            baseline_item.evidence,
            current_item.evidence,
            tenant_id="controlled-hermes",
            domain="FORGE",
            baseline_decision_id=f"before:{candidate_id}",
            current_decision_id=f"after:{candidate_id}",
            baseline_source_ref=f"run-before:{candidate_id}",
            current_source_ref=f"run-after:{candidate_id}",
            dataset_version="controlled-hermes-13-v1",
        )

        assert measurement.skill_id == candidate_id
        assert measurement.status in {
            MeasurementStatus.IMPROVED,
            MeasurementStatus.STABLE,
            MeasurementStatus.REGRESSED,
        }
        assert measurement.canonical_mutation is False
        assert measurement.authorization_granted is False
