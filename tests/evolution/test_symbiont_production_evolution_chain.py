from elo.cognitive.symbiont_capability_evolution import review_capabilities
from elo.cognitive.symbiont_capability_evolution_handoff import (
    prepare_capability_experiment_handoff,
)
from scripts.run_symbiont_capability_evolution import metrics_from_production_runs


def test_production_evidence_flows_to_diagnostic_then_existing_lab_contract():
    runs = (
        {
            "id": "run-capability-001",
            "details": {
                "report": {
                    "capability_metrics": [
                        {
                            "item": "decision_outcome_attribution",
                            "baseline": 0.70,
                            "current": 0.77,
                            "direction": "maximize",
                            "evidence_refs": ["production-evidence:001"],
                            "measurement_period": "PRODUCTION:2026-09",
                        }
                    ]
                }
            },
        },
    )

    metrics = metrics_from_production_runs(runs)
    review = review_capabilities(metrics=metrics)

    assert review.status == "ANALYSIS_READY"
    assert review.canonical_mutation is False
    assert review.metrics[0].evidence_mode == "DIRECT"
    assert review.metrics[0].measurement_period.startswith("PRODUCTION:")
    assert "elo_automation_runs:run-capability-001" in review.evidence_refs

    handoff = prepare_capability_experiment_handoff(
        review,
        tenant_id="tenant-1",
        decision_id="decision-capability-001",
        observation_id="obs-capability-001",
        source_ref="runtime://capability-evolution",
        source_commit="commit-capability-001",
        item="decision_outcome_attribution",
        hypothesis="bounded improvement of attribution quality",
        baseline="0.70",
        experiment="controlled capability correction",
        result="0.79",
        regression_status="NONE",
        generalization_status="PARTIAL",
        risk="LOW",
    )

    assert handoff.observation.domain == "EVOLUÇÃO_DE_CAPACIDADES"
    assert handoff.observation.tenant_scope == "tenant-1"
    assert handoff.observation.evidence_ids == review.evidence_refs
    assert handoff.observation.source_kind == "runtime"


def test_production_feed_does_not_infer_metrics_from_unrelated_run_data():
    runs = (
        {
            "id": "run-no-capability-metric",
            "details": {
                "report": {
                    "learning": {
                        "experiences": 999,
                        "validated": 42,
                    }
                }
            },
        },
    )

    assert metrics_from_production_runs(runs) == ()
    assert review_capabilities(metrics=()).status == "NOT_MEASURED"
