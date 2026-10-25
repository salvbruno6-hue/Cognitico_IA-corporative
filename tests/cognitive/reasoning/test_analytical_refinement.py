from elo.cognitive.reasoning.analytical_refinement import (
    AnalyticalRefinementSignals,
    RefinementLevel,
    select_analytical_refinement,
)


def test_no_risk_signal_keeps_refinement_off():
    decision = select_analytical_refinement(AnalyticalRefinementSignals())
    assert decision.level is RefinementLevel.NONE
    assert decision.reasons == ()
    assert decision.checks == ()


def test_single_uncertainty_selects_targeted_refinement():
    decision = select_analytical_refinement(AnalyticalRefinementSignals(
        uncertainties=("capacity evidence needs revalidation",),
    ))
    assert decision.level is RefinementLevel.TARGETED
    assert "material uncertainty remains" in decision.reasons
    assert decision.checks


def test_conflict_selects_deep_refinement():
    decision = select_analytical_refinement(AnalyticalRefinementSignals(
        conflicts=("source-a != source-b",),
    ))
    assert decision.level is RefinementLevel.DEEP
    assert any("counterevidence" in check for check in decision.checks)


def test_consequential_action_plus_gap_selects_deep_refinement():
    decision = select_analytical_refinement(AnalyticalRefinementSignals(
        consequential_action=True,
        integrity_gaps=("stock availability unresolved",),
    ))
    assert decision.level is RefinementLevel.DEEP
    assert "consequential action is contemplated" in decision.reasons


def test_consequential_action_alone_is_targeted_not_deep():
    decision = select_analytical_refinement(AnalyticalRefinementSignals(
        consequential_action=True,
    ))
    assert decision.level is RefinementLevel.TARGETED
