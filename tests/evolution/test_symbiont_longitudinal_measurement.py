from elo.cognitive.symbiont_longitudinal_measurement import (
    MeasurementStatus,
    SkillObservation,
    measure_longitudinal_change,
)


def obs(
    observation_id,
    *,
    value,
    skill_id="EXT-CRON-HERMES",
    tenant_id="tenant-a",
    domain="automation",
    metric="idempotency_collision_free_rate",
    direction="maximize",
    evidence_refs=("ev-1",),
    decision_id="decision-1",
    dataset_version="ds-1",
    learning_context_ids=(),
):
    return SkillObservation(
        observation_id=observation_id,
        skill_id=skill_id,
        tenant_id=tenant_id,
        domain=domain,
        decision_id=decision_id,
        metric=metric,
        value=value,
        direction=direction,
        evidence_refs=evidence_refs,
        source_ref=f"source:{observation_id}",
        dataset_version=dataset_version,
        learning_context_ids=learning_context_ids,
    )


def test_first_observation_establishes_baseline_without_claiming_improvement():
    result = measure_longitudinal_change(None, obs("run-1", value=0.80))
    assert result.status is MeasurementStatus.BASELINE_ESTABLISHED
    assert result.delta is None
    assert result.comparable is False


def test_maximize_metric_reports_improvement_and_delta():
    result = measure_longitudinal_change(
        obs("run-1", value=0.80),
        obs("run-2", value=0.88, learning_context_ids=("learning-1",)),
    )
    assert result.status is MeasurementStatus.IMPROVED
    assert result.delta == 0.08
    assert result.normalized_gain == 0.1
    assert result.learning_context_ids == ("learning-1",)
    assert result.canonical_mutation is False
    assert result.authorization_granted is False


def test_minimize_metric_reports_improvement_when_value_falls():
    result = measure_longitudinal_change(
        obs("run-1", value=0.20, metric="unsafe_malformed_reference_admission_rate", direction="minimize"),
        obs("run-2", value=0.10, metric="unsafe_malformed_reference_admission_rate", direction="minimize"),
    )
    assert result.status is MeasurementStatus.IMPROVED
    assert result.delta == -0.10
    assert result.normalized_gain == 0.5


def test_regression_is_direction_aware():
    result = measure_longitudinal_change(obs("run-1", value=0.90), obs("run-2", value=0.70))
    assert result.status is MeasurementStatus.REGRESSED
    assert result.delta == -0.20


def test_missing_evidence_cannot_claim_change():
    result = measure_longitudinal_change(
        obs("run-1", value=0.80),
        obs("run-2", value=0.90, evidence_refs=()),
    )
    assert result.status is MeasurementStatus.INSUFFICIENT_EVIDENCE
    assert result.delta is None


def test_tenant_boundary_is_rejected():
    try:
        measure_longitudinal_change(
            obs("run-1", value=0.80, tenant_id="tenant-a"),
            obs("run-2", value=0.90, tenant_id="tenant-b"),
        )
    except ValueError as exc:
        assert "tenant_id" in str(exc)
    else:
        raise AssertionError("cross-tenant comparison must be rejected")


def test_skill_metric_and_direction_must_match():
    try:
        measure_longitudinal_change(
            obs("run-1", value=0.80),
            obs("run-2", value=0.90, metric="other_metric"),
        )
    except ValueError as exc:
        assert "metric" in str(exc)
    else:
        raise AssertionError("cross-metric comparison must be rejected")


def test_duplicate_observation_does_not_create_false_improvement():
    result = measure_longitudinal_change(
        obs("run-1", value=0.80),
        obs("run-2", value=0.90),
        seen_observation_ids=("run-2",),
    )
    assert result.status is MeasurementStatus.DUPLICATE
    assert result.delta is None
    assert result.comparable is False
