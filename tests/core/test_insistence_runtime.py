from elo.core.insistence_runtime import (
    AttemptOutcome,
    AttemptResult,
    InsistenceAction,
    run_insistence_experience,
)


def test_e2e_partial_progress_retries_then_success():
    outcomes = iter([
        AttemptResult(AttemptOutcome.PARTIAL_PROGRESS, "partial", "p1", "e1"),
        AttemptResult(AttemptOutcome.SUCCESS, "complete", "p2", "e2"),
    ])
    actions = []

    def execute(action, state):
        actions.append(action)
        return next(outcomes)

    run = run_insistence_experience(objective="complete experience", execute=execute)

    assert run.terminal_action == InsistenceAction.STOP
    assert run.terminal_outcome == AttemptOutcome.SUCCESS
    assert actions == [InsistenceAction.RETRY, InsistenceAction.RETRY]
    assert len(run.attempts) == 2


def test_e2e_no_progress_refreshes_then_replans_then_succeeds():
    outcomes = iter([
        AttemptResult(AttemptOutcome.NO_PROGRESS, "none", "p0", "e0"),
        AttemptResult(AttemptOutcome.NO_PROGRESS, "none", "p0", "e1"),
        AttemptResult(AttemptOutcome.SUCCESS, "complete", "p1", "e2"),
    ])
    actions = []

    def execute(action, state):
        actions.append(action)
        return next(outcomes)

    run = run_insistence_experience(objective="resolve issue", execute=execute)

    assert actions == [InsistenceAction.RETRY, InsistenceAction.REFRESH, InsistenceAction.REPLAN]
    assert run.terminal_action == InsistenceAction.STOP
    assert run.terminal_outcome == AttemptOutcome.SUCCESS


def test_e2e_blocked_routes_to_handoff():
    def execute(action, state):
        return AttemptResult(AttemptOutcome.BLOCKED, "missing authority", "blocked", "e1")

    run = run_insistence_experience(objective="execute governed task", execute=execute)

    assert run.terminal_action == InsistenceAction.HANDOFF
    assert run.terminal_outcome == AttemptOutcome.BLOCKED
    assert len(run.attempts) == 1


def test_e2e_conflict_routes_to_handoff():
    def execute(action, state):
        return AttemptResult(AttemptOutcome.CONFLICT, "conflicting evidence", "conflict", "e1")

    run = run_insistence_experience(objective="resolve conflict", execute=execute)

    assert run.terminal_action == InsistenceAction.HANDOFF
    assert run.terminal_outcome == AttemptOutcome.CONFLICT


def test_e2e_repeated_identical_state_stops_without_infinite_loop():
    def execute(action, state):
        return AttemptResult(AttemptOutcome.NO_PROGRESS, "none", "same", "same")

    run = run_insistence_experience(objective="bounded recovery", execute=execute, max_attempts=5)

    assert run.terminal_action == InsistenceAction.STOP
    assert run.terminal_outcome == AttemptOutcome.NO_PROGRESS
    assert len(run.attempts) <= 3


def test_e2e_max_attempts_stops():
    def execute(action, state):
        return AttemptResult(AttemptOutcome.PARTIAL_PROGRESS, "still partial", "new", str(state.attempt_no))

    run = run_insistence_experience(objective="bounded task", execute=execute, max_attempts=3)

    assert run.terminal_action == InsistenceAction.STOP
    assert run.terminal_outcome == AttemptOutcome.PARTIAL_PROGRESS
    assert len(run.attempts) == 3


def test_runtime_does_not_select_capability_or_mutate_canonical_state():
    received_states = []

    def execute(action, state):
        received_states.append(state)
        return AttemptResult(AttemptOutcome.SUCCESS, "done", "success", "e1")

    run = run_insistence_experience(objective="safe execution", execute=execute)

    assert run.terminal_action == InsistenceAction.STOP
    assert received_states[0].attempt_no == 0
    assert not hasattr(run, "capability_id")
