"""Controlled chain test: information -> pointer -> capability -> evidence -> Symbiont."""

import pytest

from elo.agent_intake.conditional_pointer import resolve_pointer
from elo.agent_intake.native_capabilities import CAPABILITY_IDS, execute_candidate
from elo.agent_intake.symbiont_adaptation import refine_capability, refinement_is_eligible_for_test


TENANT = "multiteiner"
CONDITIONS = {
    "HERMES-MEMORY": "semantic-recall",
    "HERMES-SKILLS": "skill-execution",
    "HERMES-TOOLSETS": "tool-resolution",
    "HERMES-CONTEXT": "context-resolution",
    "HERMES-DELEGATION": "delegation",
    "HERMES-AUTOMATION": "schedule",
    "HERMES-MCP": "external-capability",
    "HERMES-CHECKPOINT": "state-recovery",
}


@pytest.mark.parametrize("capability_id", CAPABILITY_IDS)
def test_information_to_capability_to_symbiont_chain(capability_id):
    condition = CONDITIONS[capability_id]

    pointer = resolve_pointer(
        request_id=f"chain-{capability_id}",
        tenant_scope=TENANT,
        information={"condition": condition, "source": "controlled-lab"},
    )

    assert pointer.status == "resolved"
    assert pointer.matched_capability == capability_id
    assert pointer.destination
    assert pointer.learning_candidate == {
        "promotion_state": "candidate_only",
        "canonical_mutation": False,
    }

    evidence = execute_candidate(
        capability_id,
        request_id=f"chain-execution-{capability_id}",
        tenant_scope=TENANT,
    )
    assert evidence.status == "completed"
    assert all(evidence.outcome.values())
    assert evidence.learning_candidate == {
        "promotion_state": "candidate_only",
        "canonical_mutation": False,
    }

    adaptation = refine_capability(
        capability_id,
        {
            "controlled_test": True,
            "outcome": evidence.outcome,
        },
    )
    assert adaptation.capability_id == capability_id
    assert adaptation.existing_capacity
    assert adaptation.evidence_quality == "controlled_verified"
    assert refinement_is_eligible_for_test(adaptation) is True
    assert adaptation.promotion_state == "candidate_only"
    assert adaptation.canonical_mutation is False


def test_chain_does_not_infer_unknown_information_destination():
    pointer = resolve_pointer(
        request_id="chain-unknown-01",
        tenant_scope=TENANT,
        information={"condition": "unknown-condition", "source": "controlled-lab"},
    )
    assert pointer.status == "unresolved"
    assert pointer.matched_capability is None
    assert pointer.destination is None
    assert pointer.learning_candidate["canonical_mutation"] is False


def test_chain_preserves_policy_signal_before_execution():
    pointer = resolve_pointer(
        request_id="chain-policy-01",
        tenant_scope=TENANT,
        information={"condition": "external-capability", "source": "controlled-lab"},
    )
    assert pointer.matched_capability == "HERMES-MCP"
    assert pointer.policy_required is True


def test_chain_is_idempotent_for_same_information():
    information = {"condition": "semantic-recall", "source": "controlled-lab", "value": 1}
    first = resolve_pointer(
        request_id="chain-idempotent-01",
        tenant_scope=TENANT,
        information=information,
    )
    second = resolve_pointer(
        request_id="chain-idempotent-01",
        tenant_scope=TENANT,
        information=information,
    )
    assert first == second
    assert information == {"condition": "semantic-recall", "source": "controlled-lab", "value": 1}
