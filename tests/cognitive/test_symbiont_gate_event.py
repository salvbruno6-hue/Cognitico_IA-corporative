from elo.cognitive.symbiont_gate_event import observe_github_gate_event


def test_success_event_is_perceived_as_completed() -> None:
    result = observe_github_gate_event(
        gate_id="workflow-100",
        event={"conclusion": "success", "run_id": 100},
    )
    assert result.completed is True
    assert result.evidence_ref == "100"


def test_pending_event_is_not_completed() -> None:
    result = observe_github_gate_event(
        gate_id="check-200",
        event={"status": "in_progress"},
    )
    assert result.completed is False


def test_repeated_same_event_is_same_observation() -> None:
    event = {"conclusion": "success", "html_url": "https://github.example/run/300"}
    first = observe_github_gate_event(gate_id="run-300", event=event)
    second = observe_github_gate_event(gate_id="run-300", event=event)
    assert first == second
