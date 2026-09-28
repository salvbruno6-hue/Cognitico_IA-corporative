"""Harness de Teste do ELO — orquestrador de validação.

Compõe os 4 harnesses existentes + valida módulos Core.
Não substitui nenhum harness. Não cria autoridade paralela.

Refs: ELO_TEST_HARNESS_CONTRACT.
"""
from __future__ import annotations

import importlib
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


@dataclass
class HarnessResult:
    name: str
    status: str
    duration: float
    detail: str = ""
    error: str | None = None


@dataclass
class ModuleResult:
    name: str
    status: str
    error: str | None = None


@dataclass
class TestHarnessReport:
    overall: str
    harnesses: list[HarnessResult] = field(default_factory=list)
    modules: list[ModuleResult] = field(default_factory=list)
    duration: float = 0.0
    timestamp: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "overall": self.overall,
            "duration": self.duration,
            "timestamp": self.timestamp,
            "harnesses": [h.__dict__ for h in self.harnesses],
            "modules": [m.__dict__ for m in self.modules],
        }


class TestHarness:
    """Orquestrador de validação integrada do ELO."""

    def __init__(self) -> None:
        self._harnesses: list[tuple[str, Callable[[], None]]] = []

    def register_harness(
        self, name: str, runner: Callable[[], None]
    ) -> None:
        self._harnesses.append((name, runner))

    def run(self) -> TestHarnessReport:
        start = time.time()
        report = TestHarnessReport(
            overall="PASS",
            timestamp=start,
        )

        with tempfile.TemporaryDirectory(
            prefix="test_harness_"
        ) as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "memory" / "cognitive").mkdir(
                parents=True, exist_ok=True
            )
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp_path)
                self._run_all(report)
            finally:
                os.chdir(original_cwd)

        report.duration = time.time() - start
        report.overall = self._compute_overall(report)
        return report

    def _run_all(self, report: TestHarnessReport) -> None:
        for name, runner in self._harnesses:
            t0 = time.time()
            try:
                runner()
                report.harnesses.append(HarnessResult(
                    name=name,
                    status="PASS",
                    duration=time.time() - t0,
                ))
            except Exception as exc:
                report.harnesses.append(HarnessResult(
                    name=name,
                    status="FAIL",
                    duration=time.time() - t0,
                    error=str(exc),
                ))

        modules_to_check = [
            ("elo.core.decision_outcome_loop", "DecisionLifecycle"),
            ("elo.core.calibration", "ConfidenceCalibration"),
            ("elo.core.precedent_index", "PrecedentIndex"),
            ("elo.core.software_engineering", "EngineeringCycle"),
        ]

        for module_name, symbol in modules_to_check:
            try:
                mod = importlib.import_module(module_name)
                getattr(mod, symbol)
                report.modules.append(ModuleResult(
                    name=f"{module_name}.{symbol}",
                    status="AVAILABLE",
                ))
            except Exception as exc:
                report.modules.append(ModuleResult(
                    name=f"{module_name}.{symbol}",
                    status="MISSING",
                    error=str(exc),
                ))

    @staticmethod
    def _compute_overall(report: TestHarnessReport) -> str:
        if any(h.status == "FAIL" for h in report.harnesses):
            return "FAIL"
        if any(m.status != "AVAILABLE" for m in report.modules):
            return "BLOCKED"
        return "PASS"


__all__ = [
    "HarnessResult",
    "ModuleResult",
    "TestHarness",
    "TestHarnessReport",
]
