"""Compare two real governed Hermes 13 loop executions longitudinally.

This script is evidence analysis only. It does not authorize production,
promote a candidate, mutate Core, or replace the Evolution Gate.
"""
from __future__ import annotations

import json

from elo.agent_intake.hermes_13_implementation_loop import run_hermes_13_implementation_loop
from elo.cognitive.symbiont_longitudinal_measurement import (
    MeasurementStatus,
    measure_implementation_evidence_change,
)


def main() -> int:
    baseline_run = run_hermes_13_implementation_loop()
    current_run = run_hermes_13_implementation_loop()

    baseline = {item.candidate_id: item for item in baseline_run.results}
    current = {item.candidate_id: item for item in current_run.results}

    measurements = []
    for candidate_id in baseline:
        baseline_item = baseline[candidate_id]
        current_item = current[candidate_id]
        measurement = measure_implementation_evidence_change(
            baseline_item.evidence,
            current_item.evidence,
            tenant_id="controlled-hermes",
            domain="FORGE",
            baseline_decision_id=f"hermes-13:baseline:{candidate_id}",
            current_decision_id=f"hermes-13:current:{candidate_id}",
            baseline_source_ref=f"hermes-13:run:baseline:{candidate_id}",
            current_source_ref=f"hermes-13:run:current:{candidate_id}",
            dataset_version="controlled-hermes-13-v1",
        )
        measurements.append(
            {
                "candidate_id": candidate_id,
                "metric": measurement.metric,
                "direction": measurement.direction,
                "baseline": measurement.baseline_value,
                "current": measurement.current_value,
                "delta": measurement.delta,
                "normalized_gain": measurement.normalized_gain,
                "status": measurement.status.value,
                "evidence_refs": list(measurement.evidence_refs),
                "canonical_mutation": measurement.canonical_mutation,
                "authorization_granted": measurement.authorization_granted,
            }
        )

    payload = {
        "candidate_count": len(measurements),
        "baseline_candidates_processed": baseline_run.all_candidates_processed,
        "current_candidates_processed": current_run.all_candidates_processed,
        "production_execution": False,
        "promotion_authorized": False,
        "canonical_mutation": False,
        "status_counts": {
            status.value: sum(item["status"] == status.value for item in measurements)
            for status in MeasurementStatus
        },
        "measurements": measurements,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
