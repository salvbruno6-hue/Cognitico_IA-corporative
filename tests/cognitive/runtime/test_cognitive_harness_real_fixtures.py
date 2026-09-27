"""Testes do harness cognitivo com fixtures de experiências reais.

Cada teste roda o CRL completo com fixture derivada de experiência real persistida
no Supabase (via auditoria). O runtime não consulta Supabase.
"""
from __future__ import annotations

from pathlib import Path

from elo.cognitive.runtime.cognitive_harness import CognitiveHarness
from .fixtures.harness_experiences import (
    ALL_FIXTURES, so_001_26_confere, so_001_26_trelica,
    so_162_26_confere, so_162_26_layout,
    so_178_26_confere, so_178_26_rastreabilidade,
)


def _assert_complete(report) -> None:
    assert len(report.stage_order) == 10
    assert len(report.audit) == 10
    assert all(item["status"] == "ok" for item in report.audit)
    assert report.metrics["completed_stage_count"] == 10
    assert report.metrics["error_stage_count"] == 0
    assert report.metrics["skipped_stage_count"] == 0
    assert report.human_response


def test_so_001_26_trelica_returns_learning():
    report = CognitiveHarness().run(so_001_26_trelica())
    _assert_complete(report)
    assert report.delta["so_id"] == "SO 001.26"
    assert "001-26" in report.request_id


def test_so_162_26_layout_returns_learning():
    report = CognitiveHarness().run(so_162_26_layout())
    _assert_complete(report)
    assert report.delta["so_id"] == "SO 162.26"
    assert "162-26" in report.request_id


def test_so_178_26_rastreabilidade_returns_learning():
    report = CognitiveHarness().run(so_178_26_rastreabilidade())
    _assert_complete(report)
    assert report.delta["so_id"] == "SO 178.26"
    assert "178-26" in report.request_id


def test_so_001_26_confere_produces_delta():
    report = CognitiveHarness().run(so_001_26_confere())
    _assert_complete(report)
    assert isinstance(report.delta.get("aligned"), list)
    assert isinstance(report.delta.get("improvements"), list)


def test_so_162_26_confere_produces_delta():
    report = CognitiveHarness().run(so_162_26_confere())
    _assert_complete(report)
    assert report.delta["so_id"] == "SO 162.26"


def test_so_178_26_confere_produces_delta():
    report = CognitiveHarness().run(so_178_26_confere())
    _assert_complete(report)
    assert report.delta["so_id"] == "SO 178.26"


def test_all_fixtures_run_without_error():
    harness = CognitiveHarness()
    for name, factory in ALL_FIXTURES.items():
        report = harness.run(factory())
        assert report.metrics["error_stage_count"] == 0, f"Fixture {name} retornou error: {report.audit}"


def test_all_fixtures_produce_human_response():
    harness = CognitiveHarness()
    for name, factory in ALL_FIXTURES.items():
        report = harness.run(factory())
        assert report.human_response
        assert len(report.human_response) > 10


def test_fixtures_are_isolated_from_production():
    prod_memory = Path("memory/cognitive")
    before = list(prod_memory.rglob("*")) if prod_memory.exists() else []
    harness = CognitiveHarness()
    for factory in ALL_FIXTURES.values():
        harness.run(factory())
    after = list(prod_memory.rglob("*")) if prod_memory.exists() else []
    assert before == after, "Fixtures escreveram em produção"


def test_fixtures_are_deterministic():
    harness = CognitiveHarness()
    for factory in ALL_FIXTURES.values():
        first = harness.run(factory())
        second = harness.run(factory())
        assert first.stage_order == second.stage_order
        assert first.audit == second.audit
        assert first.delta == second.delta
        assert first.human_response == second.human_response
