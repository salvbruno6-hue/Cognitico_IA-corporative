from elo.agent_intake.hermes_learning_boundary import SkillLearningSignal
from elo.agent_intake.hermes_learning_runtime_adapter import run_learning_runtime_with_evidence
from elo.agent_intake.runtime_operational_evidence_collector import RuntimeOperationalEvidenceCollector
from elo.cognitive.symbionte_lab import SymbiontLabAdapter
from elo.core.learning_governance import GovernedLearningService


class MemoryStub:
    def __init__(self):
        self.calls = []

    def remember(self, **kwargs):
        self.calls.append(kwargs)


def signal(*, signal_id="learn-runtime-1", verified=True):
    return SkillLearningSignal(
        signal_id=signal_id,
        tenant_scope="tenant-a",
        source_refs=(f"runtime-source:{signal_id}",),
        skill_name="governed skill admission",
        instruction_digest=f"digest-{signal_id}",
        user_directed=True,
        verified=verified,
    )


def test_unverified_learning_signal_is_blocked_before_governed_learning():
    memory = MemoryStub()
    learning = SymbiontLabAdapter(GovernedLearningService(memory))
    sink = RuntimeOperationalEvidenceCollector()

    result = run_learning_runtime_with_evidence(
        signal=signal(verified=False),
        learning=learning,
        principal_id="principal-1",
        dataset_version="ds-1",
        runtime_commit="runtime-commit",
        runtime_trace="trace-1",
        runtime_evidence_sink=sink,
    )

    assert result.admitted is False
    assert result.candidate_id is None
    assert result.evidence_emitted is False
    assert memory.calls == []
    assert sink.ready_groups() == ()


def test_verified_learning_reaches_real_governed_learning_path_and_emits_evidence():
    memory = MemoryStub()
    learning = SymbiontLabAdapter(GovernedLearningService(memory))
    sink = RuntimeOperationalEvidenceCollector()

    first = run_learning_runtime_with_evidence(
        signal=signal(signal_id="learn-runtime-1"),
        learning=learning,
        principal_id="principal-1",
        dataset_version="ds-1",
        runtime_commit="runtime-commit",
        runtime_trace="trace-1",
        runtime_evidence_sink=sink,
    )
    second = run_learning_runtime_with_evidence(
        signal=signal(signal_id="learn-runtime-2"),
        learning=learning,
        principal_id="principal-1",
        dataset_version="ds-1",
        runtime_commit="runtime-commit",
        runtime_trace="trace-2",
        runtime_evidence_sink=sink,
    )

    assert first.admitted is True
    assert second.admitted is True
    assert first.evolution_classification == "COMPATIBLE"
    assert second.evolution_classification == "COMPATIBLE"
    assert first.candidate_id is not None
    assert second.candidate_id is not None
    assert len(memory.calls) == 2

    groups = sink.ready_groups()
    assert len(groups) == 1
    group = groups[0]
    assert group.candidate_id == "EXT-LEARN-HERMES"
    assert group.repeatable is True

    outcome = group.to_operational_outcome()
    assert outcome is not None
    assert outcome.candidate_id == "EXT-LEARN-HERMES"
    assert outcome.repeatability.executions >= 2
    assert outcome.repeatability.exact_rate == 1.0
