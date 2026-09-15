"""EVO-03: immutable historical evidence, append-only follow-up and replay."""

from datetime import UTC, datetime

import pytest

from elo.memory.persistent import MemoryAdmissionError, MemoryRecord, PersistentMemoryStore


def _historical() -> MemoryRecord:
    return MemoryRecord(
        memory_id="H-EVO03-001",
        tenant_id="tenant-lab",
        domain="operations",
        principal_id="evo03-lab",
        content="decision based on verified evidence",
        source_id="evidence:EVO03-001",
        provenance={"source": "github-actions", "captured_at": datetime.now(UTC).isoformat()},
        created_at=1_000.0,
        expires_at=1_001.0,
        kind="historical",
    )


def test_evo03_history_is_immutable_and_replayable():
    store = PersistentMemoryStore()
    root = _historical()
    store.admit(root)

    with pytest.raises(MemoryAdmissionError, match="historical record is immutable"):
        store.admit(root)

    follow_up = store.append_follow_up(
        root,
        content="follow-up confirmed the original decision",
        source_id="evidence:EVO03-002",
        provenance={"source": "github-actions"},
    )

    replay = store.replay_history(root.memory_id, tenant_id=root.tenant_id, domain=root.domain)
    assert replay == (root, follow_up)
    assert replay[0] == root
    assert replay[0].content == "decision based on verified evidence"
    assert replay[1].provenance["follows_memory_id"] == root.memory_id

    assert store.purge_expired(tenant_id=root.tenant_id) == 0
    assert store.get(root.memory_id, tenant_id=root.tenant_id, domain=root.domain) == root

    store.close()


def test_evo03_replay_is_tenant_and_domain_scoped():
    store = PersistentMemoryStore()
    root = _historical()
    store.admit(root)
    other = MemoryRecord(
        memory_id="H-EVO03-002",
        tenant_id="other-tenant",
        domain="operations",
        principal_id="other",
        content="unrelated history",
        source_id="evidence:OTHER",
        provenance={"source": "github-actions"},
        created_at=1_000.0,
        kind="historical",
    )
    store.admit(other)

    assert store.replay_history(root.memory_id, tenant_id="other-tenant", domain="operations") == ()
    assert store.replay_history(root.memory_id, tenant_id=root.tenant_id, domain="other-domain") == ()
    store.close()
