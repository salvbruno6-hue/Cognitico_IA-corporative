from __future__ import annotations

from elo.agent_intake.hermes_context_reference_functional_adapter import admit_message
from elo.agent_intake.runtime_operational_evidence_collector import (
    RuntimeEvidenceKey,
    RuntimeOperationalEvidenceCollector,
)


def test_contextref_repeated_real_adapter_invocations_produce_operational_outcome(monkeypatch):
    monkeypatch.setenv("ELO_RUNTIME_COMMIT", "runtime-repeatability-test")

    collector = RuntimeOperationalEvidenceCollector()

    for _ in range(2):
        emitted = []
        admit_message("@file:README.md:20-10", runtime_evidence_sink=emitted)

        assert len(emitted) == 1
        collector.append(emitted[0])

    key = RuntimeEvidenceKey(
        candidate_id="EXT-CONTEXTREF-HERMES",
        owner="ELO Context",
        runtime_entrypoint="elo.context.references.admit_message",
        metric="unsafe_malformed_reference_rejection_rate",
        direction="maximize",
    )

    outcome = collector.outcome(key)

    assert outcome.level == "OPERATIONAL_OUTCOME"
    assert outcome.repeatable is True
    assert outcome.production_proven is False
    assert len(outcome.provenance_refs) == 2
