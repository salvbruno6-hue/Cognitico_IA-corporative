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
    return SimpleNamespace(candidate_id=candidate_id)


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
