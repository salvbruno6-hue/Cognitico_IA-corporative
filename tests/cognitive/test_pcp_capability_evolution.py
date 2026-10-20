from elo.cognitive.pcp_capability_evolution import (
    PCPCapabilityMetricInput,
    delegate_pcp_capability_evolution,
    prepare_pcp_capability_evolution,
)
from elo.cognitive.pcp_confrontation import confront
from elo.cognitive.pcp_operational_evidence import build_operational_evidence_package


def _package():
    return build_operational_evidence_package(
        (
            confront(
                "production",
                "ORD-001",
                planned=10,
                actual=8,
                evidence_ids=("ev-production-1",),
            ),
        ),
        source_kind="supabase",
        source_ref="mt_ordens_producao",
    )


def test_bridge_preserves_explicit_capability_measurement():
    handoff = prepare_pcp_capability_evolution(
        _package(),
        metrics=(
            PCPCapabilityMetricInput(
                item="on_time_delivery",
                baseline=0.80,
                current=0.88,
                direction="maximize",
                measurement_period="2026-09",
                evidence_refs=("ev-otd-1",),
            ),
        ),
    )
    assert handoff.metrics[0].baseline == 0.80
    assert handoff.metrics[0].current == 0.88
    assert "ev-production-1" in handoff.evidence_refs
    assert "ev-otd-1" in handoff.evidence_refs


def test_bridge_does_not_infer_capability_values():
    handoff = prepare_pcp_capability_evolution(
        _package(),
        metrics=(
            PCPCapabilityMetricInput(
                item="capacity",
                baseline=None,
                current=None,
                direction="",
                measurement_period="",
            ),
        ),
    )
    assert handoff.metrics[0].baseline is None
    assert handoff.metrics[0].current is None
    assert handoff.metrics[0].direction == ""


def test_bridge_delegates_to_injected_canonical_evolution():
    handoff = prepare_pcp_capability_evolution(
        _package(),
        metrics=(
            PCPCapabilityMetricInput(
                item="fpy",
                baseline=0.70,
                current=0.77,
                direction="maximize",
                measurement_period="2026-09",
                evidence_refs=("ev-fpy-1",),
            ),
        ),
    )
    calls = {}

    def factory(**kwargs):
        calls["metric"] = kwargs
        return kwargs

    def reviewer(**kwargs):
        calls["review"] = kwargs
        return "CANONICAL_EVOLUTION_REVIEW"

    result = delegate_pcp_capability_evolution(
        handoff,
        capability_metric_factory=factory,
        capability_reviewer=reviewer,
    )
    assert result == "CANONICAL_EVOLUTION_REVIEW"
    assert calls["metric"]["item"] == "fpy"
    assert calls["metric"]["baseline"] == 0.70
    assert calls["review"]["evidence_refs"] == (
        "ev-production-1",
        "ev-fpy-1",
    )
