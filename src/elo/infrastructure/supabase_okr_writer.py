"""Backend-only Supabase write adapter for strategic OKR persistence.

Layer: infrastructure
Owner: strategic-objective-domain persistence
Authority: none; authorization must be validated by GovernedOkrWriter first.

The adapter uses service credentials only as a transport credential. It does not
interpret roles, capabilities, scopes or identity. It writes only the approved
Objective/KR/binding owners and never mutates KPI definitions or snapshots.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from elo.application.commands.okr_write import SnapshotBindingWrite
from elo.contracts.okr import KeyResult, Objective


DEFAULT_TIMEOUT = 15.0
OBJECTIVE_TABLE = "elo_strategic_objectives"
KEY_RESULT_TABLE = "elo_strategic_key_results"
BINDING_TABLE = "elo_strategic_kr_snapshot_bindings"


class SupabaseOkrWriteRepository:
    def __init__(self, url: str, service_role_key: str, timeout: float = DEFAULT_TIMEOUT) -> None:
        if not url.strip():
            raise ValueError("Supabase URL is required")
        if not service_role_key.strip():
            raise ValueError("Supabase service_role_key is required")
        self._url = url.rstrip("/")
        self._key = service_role_key
        self._timeout = timeout

    def upsert_objective(self, objective: Objective, *, authorization_ref: str) -> None:
        self._required(authorization_ref, "authorization_ref")
        self._post(
            OBJECTIVE_TABLE,
            {
                "tenant_id": objective.tenant_id,
                "objective_id": objective.objective_id,
                "title": objective.title,
                "strategy_ref": objective.strategy_ref,
                "owner_ref": objective.owner_ref,
                "evidence_refs": list(objective.evidence_refs),
            },
            on_conflict="tenant_id,objective_id",
        )

    def upsert_key_result(self, key_result: KeyResult, *, authorization_ref: str) -> None:
        self._required(authorization_ref, "authorization_ref")
        self._post(
            KEY_RESULT_TABLE,
            {
                "tenant_id": key_result.tenant_id,
                "key_result_id": key_result.key_result_id,
                "objective_id": key_result.objective_id,
                "title": key_result.title,
                "metric_code": key_result.metric_code,
                "direction": key_result.direction.value,
                "baseline": str(key_result.baseline) if key_result.baseline is not None else None,
                "target": str(key_result.target) if key_result.target is not None else None,
                "deadline": key_result.deadline.isoformat() if key_result.deadline else None,
                "weight": str(key_result.weight),
                "baseline_evidence_refs": list(key_result.baseline_evidence_refs),
                "target_evidence_refs": list(key_result.target_evidence_refs),
                "target_approval_state": key_result.target_approval_state.value,
                "target_approval_ref": key_result.target_approval_ref,
            },
            on_conflict="tenant_id,key_result_id",
        )

    def bind_snapshot(self, binding: SnapshotBindingWrite, *, authorization_ref: str) -> None:
        self._required(authorization_ref, "authorization_ref")
        self._post(
            BINDING_TABLE,
            {
                "tenant_id": binding.tenant_id,
                "key_result_id": binding.key_result_id,
                "snapshot_id": binding.snapshot_id,
                "evidence_refs": list(binding.evidence_refs),
            },
            on_conflict="tenant_id,key_result_id,snapshot_id",
        )

    def _post(self, table: str, payload: dict[str, Any], *, on_conflict: str) -> None:
        query = urllib.parse.urlencode({"on_conflict": on_conflict}, safe=",")
        request = urllib.request.Request(
            f"{self._url}/rest/v1/{table}?{query}",
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "apikey": self._key,
                "Authorization": f"Bearer {self._key}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates,return=minimal",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                response.read()
        except urllib.error.HTTPError as exc:
            detail = ""
            try:
                detail = exc.read().decode("utf-8")
            except Exception:
                pass
            raise RuntimeError(f"Supabase OKR write failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Supabase OKR write failed: network error: {exc}") from exc

    @staticmethod
    def _required(value: str, field_name: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{field_name} is required")
        return normalized


__all__ = ["SupabaseOkrWriteRepository"]
