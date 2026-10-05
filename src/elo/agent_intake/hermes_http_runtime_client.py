"""HTTP transport for an already-authorized Hermes production runtime.

Transport only: authorization, candidate eligibility, evidence admission and
promotion remain owned by existing canonical ELO components.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True, slots=True)
class HermesHttpRuntimeClient:
    endpoint: str
    bearer_token: str
    timeout_seconds: float = 30.0

    def execute(self, payload: Mapping[str, Any]) -> Mapping[str, Any]:
        if not self.endpoint.startswith("https://"):
            raise ValueError("production Hermes endpoint must use HTTPS")
        if not self.bearer_token:
            raise ValueError("production Hermes bearer token is required")
        if not payload.get("request_id"):
            raise ValueError("request_id is required")

        body = json.dumps(dict(payload), separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        request = Request(
            self.endpoint,
            data=body,
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.bearer_token}",
            },
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                raw = response.read()
        except HTTPError as exc:
            raise RuntimeError(f"Hermes production runtime returned HTTP {exc.code}") from exc
        except URLError as exc:
            raise RuntimeError("Hermes production runtime is unreachable") from exc

        try:
            result = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Hermes production runtime returned invalid JSON") from exc

        if not isinstance(result, Mapping):
            raise TypeError("Hermes production runtime response must be a mapping")
        if result.get("request_id") != payload["request_id"]:
            raise ValueError("Hermes production response request_id does not match request")
        if result.get("environment") != "production":
            raise ValueError("Hermes production runtime must explicitly report environment=production")
        return result


__all__ = ["HermesHttpRuntimeClient"]
