import pytest

from elo.cognitive.symbiont_external_provider_contracts import (
    EvolutionDisposition,
    ExternalCapabilityOutcome,
    ExternalCapabilityProbe,
    ExternalProviderContract,
    ProviderProtocol,
    ProviderStatus,
)


def test_provider_contract_is_provider_neutral_and_governed():
    contract = ExternalProviderContract(
        provider_id="openai:reasoning",
        provider="openai",
        capability="reasoning",
        protocol=ProviderProtocol.API,
        status=ProviderStatus.NOT_PROVISIONED,
        purpose="optional external reasoning capability",
        source_ref="https://openai.com/api",
        tenant_id="multiteiner",
        domain="cognitive",
        execution_allowed=True,
        cost_model="metered",
    )
    assert contract.canonical_mutation_allowed is False
    assert contract.evidence_required is True
    assert contract.evolution_gate_required is True


def test_hermes_can_be_registered_as_runtime_provider():
    contract = ExternalProviderContract(
        provider_id="hermes:runtime",
        provider="hermes",
        capability="runtime_execution",
        protocol=ProviderProtocol.MCP,
        status=ProviderStatus.CONNECTED,
        purpose="governed external runtime execution",
        source_ref="hermes-runtime",
        tenant_id="multiteiner",
        domain="runtime",
        execution_allowed=True,
    )
    assert contract.provider == "hermes"
    assert contract.protocol is ProviderProtocol.MCP


def test_probe_is_read_only_and_bounded_by_default():
    probe = ExternalCapabilityProbe(
        probe_id="probe-001",
        provider_id="openai:reasoning",
        capability="reasoning",
        request_id="req-001",
        tenant_id="multiteiner",
        objective="validate an external reasoning response",
        input_payload={"task": "classify controlled fixture"},
        success_criteria=("returns structured result",),
        evidence_requirements=("execution", "outcome"),
    )
    assert probe.read_only is True
    assert probe.bounded is True
    assert probe.max_calls == 1


def test_outcome_requires_evidence_and_stays_candidate_only():
    outcome = ExternalCapabilityOutcome(
        probe_id="probe-001",
        provider_id="openai:reasoning",
        request_id="req-001",
        tenant_id="multiteiner",
        success=True,
        evidence_ids=("ev-001", "ev-002"),
        outcome={"quality": "acceptable"},
        disposition=EvolutionDisposition.LAB_CANDIDATE,
    )
    assert outcome.candidate_only is True


def test_contract_rejects_credentials():
    with pytest.raises(ValueError, match="credential/secret"):
        ExternalProviderContract(
            provider_id="bad:provider",
            provider="external",
            capability="x",
            protocol=ProviderProtocol.API,
            status=ProviderStatus.AVAILABLE,
            purpose="test",
            source_ref="test",
            tenant_id="multiteiner",
            domain="test",
            metadata={"api_key": "never-store-here"},
        )


def test_external_provider_cannot_disable_governance():
    with pytest.raises(ValueError, match="governance controls"):
        ExternalProviderContract(
            provider_id="bad:provider",
            provider="external",
            capability="x",
            protocol=ProviderProtocol.API,
            status=ProviderStatus.AVAILABLE,
            purpose="test",
            source_ref="test",
            tenant_id="multiteiner",
            domain="test",
            evidence_required=False,
        )


def test_outcome_cannot_be_directly_promoted():
    with pytest.raises(ValueError, match="cannot be directly promoted"):
        ExternalCapabilityOutcome(
            probe_id="probe-002",
            provider_id="github:repository",
            request_id="req-002",
            tenant_id="multiteiner",
            success=True,
            evidence_ids=("ev-003",),
            outcome={"result": "ok"},
            candidate_only=False,
        )
