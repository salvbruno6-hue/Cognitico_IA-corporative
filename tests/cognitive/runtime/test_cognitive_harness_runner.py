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
        timeout=60,
    )


def test_list_fixtures():
    result = _run(["--list"])
    assert result.returncode == 0
    fixtures = json.loads(result.stdout)
    assert isinstance(fixtures, list)
    assert len(fixtures) >= 6


def test_run_single_fixture():
    result = _run(["so_001_26_trelica"])
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    assert output["fixture"] == "so_001_26_trelica"
    assert output["status"] in ("success", "escalated")
    assert output["stages_executed"] == 10
    assert output["human_response"] is not None
    assert "001.26" in output["human_response"]


def test_run_confere_fixture():
    result = _run(["so_162_26_confere"])
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    assert output["fixture"] == "so_162_26_confere"
    assert output["status"] in ("success", "escalated")
    assert output["delta_summary"] is not None


def test_unknown_fixture_fails():
    result = _run(["so_999_99_invalid"])
    assert result.returncode == 2
    assert "Fixture desconhecida" in result.stderr


def test_no_args_prints_usage():
    result = _run([])
    assert result.returncode == 1
    assert "Uso:" in result.stderr
