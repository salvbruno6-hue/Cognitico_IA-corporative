from src.elo.agent_intake.hermes_context_reference_functional_adapter import admit_message
from src.elo.agent_intake.runtime_operational_evidence import InMemoryRuntimeEvidenceSink


def test_contextref_runtime_emits_observed_evidence(monkeypatch):
    monkeypatch.setenv("ELO_RUNTIME_COMMIT", "runtime-test-commit")
    sink = InMemoryRuntimeEvidenceSink()

    result = admit_message("@file:README.md:20-10", runtime_evidence_sink=sink)

    assert result[0].accepted is False
    assert len(sink.list()) == 1
    evidence = sink.list()[0]
    assert evidence.candidate_id == "EXT-CONTEXTREF-HERMES"
    assert evidence.action_observed is True
    assert evidence.provenance.commit == "runtime-test-commit"
    assert evidence.observed_value == 1.0


def test_contextref_runtime_does_not_emit_without_runtime_commit(monkeypatch):
    monkeypatch.delenv("ELO_RUNTIME_COMMIT", raising=False)
    monkeypatch.delenv("GITHUB_SHA", raising=False)
    sink = InMemoryRuntimeEvidenceSink()

    admit_message("@file:README.md:20-10", runtime_evidence_sink=sink)

    assert sink.list() == ()
