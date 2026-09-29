from elo.agent_intake.hermes_live_steering_refinement import (
    LiveSteeringSignal,
    SteeringDisposition,
    assess_live_steering,
    evaluate_live_steering_gain,
)


def test_live_steering_controlled_gain_and_boundary():
    baseline, adapted, repeatable, boundary, refs = evaluate_live_steering_gain()
    assert baseline == 0.0
    assert adapted == 1.0
    assert repeatable is True
    assert boundary is True
    assert refs


def test_live_steering_requires_explicit_directive_and_rejects_authority_transfer():
    base = dict(
        signal_id="s1",
        parent_execution_id="p1",
        child_agent_id="c1",
        directive_digest="d1",
        provenance_ref="ref:1",
        explicit_directive=True,
    )
    assert assess_live_steering(LiveSteeringSignal(**base)).disposition is SteeringDisposition.CANDIDATE
    assert assess_live_steering(
        LiveSteeringSignal(**{**base, "explicit_directive": False})
    ).disposition is SteeringDisposition.REJECTED
    assert assess_live_steering(
        LiveSteeringSignal(**{**base, "authority_transfer": True})
    ).disposition is SteeringDisposition.REJECTED
