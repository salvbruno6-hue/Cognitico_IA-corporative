"""Integração do dossiê no estágio CONTEXTUALIZE."""
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
