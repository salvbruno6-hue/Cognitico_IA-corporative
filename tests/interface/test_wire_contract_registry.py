from elo.interface.wire_contract_registry import (
    REGISTRY_VERSION,
    TRANSPORT,
    build_wire_contract_registry,
    validate_wire_contract_registry,
)


def test_registry_reuses_existing_interface_contracts():
    registry = validate_wire_contract_registry()
    assert {item.name for item in registry} == {
        "CognitiveRequest", "CognitiveResponse", "ErrorContract"
    }
    assert all(item.version == REGISTRY_VERSION for item in registry)
    assert all(item.transport == TRANSPORT == "HTTP/JSON" for item in registry)
    assert all(item.canonical_owner == "elo.interface.contracts" for item in registry)


def test_schema_evidence_is_deterministic():
    first = build_wire_contract_registry()
    second = build_wire_contract_registry()
    assert first == second
    assert all(len(item.schema_digest) == 64 for item in first)
    assert all(set(item.schema_digest) <= set("0123456789abcdef") for item in first)


def test_registry_is_observational_only_and_fail_closed():
    registry = validate_wire_contract_registry()
    assert registry
    assert all(item.execution_permitted is False for item in registry)
    assert not any(item.name == "JSONRPC" for item in registry)
