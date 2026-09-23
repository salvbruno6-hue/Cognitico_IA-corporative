from elo.cognitive.symbiont_capability_evolution import CapabilityMetric, review_capabilities
from elo.cognitive.symbiont_capability_evolution_handoff import prepare_capability_experiment_handoff


def _review():
    return review_capabilities(metrics=(CapabilityMetric(
        item="fpy", baseline=0.70, current=0.77, direction="maximize",
        evidence_refs=("ev-fpy",), measurement_period="2026-09",
    ),))


def test_review_can_be_translated_to_canonical_lab_observation():
    handoff = prepare_capability_experiment_handoff(
        _review(), tenant_id="tenant-1", decision_id="decision-1", observation_id="obs-1",
        source_ref="runtime://capability", source_commit="commit-1", item="fpy",
        hypothesis="bounded improvement", baseline="FPY=0.70",
        experiment="paired controlled test", result="FPY=0.79",
        regression_status="NONE", generalization_status="PARTIAL", risk="LOW",
    )
    assert handoff.observation.domain == "EVOLUÇÃO_DE_CAPACIDADES"
    assert handoff.observation.evidence_ids == ("ev-fpy",)
    assert handoff.observation.experiment == "paired controlled test"


def test_experiment_fields_are_explicit():
    handoff = prepare_capability_experiment_handoff(
        _review(), tenant_id="tenant-1", decision_id="decision-1", observation_id="obs-2",
        source_ref="runtime://capability", source_commit="commit-1", item="fpy",
        hypothesis="explicit", baseline="explicit baseline", experiment="explicit experiment",
        result="explicit result", regression_status="NONE", generalization_status="CONFIRMED", risk="LOW",
    )
    assert handoff.observation.hypothesis == "explicit"
    assert handoff.observation.baseline == "explicit baseline"
    assert handoff.observation.result == "explicit result"
