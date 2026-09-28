from elo.agent_intake.hermes_20260928_refinements import (
    CronContinuitySignal,
    LiveSteeringSignal,
    RefinementDisposition,
    assess_cron_continuity,
    assess_live_steering,
)

def test_live_steering_requires_explicit_directive_and_provenance():
    signal = LiveSteeringSignal("s1", "parent-1", "child-1", "tighten scope", True, "trace-1")
    assert assess_live_steering(signal) is RefinementDisposition.CANDIDATE

def test_live_steering_fails_closed_without_explicit_activation():
    signal = LiveSteeringSignal("s1", "parent-1", "child-1", "tighten scope", False, "trace-1")
    assert assess_live_steering(signal) is RefinementDisposition.REJECTED

def test_cron_continuity_requires_prior_run_and_provenance():
    signal = CronContinuitySignal("c1", "automation-1", "run-1", "same-task", True, "trace-1")
    assert assess_cron_continuity(signal) is RefinementDisposition.CANDIDATE

def test_cron_continuity_fails_closed_without_prior_run():
    signal = CronContinuitySignal("c1", "automation-1", "", "same-task", True, "trace-1")
    assert assess_cron_continuity(signal) is RefinementDisposition.REJECTED
