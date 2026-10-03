from elo.agent_intake.hermes_surface_delta_20261003 import (
    SURFACE_DELTAS,
    get_surface_delta,
    validate_registry,
)


def test_surface_registry_is_candidate_only_and_non_operational() -> None:
    result = validate_registry()
    assert result == {"mechanisms": 10, "candidate_only": 10}


def test_surface_ids_are_unique_and_mapped_to_existing_owners() -> None:
    assert len({item.mechanism_id for item in SURFACE_DELTAS}) == 10
    assert all(item.elo_owner for item in SURFACE_DELTAS)
    assert all(item.validation_boundary for item in SURFACE_DELTAS)


def test_relevant_surface_introductions_preserve_authority_boundaries() -> None:
    for item in SURFACE_DELTAS:
        assert item.candidate_only is True
        assert item.canonical_mutation is False
        assert item.business_operation is False
        assert item.candidate_introduction


def test_dynamic_mcp_and_webhook_boundaries_are_not_authorization() -> None:
    mcp = get_surface_delta("HERMES-MCP-DYNAMIC")
    webhook = get_surface_delta("HERMES-WEBHOOK-GUARD")
    assert "authorized" in mcp.candidate_introduction
    assert "trusted" in webhook.candidate_introduction


def test_existing_candidate_owners_are_reused() -> None:
    assert get_surface_delta("HERMES-DELEGATION-CONTROLS").elo_owner == "ELO Agent Delegation"
    assert get_surface_delta("HERMES-PROFILE-ISOLATION").elo_owner == "ELO Agent Context & Delegation"
    assert get_surface_delta("HERMES-SKILL-LIFECYCLE").elo_owner == "ELO Knowledge & Skills"
