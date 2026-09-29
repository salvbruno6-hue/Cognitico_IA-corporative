from elo.agent_intake.hermes_cron_continuity_refinement import (
    CronContinuitySignal,
    ContinuityDisposition,
    assess_cron_continuity,
    evaluate_cron_continuity_gain,
)


def test_cron_continuity_controlled_gain_and_boundary():
    baseline, adapted, repeatable, boundary, refs = evaluate_cron_continuity_gain()
    assert baseline == 0.0
    assert adapted == 1.0
    assert repeatable is True
    assert boundary is True
    assert refs


def test_cron_continuity_requires_prior_run_and_bounded_scope():
    base = dict(
        signal_id="c1",
        automation_id="a1",
        prior_run_ref="run-1",
        continuity_scope="bounded:task",
        provenance_ref="ref:1",
        explicit_continuity=True,
    )
    assert assess_cron_continuity(CronContinuitySignal(**base)).disposition is ContinuityDisposition.CANDIDATE
    assert assess_cron_continuity(
        CronContinuitySignal(**{**base, "prior_run_ref": ""})
    ).disposition is ContinuityDisposition.REJECTED
    assert assess_cron_continuity(
        CronContinuitySignal(**{**base, "continuity_scope": "*"})
    ).disposition is ContinuityDisposition.REJECTED
    assert assess_cron_continuity(
        CronContinuitySignal(**{**base, "canonical_memory_write": True})
    ).disposition is ContinuityDisposition.REJECTED
