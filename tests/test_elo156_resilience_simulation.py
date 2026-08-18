from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    attempt: int
    status: str
    provenance: str
    historical_id: str


def run_simulation(sequence, max_retries=2):
    evidence = []
    for attempt, outcome in enumerate(sequence[: max_retries + 1], start=1):
        if outcome == "timeout":
            evidence.append(Evidence(attempt, "TIMEOUT", "provider-sim", "H-001"))
            continue
        if outcome == "unavailable":
            evidence.append(Evidence(attempt, "UNAVAILABLE", "provider-sim", "H-001"))
            return evidence, "HANDOFF"
        evidence.append(Evidence(attempt, "SUCCESS", "provider-sim", "H-001"))
        return evidence, "RECOVERED"
    return evidence, "DEGRADED"


def test_timeout_is_bounded_and_never_becomes_success():
    evidence, state = run_simulation(["timeout", "timeout", "timeout"])
    assert len(evidence) == 3
    assert state == "DEGRADED"
    assert all(item.status == "TIMEOUT" for item in evidence)


def test_retry_recovers_without_rewriting_history():
    evidence, state = run_simulation(["timeout", "success"])
    assert state == "RECOVERED"
    assert [item.status for item in evidence] == ["TIMEOUT", "SUCCESS"]
    assert [item.attempt for item in evidence] == [1, 2]
    assert all(item.historical_id == "H-001" for item in evidence)


def test_unavailable_provider_is_handoff_not_synthetic_pass():
    evidence, state = run_simulation(["unavailable"])
    assert state == "HANDOFF"
    assert evidence[-1].status == "UNAVAILABLE"
    assert state != "RECOVERED"


def test_recovery_preserves_provenance_and_history():
    evidence, state = run_simulation(["timeout", "success"])
    assert state == "RECOVERED"
    assert len({item.provenance for item in evidence}) == 1
    assert len({item.historical_id for item in evidence}) == 1


def test_retry_is_deterministic_for_same_input():
    first = run_simulation(["timeout", "success"])
    second = run_simulation(["timeout", "success"])
    assert first == second
