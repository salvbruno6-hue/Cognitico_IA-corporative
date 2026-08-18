from elo.core.strategy_recovery import StrategicPath, assess_resolution_for_forward_strategy


def test_resolution_is_not_the_end_of_analysis():
    assessment = assess_resolution_for_forward_strategy(
        situation="supplier delay",
        resolution="temporary source secured",
        objective="protect delivery commitment",
        residual_risks=["capacity gap"],
    )

    assert assessment.recommended_path is StrategicPath.RECOVER
    assert StrategicPath.PROTECT in assessment.strategic_paths
    assert assessment.next_move
    assert assessment.trigger


def test_reversal_is_preferred_when_the_route_is_no_longer_supported():
    assessment = assess_resolution_for_forward_strategy(
        situation="production route failed",
        resolution="failure contained",
        objective="deliver without violating quality boundary",
        residual_risks=["repeat failure"],
        reversal_warranted=True,
        authority_available=False,
    )

    assert assessment.recommended_path is StrategicPath.REVERSE
    assert StrategicPath.HANDOFF in assessment.strategic_paths
    assert assessment.authority_required is True


def test_stable_resolution_can_advance_with_monitoring():
    assessment = assess_resolution_for_forward_strategy(
        situation="planning variance",
        resolution="capacity confirmed",
        objective="meet approved demand",
        authority_available=True,
    )

    assert assessment.recommended_path is StrategicPath.ADVANCE
    assert StrategicPath.HANDOFF not in assessment.strategic_paths
