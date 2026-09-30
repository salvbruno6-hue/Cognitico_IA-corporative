"""Runtime integration tests for the governed Hermes Context Plugin candidate."""
from __future__ import annotations

from elo.cognitive.runtime.crl import CRLContext
from elo.cognitive.runtime.handlers import contextualize


class _FakeResolver:
    def resolve(self, so_id: str, **kwargs) -> dict:
        assert so_id == "SO-155.26"
        assert kwargs["tenant_id"] == "tenant-a"
        assert kwargs["domain"] == "orcamento"
        return {
            "so_id": "SO-155.26",
            "canonical_key": "SO_155_26",
            "mask": "SO NNN.AA",
            "tenant_id": "tenant-a",
            "domain": "orcamento",
            "learning": None,
            "handbook": [],
            "precedents": [],
            "context_keys": [],
            "dossier": {
                "so_id": "SO-155.26",
                "canonical_key": "SO_155_26",
                "maturation_state": "IDENTIFIED",
                "scope_state": "SCOPED",
                "source_refs": [],
            },
        }


class _FakeIndex:
    def find(self, **kwargs):
        return []


class _FakeStore:
    def load(self):
        return _FakeIndex()


def test_contextualize_exposes_so_dossier(monkeypatch) -> None:
    monkeypatch.setattr(contextualize, "SOResolver", _FakeResolver)

    ctx = CRLContext(
        request_id="req-1",
        payload={
            "so_id": "SO-155.26",
            "tenant_id": "tenant-a",
            "domain": "orcamento",
        },
    )
    result = contextualize.contextualize_handler(ctx)

    assert result.stage_results["so_context"]["so_id"] == "SO-155.26"
    assert result.stage_results["so_dossier"]["canonical_key"] == "SO_155_26"


def test_contextualize_preserves_canonical_path_without_hermes(monkeypatch) -> None:
    monkeypatch.setattr(contextualize, "PrecedentStore", _FakeStore)

    ctx = CRLContext(
        request_id="req-no-hermes",
        payload={
            "tenant_id": "tenant-a",
            "domain": "orcamento",
            "context_keys": (),
        },
    )

    result = contextualize.contextualize_handler(ctx)

    assert result.stage_results["precedents"] == []
    assert "hermes_context_plugin" not in result.stage_results
    assert "hermes_context_pack" not in result.stage_results


def test_contextualize_enriches_real_runtime_with_explicit_hermes_signal(monkeypatch) -> None:
    monkeypatch.setattr(contextualize, "PrecedentStore", _FakeStore)

    ctx = CRLContext(
        request_id="req-hermes",
        payload={
            "tenant_id": "tenant-a",
            "domain": "orcamento",
            "context_question": "consultar contexto do orçamento",
            "hermes_context_plugin": {
                "signal_id": "signal-001",
                "tenant_scope": "tenant-a",
                "plugin_id": "plugin-context-001",
                "engine_name": "hermes-context-engine",
                "source_refs": ["hermes://evidence/001"],
                "explicit_activation": True,
                "provenance_verified": True,
            },
        },
    )

    result = contextualize.contextualize_handler(ctx)

    plugin = result.stage_results["hermes_context_plugin"]
    assert plugin["adapted"] is True
    assert plugin["disposition"] == "CANDIDATE"
    assert plugin["canonical_authority"] is False

    pack = result.stage_results["hermes_context_pack"]
    assert pack.query.tenant_id == "tenant-a"
    assert pack.sources[0].authority == "ELO Context"
    assert pack.sources[0].tenant_id == "tenant-a"


def test_contextualize_rejects_cross_tenant_hermes_signal(monkeypatch) -> None:
    monkeypatch.setattr(contextualize, "PrecedentStore", _FakeStore)

    ctx = CRLContext(
        request_id="req-cross-tenant",
        payload={
            "tenant_id": "tenant-a",
            "domain": "orcamento",
            "hermes_context_plugin": {
                "signal_id": "signal-002",
                "tenant_scope": "tenant-b",
                "plugin_id": "plugin-context-002",
                "engine_name": "hermes-context-engine",
                "source_refs": ["hermes://evidence/002"],
                "explicit_activation": True,
                "provenance_verified": True,
            },
        },
    )

    try:
        contextualize.contextualize_handler(ctx)
    except ValueError as exc:
        assert "tenant" in str(exc)
    else:
        raise AssertionError("cross-tenant Hermes signal must fail closed")
