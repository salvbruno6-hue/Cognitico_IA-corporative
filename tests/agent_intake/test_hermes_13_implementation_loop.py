from types import SimpleNamespace

import pytest

from elo.agent_intake import hermes_13_implementation_loop as loop


def _fake_probe(candidate_id):
    def probe():
        implementation = SimpleNamespace(
            result="READY_FOR_ELO_REVIEW",
            next_state="ELO_REVIEW",
            canonical_mutation=False,
        )
        evidence = SimpleNamespace(candidate_id=candidate_id)
        return implementation, evidence

    return probe


def test_hermes_13_loop_covers_canonical_order_without_authorization(monkeypatch):
    for candidate_id in loop.HERMES_13_EXECUTION_ORDER:
        monkeypatch.setattr(
            loop,
            {
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
            }[candidate_id],
            _fake_probe(candidate_id),
        )

    report = loop.run_hermes_13_implementation_loop()

    assert report.all_candidates_processed
    assert tuple(item.candidate_id for item in report.results) == loop.HERMES_13_EXECUTION_ORDER
    assert len(report.authorization_pending) == 13
    assert all(item.result == "READY_FOR_ELO_REVIEW" for item in report.results)
    assert all(item.next_state == "ELO_REVIEW" for item in report.results)
    assert all(not item.canonical_mutation for item in report.results)
    assert all(item.evidence_present for item in report.results)


def test_hermes_13_loop_fails_closed_on_canonical_mutation(monkeypatch):
    candidate_id = loop.HERMES_13_EXECUTION_ORDER[0]

    for name in (
        "run_context_plugin_loop_probe",
        "run_worktree_loop_probe",
        "run_multiagent_loop_probe",
        "run_cron_loop_probe",
        "run_memory_provider_loop_probe",
        "run_route_loop_probe",
        "run_profile_loop_probe",
        "run_batch_loop_probe",
        "run_learning_loop_probe",
        "run_learning_graph_functional_loop_probe",
        "run_contextref_functional_loop_probe",
        "run_checkpoint_loop_probe",
        "run_hook_loop_probe",
    ):
        monkeypatch.setattr(loop, name, _fake_probe(candidate_id))

    def mutating_probe():
        implementation = SimpleNamespace(
            result="IMPLEMENTATION_AUTHORIZED",
            next_state="IMPLEMENTATION_AUTHORIZED",
            canonical_mutation=True,
        )
        evidence = SimpleNamespace(candidate_id=candidate_id)
        return implementation, evidence

    monkeypatch.setattr(loop, "run_context_plugin_loop_probe", mutating_probe)

    with pytest.raises(RuntimeError, match="canonical mutation"):
        loop.run_hermes_13_implementation_loop()
