"""Testes do Harness de Teste."""
from __future__ import annotations

import pytest

from elo.testing.test_harness import TestHarness


def test_empty_harness_passes():
    h = TestHarness()
    report = h.run()
    assert report.overall == "PASS"
    assert len(report.harnesses) == 0


def test_harness_passing_registered():
    h = TestHarness()
    h.register_harness("always_pass", lambda: None)
    report = h.run()
    assert report.overall == "PASS"
    assert report.harnesses[0].status == "PASS"


def test_harness_failing_registered():
    h = TestHarness()

    def failing():
        raise RuntimeError("boom")

    h.register_harness("always_fail", failing)
    report = h.run()
    assert report.overall == "FAIL"
    assert report.harnesses[0].status == "FAIL"
    assert "boom" in (report.harnesses[0].error or "")


def test_harness_validates_core_modules():
    h = TestHarness()
    report = h.run()
    names = [m.name for m in report.modules]
    assert any("decision_outcome_loop" in n for n in names)
    assert any("calibration" in n for n in names)
    assert any("precedent_index" in n for n in names)
    assert any("software_engineering" in n for n in names)
    assert all(m.status == "AVAILABLE" for m in report.modules)


def test_report_is_serializable():
    h = TestHarness()
    h.register_harness("noop", lambda: None)
    report = h.run()
    serialized = report.to_dict()
    assert "overall" in serialized
    assert "harnesses" in serialized
    assert "modules" in serialized


def test_default_bootstrap_loads():
    from elo.testing.bootstrap import build_default_test_harness
    h = build_default_test_harness()
    report = h.run()
    assert report.overall in ("PASS", "FAIL", "BLOCKED")
    assert len(report.modules) == 4


def test_harness_is_isolated(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    h = TestHarness()
    h.register_harness("noop", lambda: None)
    report = h.run()
    assert report.overall == "PASS"
