"""Testes do SOResolver."""
from __future__ import annotations

from pathlib import Path

import pytest

from elo.cognitive.runtime.knowledge.so_resolver import (
    SOResolver,
    normalize_so_id,
)


def test_normalize_so_id():
    assert normalize_so_id("SO 155.26") == "SO-155.26"
    assert normalize_so_id("so_155_26") == "SO-155-26"
    assert normalize_so_id(" SO  155.26 ") == "SO-155.26"


def test_resolver_finds_learning(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "04-knowledge-handbook").mkdir()
    (tmp_path / "memory" / "solicitations_learning").mkdir(parents=True)

    (tmp_path / "memory" / "solicitations_learning" / "INDEX.json").write_text(
        '{"solicitations":[{"so_id":"SO-155.26",'
        '"canonical_key":"SO_155_26",'
        '"path":"SO-155.26.md",'
        '"domain":"orcamento",'
        '"tags":["modulos","manutencao"],'
        '"summary":"test"}]}',
        encoding="utf-8",
    )
    (tmp_path / "04-knowledge-handbook" / "INDEX.json").write_text(
        '{"documents":[{"id":"KB-1","path":"a.md","title":"A",'
        '"domain":"orcamento","tags":["modulos"],"summary":"x"}]}',
        encoding="utf-8",
    )

    resolver = SOResolver(
        handbook_index=tmp_path / "04-knowledge-handbook" / "INDEX.json",
        learning_index=tmp_path / "memory" / "solicitations_learning" / "INDEX.json",
    )
    result = resolver.resolve("SO 155.26")

    assert result["so_id"] == "SO-155.26"
    assert result["learning"] is not None
    assert result["learning"]["so_id"] == "SO-155.26"
    assert len(result["handbook"]) == 1
