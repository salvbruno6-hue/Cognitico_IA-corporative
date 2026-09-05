import pytest

from elo.core.assurance import (
    AbstentionDecision,
    AssuranceError,
    CompletionReceipt,
    CustodyEnvelope,
    ReplayRecord,
    RetrievalEvaluation,
)
from elo.knowledge.rag import GovernedRetriever, RetrievedEvidence


def test_a15_retrieval_quality_blocks_stale_hits():
    evaluation = RetrievalEvaluation("eval-v1", 10, 0.9, 0.8, 0.75, 0.1, 120.0)
    assert evaluation.quality_gate == "BLOCKED_STALE"


def test_a15_retrieval_quality_passes_clean_evidence():
    evaluation = RetrievalEvaluation("eval-v1", 10, 0.9, 0.8, 0.75, 0.0, 120.0)
    assert evaluation.quality_gate == "PASS"


def test_a15_builds_metrics_from_captured_rankings():
    evaluation = RetrievalEvaluation.from_rankings(
        dataset_version="eval-v2",
        k=2,
        queries=(
            {"relevant_ids": ("a",), "ranked_ids": ("a", "b"), "latency_ms": (10.0,)},
            {"relevant_ids": ("c",), "ranked_ids": ("b", "c"), "latency_ms": (20.0,)},
        ),
    )
    assert evaluation.queries == 2
    assert evaluation.recall_at_k == 1.0
    assert evaluation.precision_at_k == 0.5
    assert evaluation.mrr == 0.75
    assert evaluation.stale_hit_rate == 0.0
    assert evaluation.p95_latency_ms == 10.0


def test_a16_replay_is_deterministic_and_does_not_execute():
    record = ReplayRecord.build(
        execution_id="exec-1",
        input_snapshot={"query": "M01"},
        decision_snapshot={"decision": "READ"},
        tool_plan=({"tool": "forge", "operation": "read"},),
        result_snapshot={"rows": 2},
        world_snapshot={"policy": "v1"},
        compiler_version="c1",
    )
    assert record.verify(expected_world_snapshot={"policy": "v1"}, expected_compiler_version="c1")
    assert not record.verify(expected_compiler_version="c2")


def test_a17_closure_requires_all_required_dimensions_and_binds_replay():
    fields = {
        "identity": "id", "scope": "repo", "direction": "read", "authority": "elo-authz",
        "mutation": "none", "protection": "fail-closed", "epistemic_state": "verified",
        "proof": "sha256", "freshness": "current",
    }
    replay = ReplayRecord.build(
        execution_id="exec-1",
        input_snapshot={"query": "M01"},
        decision_snapshot={"decision": "READ"},
        tool_plan=(),
        result_snapshot={"rows": 2},
    )
    receipt = CompletionReceipt("exec-1", fields, replay.trace_digest, ("evidence-1",))
    assert receipt.closed
    assert receipt.validate_replay(replay)
    with pytest.raises(AssuranceError):
        CompletionReceipt("exec-2", {"identity": "id"}, "digest", ("evidence-1",))


def test_a18_custody_is_hash_linked_and_self_verifying():
    first = CustodyEnvelope.build(sequence=0, kind="INTENT", payload={"query": "M01"})
    second = CustodyEnvelope.build(sequence=1, kind="TOOL", payload={"tool": "forge"}, previous_digest=first.digest)
    assert first.verify()
    assert second.verify(first)
    assert not CustodyEnvelope(second.sequence, second.kind, second.payload_digest, second.previous_digest, "tampered").verify(first)


def test_a19_abstention_is_fail_closed():
    decision = AbstentionDecision.decide(evidence_count=0, conflict=True)
    assert decision.status == "ABSTAIN"
    assert "INSUFFICIENT_EVIDENCE" in decision.reasons
    assert "UNRESOLVED_CONFLICT" in decision.reasons


def test_a19_proceed_requires_no_blocking_condition():
    decision = AbstentionDecision.decide(evidence_count=2)
    assert decision.status == "PROCEED"
    assert decision.reasons == ()


def test_a19_retrieval_path_abstains_on_stale_or_conflicting_provenance():
    stale = RetrievedEvidence("e1", "forge", "m1", "M01", 0.9, {"stale": True})
    conflicting = RetrievedEvidence("e2", "forge", "m2", "M01", 0.8, {"conflict": True})
    decision = GovernedRetriever._assure_evidence((stale, conflicting))
    assert decision.status == "ABSTAIN"
    assert "STALE_EVIDENCE" in decision.reasons
    assert "UNRESOLVED_CONFLICT" in decision.reasons


def test_a19_retrieval_path_abstains_on_out_of_scope_evidence():
    evidence = RetrievedEvidence("e1", "forge", "m1", "M01", 0.9, {"out_of_scope": True})
    decision = GovernedRetriever._assure_evidence((evidence,))
    assert decision.status == "ABSTAIN"
    assert decision.reasons == ("OUT_OF_SCOPE",)
