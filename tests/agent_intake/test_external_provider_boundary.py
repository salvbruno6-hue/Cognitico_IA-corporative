from elo.agent_intake.external_provider_boundary import classify_external_provider


def test_external_plugin_stays_adapter_under_existing_gateway_owner():
    decision = classify_external_provider({
        "provider_id": "github-copilot",
        "owner": "ELO External Capability Gateway",
        "boundary": "plugin",
        "authority": "execution_adapter",
    })
    assert decision.admitted is True
    assert decision.classification == "adapter"
    assert decision.reason == "bounded_external_provider"
    assert decision.canonical_mutation is False


def test_external_process_is_bounded_without_becoming_core():
    decision = classify_external_provider({
        "provider_id": "acp-agent",
        "owner": "ELO External Capability Gateway",
        "boundary": "external_process",
        "authority": "execution_adapter",
    })
    assert decision.admitted is True
    assert decision.classification == "adapter"
    assert decision.canonical_mutation is False


def test_incomplete_metadata_fails_closed():
    decision = classify_external_provider({"provider_id": "github-copilot", "boundary": "plugin"})
    assert decision.admitted is False
    assert decision.reason == "incomplete_provider_metadata"


def test_parallel_core_or_router_authority_is_rejected():
    for authority in ("core", "router", "routing", "memory", "evolution_gate"):
        decision = classify_external_provider({
            "provider_id": "external-provider",
            "owner": "ELO External Capability Gateway",
            "boundary": "plugin",
            "authority": authority,
        })
        assert decision.admitted is False
        assert decision.reason == "parallel_authority_forbidden"


def test_owner_mismatch_is_rejected():
    decision = classify_external_provider({
        "provider_id": "external-provider",
        "owner": "ELO Core",
        "boundary": "plugin",
        "authority": "execution_adapter",
    })
    assert decision.admitted is False
    assert decision.reason == "canonical_owner_mismatch"


def test_unknown_boundary_is_rejected():
    decision = classify_external_provider({
        "provider_id": "external-provider",
        "owner": "ELO External Capability Gateway",
        "boundary": "embedded_core",
        "authority": "execution_adapter",
    })
    assert decision.admitted is False
    assert decision.reason == "unsupported_provider_boundary"
