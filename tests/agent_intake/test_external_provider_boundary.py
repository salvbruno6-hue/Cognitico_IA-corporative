from elo.agent_intake.external_provider_boundary import classify_external_provider


def valid_provider(**overrides):
    metadata = {
        "provider_id": "external-provider",
        "owner": "ELO External Capability Gateway",
        "boundary": "plugin",
        "authority": "execution_adapter",
    }
    metadata.update(overrides)
    return metadata


def test_external_plugin_stays_adapter_under_existing_gateway_owner():
    decision = classify_external_provider(valid_provider(provider_id="github-copilot"))
    assert decision.admitted is True
    assert decision.classification == "adapter"
    assert decision.reason == "bounded_external_provider"
    assert decision.canonical_mutation is False


def test_external_process_is_bounded_without_becoming_core():
    decision = classify_external_provider(valid_provider(provider_id="acp-agent", boundary="external_process"))
    assert decision.admitted is True
    assert decision.classification == "adapter"
    assert decision.canonical_mutation is False


def test_incomplete_metadata_fails_closed():
    decision = classify_external_provider({"provider_id": "github-copilot", "boundary": "plugin"})
    assert decision.admitted is False
    assert decision.reason == "incomplete_or_malformed_provider_metadata"


def test_malformed_provider_identity_types_fail_closed():
    for provider_id in (True, 123, {"unexpected": "object"}, ["provider"]):
        decision = classify_external_provider(valid_provider(provider_id=provider_id))
        assert decision.admitted is False
        assert decision.reason == "incomplete_or_malformed_provider_metadata"


def test_parallel_core_or_router_authority_is_rejected():
    for authority in ("core", "router", "routing", "memory", "evolution_gate"):
        decision = classify_external_provider(valid_provider(authority=authority))
        assert decision.admitted is False
        assert decision.reason == "parallel_authority_forbidden"


def test_malformed_authority_types_fail_closed():
    for authority in (["core"], {"core": True}, True, 123):
        decision = classify_external_provider(valid_provider(authority=authority))
        assert decision.admitted is False
        assert decision.reason == "incomplete_or_malformed_provider_metadata"


def test_missing_or_unknown_authority_is_rejected():
    missing = valid_provider()
    missing.pop("authority")
    decision = classify_external_provider(missing)
    assert decision.admitted is False
    assert decision.reason == "incomplete_or_malformed_provider_metadata"

    decision = classify_external_provider(valid_provider(authority="provider_owned"))
    assert decision.admitted is False
    assert decision.reason == "unsupported_provider_authority"


def test_owner_mismatch_is_rejected():
    decision = classify_external_provider(valid_provider(owner="ELO Core"))
    assert decision.admitted is False
    assert decision.reason == "canonical_owner_mismatch"


def test_unknown_boundary_is_rejected():
    decision = classify_external_provider(valid_provider(boundary="embedded_core"))
    assert decision.admitted is False
    assert decision.reason == "unsupported_provider_boundary"
