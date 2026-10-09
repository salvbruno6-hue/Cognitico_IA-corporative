"""Read-only Supabase adapter for the approved strategic Objective/KR owners.

Layer: infrastructure
Owner: strategic-objective-domain
Status: prepared
Authority: implementation
Related: OkrReadRepository, elo_strategic_objectives, elo_strategic_key_results

This adapter is intentionally backend/service-bound. It never authorizes a tenant;
the caller must pass a tenant scope already resolved by the canonical ELO authz
boundary. Every read includes tenant_id and returned rows are checked again.

Measurement persistence is intentionally not implemented. Until a governed
Measurement<->KR binding is approved, list_measurements() fails closed by
returning an empty tuple instead of inferring rows from mt_snapshots_kpi.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from decimal import Decimal
from typing import Any

from elo.contracts.okr import (
    KeyResult,
    KeyResultDirection,
    Measurement,
    Objective,
    TargetApprovalState,
)


DEFAULT_TIMEOUT = 15.0
OBJECTIVE_TABLE = "elo_strategic_objectives"
KEY_RESULT_TABLE = "elo_strategic_key_results"


class SupabaseOkrReadRepository:
    """Implement OkrReadRepository over backend-only Supabase REST reads.

    The service-role credential is accepted only by backend construction. It
    must never be exposed to a browser/client. The repository itself owns no
    authorization decision and never broadens the requested tenant scope.
    """

    def __init__(
        self,
        url: str,
        service_role_key: str,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        if not url.strip():
            raise ValueError("Supabase URL is required")
        if not service_role_key.strip():
            raise ValueError("Supabase service_role_key is required")
        self._url = url.rstrip("/")
        self._key = service_role_key
        self._timeout = timeout

    def get_objective(self, *, tenant_id: str, objective_id: str) -> Objective | None:
        tenant = self._required(tenant_id, "tenant_id")
        objective = self._required(objective_id, "objective_id")
        rows = self._get_rows(
            OBJECTIVE_TABLE,
            {
                "select": "tenant_id,objective_id,title,strategy_ref,owner_ref,evidence_refs",
                "tenant_id": f"eq.{tenant}",
                "objective_id": f"eq.{objective}",
                "limit": "1",
            },
        )
        if not rows:
            return None
        row = rows[0]
        self._assert_tenant(tenant, row)
        return self._objective_from_row(row)

    def get_key_result(self, *, tenant_id: str, key_result_id: str) -> KeyResult | None:
        tenant = self._required(tenant_id, "tenant_id")
        key_result = self._required(key_result_id, "key_result_id")
        rows = self._get_rows(
            KEY_RESULT_TABLE,
            {
                "select": (
                    "tenant_id,key_result_id,objective_id,title,metric_code,direction,"
                    "baseline,target,deadline,weight,baseline_evidence_refs,"
                    "target_evidence_refs,target_approval_state,target_approval_ref"
                ),
                "tenant_id": f"eq.{tenant}",
                "key_result_id": f"eq.{key_result}",
                "limit": "1",
            },
        )
        if not rows:
            return None
        row = rows[0]
        self._assert_tenant(tenant, row)
        return self._key_result_from_row(row)

    def list_key_results(self, *, tenant_id: str, objective_id: str) -> tuple[KeyResult, ...]:
        tenant = self._required(tenant_id, "tenant_id")
        objective = self._required(objective_id, "objective_id")
        rows = self._get_rows(
            KEY_RESULT_TABLE,
            {
                "select": (
                    "tenant_id,key_result_id,objective_id,title,metric_code,direction,"
                    "baseline,target,deadline,weight,baseline_evidence_refs,"
                    "target_evidence_refs,target_approval_state,target_approval_ref"
                ),
                "tenant_id": f"eq.{tenant}",
                "objective_id": f"eq.{objective}",
                "order": "key_result_id.asc",
            },
        )
        results: list[KeyResult] = []
        for row in rows:
            self._assert_tenant(tenant, row)
            if str(row.get("objective_id") or "") != objective:
                raise PermissionError("Supabase OKR read returned a different Objective")
            results.append(self._key_result_from_row(row))
        return tuple(results)

    def list_measurements(self, *, tenant_id: str, key_result_id: str) -> tuple[Measurement, ...]:
        # Validate caller scope even though no storage read occurs. This method
        # deliberately does not infer Measurement from mt_snapshots_kpi.
        self._required(tenant_id, "tenant_id")
        self._required(key_result_id, "key_result_id")
        return ()

    def _get_rows(self, table: str, params: dict[str, str]) -> list[dict[str, Any]]:
        query = urllib.parse.urlencode(params, safe=".,()*")
        request = urllib.request.Request(
            f"{self._url}/rest/v1/{table}?{query}",
            method="GET",
            headers={
                "apikey": self._key,
                "Authorization": f"Bearer {self._key}",
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = ""
            try:
                detail = exc.read().decode("utf-8")
            except Exception:
                pass
            raise RuntimeError(f"Supabase OKR read failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Supabase OKR read failed: network error: {exc}") from exc

        if not raw:
            return []
        parsed = json.loads(raw)
        if not isinstance(parsed, list):
            raise RuntimeError("Supabase OKR read returned a non-list payload")
        return [item for item in parsed if isinstance(item, dict)]

    @staticmethod
    def _objective_from_row(row: dict[str, Any]) -> Objective:
        return Objective(
            tenant_id=str(row["tenant_id"]),
            objective_id=str(row["objective_id"]),
            title=str(row["title"]),
            strategy_ref=SupabaseOkrReadRepository._optional_text(row.get("strategy_ref")),
            owner_ref=SupabaseOkrReadRepository._optional_text(row.get("owner_ref")),
            evidence_refs=SupabaseOkrReadRepository._refs(row.get("evidence_refs")),
        )

    @staticmethod
    def _key_result_from_row(row: dict[str, Any]) -> KeyResult:
        deadline = row.get("deadline")
        return KeyResult(
            tenant_id=str(row["tenant_id"]),
            key_result_id=str(row["key_result_id"]),
            objective_id=str(row["objective_id"]),
            title=str(row["title"]),
            metric_code=str(row["metric_code"]),
            direction=KeyResultDirection(str(row["direction"])),
            baseline=SupabaseOkrReadRepository._decimal_or_none(row.get("baseline")),
            target=SupabaseOkrReadRepository._decimal_or_none(row.get("target")),
            deadline=date.fromisoformat(str(deadline)) if deadline else None,
            weight=Decimal(str(row.get("weight", 1))),
            baseline_evidence_refs=SupabaseOkrReadRepository._refs(row.get("baseline_evidence_refs")),
            target_evidence_refs=SupabaseOkrReadRepository._refs(row.get("target_evidence_refs")),
            target_approval_state=TargetApprovalState(str(row.get("target_approval_state", "DRAFT"))),
            target_approval_ref=SupabaseOkrReadRepository._optional_text(row.get("target_approval_ref")),
        )

    @staticmethod
    def _assert_tenant(expected: str, row: dict[str, Any]) -> None:
        observed = str(row.get("tenant_id") or "")
        if observed != expected:
            raise PermissionError("Supabase OKR data crossed the authorized tenant boundary")

    @staticmethod
    def _required(value: str, field_name: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{field_name} is required")
        return normalized

    @staticmethod
    def _refs(value: Any) -> tuple[str, ...]:
        if value is None:
            return ()
        if isinstance(value, (list, tuple)):
            return tuple(dict.fromkeys(str(item).strip() for item in value if str(item).strip()))
        raise ValueError("evidence refs must be an array")

    @staticmethod
    def _optional_text(value: Any) -> str | None:
        if value is None:
            return None
        normalized = str(value).strip()
        return normalized or None

    @staticmethod
    def _decimal_or_none(value: Any) -> Decimal | None:
        if value is None:
            return None
        return Decimal(str(value))


__all__ = ["SupabaseOkrReadRepository"]
