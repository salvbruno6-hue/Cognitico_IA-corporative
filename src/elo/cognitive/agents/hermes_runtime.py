"""ELO-owned client for the governed Hermes execution boundary.

The client transports an already-authorized HermesExecutionRequest. It does not
resolve authorization, infrastructure, canonical knowledge, or learning.
"""

from __future__ import annotations

import json
import os
from collections.abc import Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from typing import Any

from .hermes_contract import HermesExecutionRequest, HermesExecutionResult

Transport = Callable[[str, Mapping[str, Any]], Mapping[str, Any]]


def _default_transport(endpoint: str, payload: Mapping[str, Any]) -> Mapping[str, Any]:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    runtime_token = os.getenv("ELO_HERMES_RUNTIME_TOKEN", "").strip()
    if runtime_token:
        headers["Authorization"] = f"Bearer {runtime_token}"

    request = Request(
        endpoint.rstrip("/") + "/elo/v1/execute",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:  # noqa: S310 - endpoint is an ELO configuration boundary
            body = response.read().decode("utf-8")
    except (HTTPError, URLError) as exc:
        raise RuntimeError(f"Hermes execution transport failed: {exc}") from exc
    decoded = json.loads(body)
    if not isinstance(decoded, Mapping):
        raise TypeError("Hermes response must be a JSON object")
    return decoded


def execute_via_hermes(
    request: HermesExecutionRequest,
    *,
    endpoint: str,
    transport: Transport | None = None,
) -> HermesExecutionResult:
    """Send one ELO-authorized mission to Hermes and normalize its evidence result."""
    if not endpoint.strip():
        raise ValueError("Hermes endpoint is required")

    raw = (transport or _default_transport)(endpoint, request.to_dict())
    result = HermesExecutionResult(**dict(raw))
    if result.request_id != request.request_id:
        raise ValueError("Hermes response request_id does not match ELO request")
    return result
