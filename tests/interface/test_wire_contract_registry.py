from elo.interface.wire_contract_registry import (
    REGISTRY_VERSION,
    build_wire_contract_registry,
    validate_wire_contract_registry,
)


def test_registry_reuses_existing_interface_contracts():
    registry = validate_wire_contract_registry()

    assert {item.name for item in registry} == {
        "CognitiveRequest",
        "CognitiveResponse",
        "ErrorContract",
    }
    assert all(item.version == REGISTRY_VERSION for item in registry)
    assert all(item.transport == "HTTP/JSON" for item in registry)


def test_schema_evidence_is_deterministic():
    first = build_wire_contract_registry()
    second = build_wire_contract_registry()

    assert first == second
    assert all(len(item.schema_digest) == 64 for item in first)


def test_registry_is_observational_only():
    registry = build_wire_contract_registry()

    assert registry
    assert not any(item.name == "JSONRPC" for item in registry)
