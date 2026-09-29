from elo.agent_intake.hermes_current_refinements import (
    CronContinuityObservation,
    LiveSteeringObservation,
    REFINEMENTS,
    get_refinement,
    validate_cron_continuity,
    validate_live_steering,
)


def test_refinements_reuse_existing_capabilities():
    assert len(REFINEMENTS) == 2
    assert get_refinement("REF-MULTIAGENT-LIVE-STEERING-HERMES").parent_capability == "EXT-MULTIAGENT-HERMES"
    assert get_refinement("REF-CRON-CONTINUITY-HERMES").parent_capability == "EXT-CRON-HERMES"
    assert all(item.candidate_only for item in REFINEMENTS)
    assert all(item.canonical_mutation is False for item in REFINEMENTS)


def test_live_steering_requires_explicit_provenance_and_bounded_identity():
    valid = LiveSteeringObservation(
        "REF-MULTIAGENT-LIVE-STEERING-HERMES", "parent-1", "child-1", "directive-1", True, "trace-1"
    )
    invalid = LiveSteeringObservation(
        "REF-MULTIAGENT-LIVE-STEERING-HERMES", "parent-1", "child-1", "directive-1", False, "trace-1"
    )
    assert validate_live_steering(valid)
    assert not validate_live_steering(invalid)


def test_cron_continuity_requires_prior_run_and_bounded_memory():
    valid = CronContinuityObservation(
        "REF-CRON-CONTINUITY-HERMES", "automation-1", "run-1", "same-job", "bounded", "trace-1"
    )
    invalid = CronContinuityObservation(
        "REF-CRON-CONTINUITY-HERMES", "automation-1", "", "same-job", "bounded", "trace-1"
    )
    unbounded = CronContinuityObservation(
        "REF-CRON-CONTINUITY-HERMES", "automation-1", "run-1", "same-job", "unbounded", "trace-1"
    )
    assert validate_cron_continuity(valid)
    assert not validate_cron_continuity(invalid)
    assert not validate_cron_continuity(unbounded)
