import pytest

from elo.core.pre_inference_veto import VetoDecision, evaluate_pre_inference_veto


def test_explicit_allow_permits_inference_and_auxiliary_context_paths():
    result = evaluate_pre_inference_veto({"action": "allow"})
    assert result.decision is VetoDecision.PROCEED
    assert result.inference_allowed is True
    assert result.external_memory_allowed is True
    assert result.background_review_allowed is True
    assert result.compaction_allowed is True


def test_explicit_block_stops_inference_and_all_auxiliary_context_egress():
    result = evaluate_pre_inference_veto({"action": "block", "message": "policy denied"})
    assert result.decision is VetoDecision.BLOCK
    assert result.inference_allowed is False
    assert result.external_memory_allowed is False
    assert result.background_review_allowed is False
    assert result.compaction_allowed is False


@pytest.mark.parametrize("payload", [
    None,
    [],
    "block",
    {},
    {"action": None},
    {"action": True},
    {"action": 1},
    {"action": "unknown"},
    {"action": "block"},
    {"action": "block", "message": ""},
    {"action": "block", "message": []},
])
def test_malformed_or_ambiguous_policy_results_fail_closed(payload):
    result = evaluate_pre_inference_veto(payload)
    assert result.decision is VetoDecision.INVALID
    assert result.inference_allowed is False
    assert result.external_memory_allowed is False
    assert result.background_review_allowed is False
    assert result.compaction_allowed is False


def test_block_does_not_expose_original_prompt_or_create_execution_authority():
    payload = {"action": "block", "message": "withheld", "prompt": "secret raw prompt"}
    result = evaluate_pre_inference_veto(payload)
    assert "secret raw prompt" not in repr(result)
    assert not hasattr(result, "execution_allowed")
