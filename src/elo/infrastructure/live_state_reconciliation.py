"""Harness de Reconciliação Live.

Confronta estado esperado (declarado em YAML) com estado live
(fornecido por um reader). Produz PASS / DRIFT / UNKNOWN /
BLOCKED.

Read-only. Nunca corrige. Nunca executa DDL.

Refs: ELO_LIVE_STATE_RECONCILIATION_CONTRACT.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Protocol

import yaml


DEFAULT_EXPECTED_STATE = Path(
    "09-governance/contracts/expected_state/supabase_rls.yaml"
)


class ReconciliationStatus(str, Enum):
    PASS = "PASS"
    DRIFT = "DRIFT"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class RLSLiveState:
    """Estado live de RLS para uma tabela."""
    table: str
    rls_enabled: bool | None
    policies: tuple[str, ...] = ()
    read_error: str | None = None


@dataclass(frozen=True)
class TableReconciliation:
    """Resultado do confronto para uma tabela."""
    table: str
    status: ReconciliationStatus
    expected_rls: bool
    live_rls: bool | None
    expected_policies: tuple[str, ...]
    live_policies: tuple[str, ...]
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "table": self.table,
            "status": self.status.value,
            "expected_rls": self.expected_rls,
            "live_rls": self.live_rls,
            "expected_policies": list(self.expected_policies),
            "live_policies": list(self.live_policies),
            "reasons": list(self.reasons),
        }


@dataclass(frozen=True)
class ReconciliationReport:
    """Resultado consolidado do harness."""
    scope: str
    tables: tuple[TableReconciliation, ...]
    overall: ReconciliationStatus

    def to_dict(self) -> dict[str, Any]:
        return {
            "scope": self.scope,
            "overall": self.overall.value,
            "tables": [t.to_dict() for t in self.tables],
        }


class RLSStateReader(Protocol):
    """Contrato do reader de estado live.

    A implementação concreta (Supabase) vive em PR posterior.
    Nesta PR, apenas mocks implementam.
    """

    def read(self, table: str) -> RLSLiveState: ...


class LiveStateReconciliation:
    """Harness que confronta expected vs live para RLS."""

    def __init__(
        self,
        expected_state_path: Path = DEFAULT_EXPECTED_STATE,
    ) -> None:
        self._expected_path = expected_state_path

    def load_expected(self) -> dict[str, Any]:
        if not self._expected_path.exists():
            raise FileNotFoundError(
                f"Estado esperado não encontrado: "
                f"{self._expected_path}"
            )
        return yaml.safe_load(
            self._expected_path.read_text(encoding="utf-8")
        )

    def reconcile(
        self, reader: RLSStateReader
    ) -> ReconciliationReport:
        expected = self.load_expected()
        tables = expected.get("tables", [])

        results: list[TableReconciliation] = []
        for entry in tables:
            name = entry["name"]
            expected_rls = bool(entry.get("expected_rls", False))
            expected_policies = tuple(
                entry.get("policies", []) or ()
            )

            try:
                live = reader.read(name)
            except Exception as exc:
                results.append(TableReconciliation(
                    table=name,
                    status=ReconciliationStatus.BLOCKED,
                    expected_rls=expected_rls,
                    live_rls=None,
                    expected_policies=expected_policies,
                    live_policies=(),
                    reasons=(f"reader failed: {exc}",),
                ))
                continue

            if live.read_error is not None:
                results.append(TableReconciliation(
                    table=name,
                    status=ReconciliationStatus.BLOCKED,
                    expected_rls=expected_rls,
                    live_rls=None,
                    expected_policies=expected_policies,
                    live_policies=(),
                    reasons=(live.read_error,),
                ))
                continue

            if live.rls_enabled is None:
                results.append(TableReconciliation(
                    table=name,
                    status=ReconciliationStatus.UNKNOWN,
                    expected_rls=expected_rls,
                    live_rls=None,
                    expected_policies=expected_policies,
                    live_policies=live.policies,
                    reasons=("live state not available",),
                ))
                continue

            reasons: list[str] = []
            drift = False

            if live.rls_enabled != expected_rls:
                drift = True
                reasons.append(
                    f"RLS mismatch: expected={expected_rls}, "
                    f"live={live.rls_enabled}"
                )

            if expected_policies:
                live_set = set(live.policies)
                missing = [
                    p for p in expected_policies
                    if p not in live_set
                ]
                if missing:
                    drift = True
                    reasons.append(
                        f"missing policies: {missing}"
                    )

            status = (
                ReconciliationStatus.DRIFT if drift
                else ReconciliationStatus.PASS
            )

            results.append(TableReconciliation(
                table=name,
                status=status,
                expected_rls=expected_rls,
                live_rls=live.rls_enabled,
                expected_policies=expected_policies,
                live_policies=live.policies,
                reasons=tuple(reasons),
            ))

        overall = self._compute_overall(results)
        return ReconciliationReport(
            scope=expected.get("scope", "unknown"),
            tables=tuple(results),
            overall=overall,
        )

    @staticmethod
    def _compute_overall(
        results: list[TableReconciliation],
    ) -> ReconciliationStatus:
        if not results:
            return ReconciliationStatus.UNKNOWN
        statuses = {r.status for r in results}
        if ReconciliationStatus.BLOCKED in statuses:
            return ReconciliationStatus.BLOCKED
        if ReconciliationStatus.DRIFT in statuses:
            return ReconciliationStatus.DRIFT
        if ReconciliationStatus.UNKNOWN in statuses:
            return ReconciliationStatus.UNKNOWN
        return ReconciliationStatus.PASS


__all__ = [
    "LiveStateReconciliation",
    "ReconciliationReport",
    "ReconciliationStatus",
    "RLSLiveState",
    "RLSStateReader",
    "TableReconciliation",
]
