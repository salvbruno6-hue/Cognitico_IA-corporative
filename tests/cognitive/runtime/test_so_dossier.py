"""Testes do índice governado SODossier."""
from __future__ import annotations

import json
from pathlib import Path

from elo.cognitive.runtime.knowledge.so_dossier import SODossier


def test_dossier_references_sources_without_copying_content(tmp_path: Path) -> None:
    learning = {
        "so_id": "SO-155.26",
        "canonical_key": "SO_155_26",
        "path": "SO-155.26.md",
        "tags": ["modulos", "manutencao"],
    }

    handbook = [
        {
            "id": "KB-1",
            "path": "04-knowledge-handbook/example.md",
            "tags": ["modulos"],
        }
    ]

    (tmp_path / "SO-155.26.md").write_text("aprendizado secreto", encoding="utf-8")
    (tmp_path / "04-knowledge-handbook").mkdir()
    (tmp_path / "04-knowledge-handbook/example.md").write_text(
        "conteudo do handbook", encoding="utf-8"
    )

    dossier = SODossier.from_resolved_context(
        so_id="SO-155.26",
        canonical_key="SO_155_26",
        learning=learning,
        handbook=handbook,
        context_keys=("modulos", "manutencao"),
        repository_root=tmp_path,
        tenant_id="tenant-a",
        domain="orcamento",
    )

    payload = dossier.to_dict()
    serialized = json.dumps(payload, ensure_ascii=False)

    assert payload["so_id"] == "SO-155.26"
    assert payload["canonical_key"] == "SO_155_26"
    assert payload["maturation_state"] == "REFERENCED"
    assert payload["scope_state"] == "SCOPED"
    assert payload["tenant_id"] == "tenant-a"
    assert payload["domain"] == "orcamento"
    assert "aprendizado secreto" not in serialized
    assert "conteudo do handbook" not in serialized
    assert all(
        ref["applicability"] == "CONSULTIVE"
        for ref in payload["source_refs"]
    )
    assert any(
        ref["source_type"] == "supabase_experience"
        and ref["table"] == "elo_aprendizado_experiencias"
        for ref in payload["source_refs"]
    )


def test_dossier_marks_unknown_scope_without_inference(tmp_path: Path) -> None:
    dossier = SODossier.from_resolved_context(
        so_id="SO-155.26",
        canonical_key="SO_155_26",
        learning=None,
        handbook=[],
        repository_root=tmp_path,
    )
    assert dossier.to_dict()["scope_state"] == "UNKNOWN"


def test_dossier_uses_operational_memory_reference(tmp_path: Path) -> None:
    path = tmp_path / "memory" / "solicitations" / "SO_155_26"
    path.mkdir(parents=True)
    (path / "index.json").write_text("{}", encoding="utf-8")

    dossier = SODossier.from_resolved_context(
        so_id="SO-155.26",
        canonical_key="SO_155_26",
        learning=None,
        handbook=[],
        repository_root=tmp_path,
    )

    refs = dossier.to_dict()["source_refs"]
    operational = next(
        ref for ref in refs if ref["source_type"] == "operational_memory"
    )
    assert operational["path"] == "memory/solicitations/SO_155_26/index.json"
    assert operational["exists"] is True
