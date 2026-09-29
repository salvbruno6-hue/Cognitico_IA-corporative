import pytest

from elo.agent_intake.hermes_13_process_contract import (
    HERMES_13_PROCESS_CONTRACTS,
    get_process_contract,
)


EXPECTED = {
    "EXT-CONTEXT-PLUGIN-HERMES": ("context_task_success_rate", "maximize"),
    "EXT-WORKTREE-HERMES": ("collision_free_task_rate", "maximize"),
    "EXT-MULTIAGENT-HERMES": ("context_isolation_rate", "maximize"),
    "EXT-CRON-HERMES": ("idempotency_collision_free_rate", "maximize"),
    "EXT-MEMPROVIDER-HERMES": ("provider_identity_preservation_rate", "maximize"),
    "EXT-ROUTE-HERMES": ("unsafe_route_admission_block_rate", "maximize"),
    "EXT-PROFILE-HERMES": ("collision_free_profile_task_rate", "maximize"),
    "EXT-BATCH-HERMES": ("collision_free_batch_task_rate", "maximize"),
    "EXT-LEARN-HERMES": ("unsafe_skill_admission_block_rate", "maximize"),
    "EXT-LEARNING-GRAPH-HERMES": ("duplicate_relation_block_rate", "maximize"),
    "EXT-CONTEXTREF-HERMES": (
        "unsafe_malformed_reference_admission_rate",
        "minimize",
    ),
    "EXT-CHECKPOINT-HERMES": ("unsafe_replay_block_rate", "maximize"),
    "EXT-HOOK-HERMES": ("lifecycle_guardrail_detection_rate", "maximize"),
}


def _evidence(candidate_id):
    contract = get_process_contract(candidate_id)
    return type(
        "Evidence",
        (),
        {
            "candidate_id": candidate_id,
            "baseline": {contract.metric: 0.0},
            "adapted": {contract.metric: 1.0},
            "metric_directions": {contract.metric: contract.direction},
            "repeatable": True,
            "provenance_refs": ("controlled-eval:test",),
            "boundary_integrity": True,
        },
    )()


def test_all_13_have_process_specific_metric_contracts():
    assert set(HERMES_13_PROCESS_CONTRACTS) == set(EXPECTED)
    for candidate_id, expected in EXPECTED.items():
        contract = get_process_contract(candidate_id)
        assert (contract.metric, contract.direction) == expected


def test_each_process_contract_accepts_complete_evidence():
    for candidate_id in EXPECTED:
        get_process_contract(candidate_id).validate_evidence(_evidence(candidate_id))


@pytest.mark.parametrize(
    "field",
    ("repeatable", "provenance_refs", "boundary_integrity"),
)
def test_each_process_contract_rejects_missing_process_proof(field):
    for candidate_id in EXPECTED:
        evidence = _evidence(candidate_id)
        setattr(evidence, field, False if field != "provenance_refs" else ())
        with pytest.raises(ValueError, match=candidate_id):
            get_process_contract(candidate_id).validate_evidence(evidence)


def test_process_contract_rejects_wrong_metric():
    evidence = _evidence("EXT-ROUTE-HERMES")
    evidence.baseline = {"some_other_metric": 1.0}
    with pytest.raises(ValueError, match="unsafe_route_admission_block_rate"):
        get_process_contract("EXT-ROUTE-HERMES").validate_evidence(evidence)
