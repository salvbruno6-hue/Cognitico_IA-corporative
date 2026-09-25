from elo.cognitive.symbiont_gate_observer import github_gate_observer_from_status


def test_external_status_is_translated_without_authorization() -> None:
    observation = github_gate_observer_from_status(
        "ci-789",
        {"state": "SUCCESS", "evidence_ref": "run-789"},
    )
    assert observation.gate_id == "ci-789"
    assert observation.completed is True
    assert observation.evidence_ref == "run-789"


def test_unknown_external_status_remains_pending() -> None:
    observation = github_gate_observer_from_status("ci-unknown", {"state": "QUEUED"})
    assert observation.completed is False
