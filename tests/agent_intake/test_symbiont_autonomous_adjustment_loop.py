from elo.agent_intake.implementation_loop import (
    SymbiontAutonomyState,
    run_symbiont_autonomous_adjustment_loop,
)


def test_symbiont_runs_without_human_between_iterations():
    calls = []
    outcomes = iter([("RETEST", None), ("SUCCESS", None)])

    def adjust(iteration):
        calls.append(("adjust", iteration))
        return True, f"evidence:{iteration}"

    def evaluate(iteration):
        calls.append(("evaluate", iteration))
        return next(outcomes)

    result = run_symbiont_autonomous_adjustment_loop(
        adjust=adjust,
        evaluate=evaluate,
        max_iterations=3,
    )

    assert result.state is SymbiontAutonomyState.COMPLETED
    assert result.human_required is False
    assert result.canonical_mutation is False
    assert calls == [
        ("adjust", 1),
        ("evaluate", 1),
        ("adjust", 2),
        ("evaluate", 2),
    ]


def test_symbiont_escalates_only_at_explicit_governance_boundary():
    approvals = []

    def adjust(iteration):
        return True, f"evidence:{iteration}"

    def evaluate(iteration):
        return "RETEST", None

    def human_boundary(iteration):
        approvals.append(iteration)
        return "Production execution requires explicit authorization."

    result = run_symbiont_autonomous_adjustment_loop(
        adjust=adjust,
        evaluate=evaluate,
        human_boundary=human_boundary,
        max_iterations=5,
    )

    assert result.state is SymbiontAutonomyState.HUMAN_APPROVAL_REQUIRED
    assert result.human_required is True
    assert result.iterations[-1].iteration == 1
    assert result.next_action == "Production execution requires explicit authorization."
    assert approvals == [1]


def test_symbiont_blocks_on_unresolved_evaluation_without_fabricating_success():
    result = run_symbiont_autonomous_adjustment_loop(
        adjust=lambda iteration: (False, None),
        evaluate=lambda iteration: (
            "RETEST",
            "Evidence is contradictory; human decision is required.",
        ),
        max_iterations=3,
    )

    assert result.state is SymbiontAutonomyState.BLOCKED
    assert result.human_required is True
    assert result.completed is False
    assert result.iterations[0].changed is False
