"""Teste do script de execução do harness."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_cognitive_harness.py")


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        timeout=120,
    )


def test_list_fixtures():
    result = _run(["--list"])
    assert result.returncode == 0, result.stderr
    fixtures = json.loads(result.stdout)
    assert isinstance(fixtures, list)
    assert len(fixtures) >= 6


def test_run_single_fixture():
    result = _run(["so_001_26_trelica"])
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    assert output["fixture"] == "so_001_26_trelica"
    assert output["stages_completed"] == 10
    assert output["stages_error"] == 0
    assert output["stages_skipped"] == 0
    assert output["human_response"]
    assert output["delta_summary"]["so_id"] == "SO 001.26"
    assert output["isolated"] is True
    assert output["promotion_attempted"] is False
    assert output["governance_decision"] == "MEASUREMENT_ONLY"


def test_run_confere_fixture():
    result = _run(["so_162_26_confere"])
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    assert output["fixture"] == "so_162_26_confere"
    assert output["stages_completed"] == 10
    assert output["delta_summary"]["so_id"] == "SO 162.26"


def test_unknown_fixture_fails():
    result = _run(["so_999_99_invalid"])
    assert result.returncode == 2
    assert "Fixture desconhecida" in result.stderr


def test_no_args_prints_usage():
    result = _run([])
    assert result.returncode == 1
    assert "Uso:" in result.stderr
