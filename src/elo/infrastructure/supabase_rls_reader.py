"""Reader live de RLS via Supabase RPC.

Chama public.elo_read_rls_state (que delega para
elo_private.read_rls_state), executável somente por
service_role.

Read-only. Nunca executa DDL.

Refs: ELO_LIVE_STATE_RECONCILIATION_CONTRACT,
      migration 20260927000000_elo_read_rls_state.sql.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from .live_state_reconciliation import RLSLiveState


RPC_PATH = "/rest/v1/rpc/elo_read_rls_state"
DEFAULT_TIMEOUT = 15.0


class SupabaseRLSStateReader:
    """Implementação do RLSStateReader via REST + service_role.

    Não usa PostgREST direto em pg_catalog.
    Não expõe pg_catalog.

    Cada chamada read(table) dispara uma RPC com 1 item no
    array. Para múltiplas tabelas, o harness chama N vezes.
    Se isso se tornar custoso, uma extensão futura pode ler
    em lote.
    """

    def __init__(
        self,
        url: str,
        service_role_key: str,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        if not url:
            raise ValueError("Supabase URL is required")
        if not service_role_key:
            raise ValueError("Supabase service_role_key is required")
        self._url = url.rstrip("/")
        self._key = service_role_key
        self._timeout = timeout

    def read(self, table: str) -> RLSLiveState:
        try:
            payload = self._call_rpc([table])
        except Exception as exc:
            return RLSLiveState(
                table=table,
                rls_enabled=None,
                read_error=f"rpc call failed: {exc}",
            )

        if not payload:
            return RLSLiveState(
                table=table,
                rls_enabled=None,
                read_error="empty rpc response",
            )

        item = payload[0]
        if item.get("error") == "table_not_found":
            return RLSLiveState(
                table=table,
                rls_enabled=None,
                read_error="table not found in public schema",
            )

        rls = item.get("rls_enabled")
        if rls is None:
            return RLSLiveState(
                table=table,
                rls_enabled=None,
                read_error="rls_enabled is null in response",
            )

        policies = item.get("policies") or []
        if isinstance(policies, str):
            try:
                policies = json.loads(policies)
            except json.JSONDecodeError:
                policies = []

        return RLSLiveState(
            table=table,
            rls_enabled=bool(rls),
            policies=tuple(str(p) for p in policies),
        )

    def _call_rpc(self, tables: list[str]) -> list[dict[str, Any]]:
        body = json.dumps({"p_tables": tables}).encode("utf-8")
        request = urllib.request.Request(
            f"{self._url}{RPC_PATH}",
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "apikey": self._key,
                "Authorization": f"Bearer {self._key}",
                "Accept": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(
                request, timeout=self._timeout
            ) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = ""
            try:
                detail = exc.read().decode("utf-8")
            except Exception:
                pass
            raise RuntimeError(
                f"HTTP {exc.code}: {detail}"
            ) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"network error: {exc}") from exc

        if not raw:
            return []

        parsed = json.loads(raw)

        if isinstance(parsed, str):
            parsed = json.loads(parsed)

        if isinstance(parsed, dict):
            parsed = [parsed]

        if not isinstance(parsed, list):
            raise RuntimeError(
                f"unexpected rpc response type: {type(parsed)}"
            )

        return parsed


__all__ = ["SupabaseRLSStateReader"]
