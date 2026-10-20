import pytest

from elo.cognitive.agents.hermes_skill_runtime import (
    IntentSpec,
    build_governed_skill_execution_envelope,
)
from elo.cognitive.symbiont_governance_contract import MandateAcknowledgement


def intent() -> IntentSpec:
    return IntentSpec(
        request_id="req-1",
        intent="consult external data",
        tenant_scope="tenant-a",
        mission_class="consultative",
        authorized_capabilities=("external_data_query",),
        evidence_requirements=("execution",),
    )


def ack(**overrides: object) -> MandateAcknowledgement:
    values = {
        "request_id": "req-1",
        "identity_id": "identity-1",
        "tenant_scope": "tenant-a",
        "mandate_version": "1.0",
        "acknowledged": True,
    }
    values.update(overrides)
    return MandateAcknowledgement(**values)


def test_governed_envelope_requires_matching_ack() -> None:
    payload = build_governed_skill_execution_envelope(intent(), acknowledgement=ack())
    assert payload["governance"]["mandate_acknowledged"] is True
    assert payload["governance"]["operation"] == "query"


def test_governed_envelope_rejects_ack_from_other_request_or_tenant() -> None:
    with pytest.raises(ValueError, match="request_id"):
        build_governed_skill_execution_envelope(
            intent(), acknowledgement=ack(request_id="other")
        )
    with pytest.raises(ValueError, match="tenant scope"):
        build_governed_skill_execution_envelope(
            intent(), acknowledgement=ack(tenant_scope="tenant-b")
        )


def test_governed_envelope_rejects_pii_and_canonical_mutation() -> None:
    with pytest.raises(ValueError, match="PII"):
        build_governed_skill_execution_envelope(
            intent(), acknowledgement=ack(), pii_exposure=True
        )
    with pytest.raises(ValueError, match="canonical mutation"):
        build_governed_skill_execution_envelope(
            intent(), acknowledgement=ack(), operation="write", canonical_mutation=True
        )
