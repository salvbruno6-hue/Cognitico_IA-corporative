from types import SimpleNamespace
import pytest
from elo.agent_intake import hermes_13_implementation_loop as loop

_NAMES = {
    "EXT-CONTEXT-PLUGIN-HERMES": "run_context_plugin_loop_probe",
    "EXT-WORKTREE-HERMES": "run_worktree_loop_probe",
    "EXT-MULTIAGENT-HERMES": "run_multiagent_loop_probe",
    "EXT-CRON-HERMES": "run_cron_loop_probe",
    "EXT-MEMPROVIDER-HERMES": "run_memory_provider_loop_probe",
    "EXT-ROUTE-HERMES": "run_route_loop_probe",
    "EXT-PROFILE-HERMES": "run_profile_loop_probe",
    "EXT-BATCH-HERMES": "run_batch_loop_probe",
    "EXT-LEARN-HERMES": "run_learning_loop_probe",
    "EXT-LEARNING-GRAPH-HERMES": "run_learning_graph_functional_loop_probe",
    "EXT-CONTEXTREF-HERMES": "run_contextref_functional_loop_probe",
    "EXT-CHECKPOINT-HERMES": "run_checkpoint_loop_probe",
    "EXT-HOOK-HERMES": "run_hook_loop_probe",
}

# Candidatos cujo probe retorna (evidence, implementation) em
# vez de (implementation, evidence). Fonte:
# src/elo/agent_intake/hermes_13_implementation_loop.py
# (implementation_first=False)
_EVIDENCE_FIRST = {"EXT-CHECKPOINT-HERMES"}


def _make_implementation(
    result="READY_FOR_ELO_REVIEW",
    next_state="ELO_REVIEW",
    canonical_mutation=False,
):
    return SimpleNamespace(
        result=result,
        next_state=next_state,
        canonical_mutation=canonical_mutation,
    )


def _make_evidence(candidate_id):
    contract = loop.get_process_contract(candidate_id)
    return SimpleNamespace(
        candidate_id=candidate_id,
        baseline={contract.metric: 0.0},
        adapted={contract.metric: 1.0},
        metric_directions={contract.metric: contract.direction},
        repeatable=True,
        provenance_refs=(f"controlled-eval:{candidate_id}",),
        boundary_integrity=True,
    )


def _fake_probe(candidate_id):
    def probe():
        implementation = _make_implementation()
        evidence = _make_evidence(candidate_id)
        if candidate_id in _EVIDENCE_FIRST:
            return (evidence, implementation)
        return (implementation, evidence)
    return probe


def test_hermes_13_loop_covers_canonical_order_without_authorization(monkeypatch):
    for candidate_id in loop.HERMES_13_EXECUTION_ORDER:
        monkeypatch.setattr(
            loop, _NAMES[candidate_id], _fake_probe(candidate_id)
        )
    report = loop.run_hermes_13_implementation_loop()
    assert report.all_candidates_processed
    assert tuple(
        item.candidate_id for item in report.results
    ) == loop.HERMES_13_EXECUTION_ORDER
    assert len(report.authorization_pending) == 13
    assert all(
        item.result == "READY_FOR_ELO_REVIEW"
        for item in report.results
    )
    assert all(
        item.next_state == "ELO_REVIEW"
        for item in report.results
    )
    assert all(
        not item.canonical_mutation for item in report.results
    )
    assert all(
        item.process_contract_valid for item in report.results
    )


def test_hermes_13_loop_fails_closed_on_canonical_mutation(monkeypatch):
    for candidate_id in loop.HERMES_13_EXECUTION_ORDER:
        monkeypatch.setattr(
            loop, _NAMES[candidate_id], _fake_probe(candidate_id)
        )

    target = "EXT-CONTEXT-PLUGIN-HERMES"

    def mutating_probe():
        implementation = _make_implementation(
            result="IMPLEMENTATION_AUTHORIZED",
            next_state="IMPLEMENTATION_AUTHORIZED",
            canonical_mutation=True,
        )
        evidence = _make_evidence(target)
        if target in _EVIDENCE_FIRST:
            return (evidence, implementation)
        return (implementation, evidence)

    monkeypatch.setattr(
        loop, _NAMES[target], mutating_probe
    )
    with pytest.raises(RuntimeError, match="canonical mutation"):
        loop.run_hermes_13_implementation_loop()


def test_hermes_13_explicit_learning_context_feeds_all_skills_without_authorization(monkeypatch):
    from elo.core.learning_governance import ExperienceRecord
    from elo.cognitive.symbiont_skill_feedback_loop import SkillExecutionContext

    for candidate_id in loop.HERMES_13_EXECUTION_ORDER:
        monkeypatch.setattr(
            loop, _NAMES[candidate_id], _fake_probe(candidate_id)
        )

    class LearningServiceStub:
        def __init__(self):
            self.count = 0

        def capture_outcome(self, **kwargs):
            self.count += 1
            return ExperienceRecord(
                experience_id=f"experience-{self.count}",
                tenant_id=kwargs["tenant_id"],
                domain=kwargs["domain"],
                decision_id=kwargs["decision_id"],
                expected_outcome=kwargs["expected_outcome"],
                observed_outcome=kwargs["observed_outcome"],
                evidence_ids=tuple(kwargs["evidence_ids"]),
                captured_at=1.0,
            )

        def propose_candidate(self, experience, *, dataset_version, hypothesis):
            return SimpleNamespace(
                candidate_id=f"candidate-{experience.experience_id}",
                experience_id=experience.experience_id,
                state="CANDIDATE",
                hypothesis=hypothesis,
            )

    service = LearningServiceStub()
    contexts = {
        candidate_id: SkillExecutionContext(
            skill_id=candidate_id,
            tenant_id="tenant-test",
            domain="FORGE",
            principal_id="symbiont-test",
            decision_id=f"decision-{candidate_id}",
            expected_outcome="controlled decision outcome",
            observed_outcome="improved controlled decision outcome",
            evidence_ids=(f"evidence-{candidate_id}",),
            dataset_version="test-v1",
        )
        for candidate_id in loop.HERMES_13_EXECUTION_ORDER
    }

    report = loop.run_hermes_13_implementation_loop(
        learning_service=service,
        learning_contexts=contexts,
    )

    assert report.learning_feedback_count == 13
    assert service.count == 13
    assert all(
        item.learning_feedback is not None
        and item.learning_feedback.skill_id == item.candidate_id
        and item.learning_feedback.learning_candidate is not None
        and not item.learning_feedback.authorization_granted
        and not item.learning_feedback.canonical_mutation
        for item in report.results
    )


def test_hermes_13_requires_matching_context_for_learning():
    from elo.cognitive.symbiont_skill_feedback_loop import SkillExecutionContext

    context = SkillExecutionContext(
        skill_id="OTHER-SKILL",
        tenant_id="tenant-test",
        domain="FORGE",
        principal_id="symbiont-test",
        decision_id="decision-1",
        expected_outcome="expected",
        observed_outcome="observed",
        evidence_ids=("e1",),
        dataset_version="test-v1",
    )

    with pytest.raises(ValueError, match="cover all 13 candidates"):
        loop.run_hermes_13_implementation_loop(
            learning_service=SimpleNamespace(),
            learning_contexts={"OTHER-SKILL": context},
        )
