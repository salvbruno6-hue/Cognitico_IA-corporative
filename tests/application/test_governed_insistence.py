from elo.application.use_cases.governed_insistence import (
    GovernedInsistenceRequest,
    GovernedInsistenceUseCase,
)
from elo.core.capability_resolution import resolve_capability
from elo.core.insistence_runtime import AttemptOutcome, AttemptResult, InsistenceAction


def test_e2e_core_decision_to_governed_insistence_to_success():
    # The condition is supplied as an already-produced cognitive-analysis result.
    # This test intentionally does not define an IntentSpec -> condition mapping.
    decision = resolve_capability(
        request_id="req-e2e-001",
        tenant_scope="tenant-test",
        condition="skill-execution",
        analysis_evidence=("evidence-cognitive-001",),
    )
    assert decision.executable is True
    assert decision.capability_id == "ELO_SKILL_RUNTIME"

    observed_actions = []
    outcomes = iter(
        [
            AttemptResult(
                AttemptOutcome.PARTIAL_PROGRESS,
                "skill started",
                "p1",
                "e1",
                ("e1",),
            ),
            AttemptResult(
                AttemptOutcome.SUCCESS,
                "skill completed",
                "p2",
                "e2",
                ("e2",),
            ),
        ]
    )

    def execute(core_decision, action, state):
        assert core_decision is decision
        assert core_decision.capability_id == "ELO_SKILL_RUNTIME"
        observed_actions.append(action)
        return next(outcomes)

    run = GovernedInsistenceUseCase().run(
        GovernedInsistenceRequest(
            objective="complete governed skill experience",
            core_capability_decision=decision,
        ),
        execute=execute,
    )

    assert observed_actions == [InsistenceAction.RETRY, InsistenceAction.RETRY]
    assert run.terminal_outcome == AttemptOutcome.SUCCESS
    assert run.terminal_action == InsistenceAction.STOP
    assert len(run.attempts) == 2


def test_e2e_core_unresolved_decision_cannot_enter_insistence_runtime():
    decision = resolve_capability(
        request_id="req-e2e-002",
        tenant_scope="tenant-test",
        condition="unknown-condition",
        analysis_evidence=("evidence-cognitive-002",),
    )
    assert decision.executable is False
    assert decision.capability_id is None

    try:
        GovernedInsistenceUseCase().run(
            GovernedInsistenceRequest(
                objective="must not execute unresolved capability",
                core_capability_decision=decision,
            ),
            execute=lambda *_: AttemptResult(AttemptOutcome.SUCCESS, "unexpected"),
        )
    except ValueError as exc:
        assert str(exc) == "Core capability decision is not executable"
    else:
        raise AssertionError("unresolved Core decision reached execution")
