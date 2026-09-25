from elo.integrations.enterprise.external_data import (
    ALLOWED_OPERATIONS,
    DEFAULT_READ_OPERATIONS,
    EXTERNAL_SOURCE_KINDS,
)


def test_external_contract_uses_single_governed_operation_vocabulary():
    assert ALLOWED_OPERATIONS == {
        "metadata_read",
        "read",
        "query",
        "write",
        "schema_change",
    }
    assert DEFAULT_READ_OPERATIONS == {"metadata_read", "read", "query"}


def test_external_contract_keeps_source_kinds_separate_from_elo_canonical():
    assert EXTERNAL_SOURCE_KINDS == {
        "ENTERPRISE_EXTERNAL",
        "USER_EXTERNAL",
        "INTEGRATION",
    }
    assert "ELO_CANONICAL" not in EXTERNAL_SOURCE_KINDS


def test_external_operations_are_not_cognitive_lifecycle_states():
    cognitive_states = {
        "proposed",
        "approved",
        "executed",
        "observing",
        "evaluated",
        "attributed",
        "learned",
        "closed",
        "escalated",
        "reverted",
    }
    assert ALLOWED_OPERATIONS.isdisjoint(cognitive_states)
