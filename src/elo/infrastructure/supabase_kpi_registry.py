"""Read-only Supabase adapter for the canonical formal KPI registry."""
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Mapping


class SupabaseFormalKpiRegistryReader:
    """Resolve formal KPI definitions without owning or promoting KPIs."""

    def __init__(self, url: str, service_role_key: str, timeout: float = 15.0) -> None:
        if not url.strip():
            raise ValueError("Supabase URL is required")
        if not service_role_key.strip():
            raise ValueError("Supabase service_role_key is required")
        self._url = url.rstrip("/")
        self._key = service_role_key
        self._timeout = timeout

    def get_definition(self, *, metric_code: str) -> Mapping[str, object] | None:
        code = metric_code.strip()
        if not code:
            raise ValueError("metric_code is required")
        query = urllib.parse.urlencode(
            {
                "select": "id,codigo_kpi,nome,unidade,formula,ativo",
                "codigo_kpi": f"eq.{code}",
                "limit": "1",
            },
            safe=".,()*",
        )
        request = urllib.request.Request(
            f"{self._url}/rest/v1/mt_definicoes_kpi?{query}",
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
            raise RuntimeError(f"Supabase KPI read failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Supabase KPI read failed: network error: {exc}") from exc

        if not raw:
            return None
        parsed: Any = json.loads(raw)
        if not isinstance(parsed, list):
            raise RuntimeError("Supabase KPI read returned a non-list payload")
        rows = [item for item in parsed if isinstance(item, dict)]
        if not rows:
            return None
        row = rows[0]
        if str(row.get("codigo_kpi") or "") != code:
            raise ValueError("formal KPI lookup returned a different metric_code")
        return row


__all__ = ["SupabaseFormalKpiRegistryReader"]
