from __future__ import annotations

import json

import pytest

from elo.agent_intake.hermes_http_runtime_client import HermesHttpRuntimeClient


class _Response:
    def __init__(self, payload):
        self._payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self._payload


def test_production_client_requires_https():
    client = HermesHttpRuntimeClient("http://runtime.example", "secret")
    with pytest.raises(ValueError, match="HTTPS"):
        client.execute({"request_id": "req-1"})


def test_production_client_rejects_non_production_response(monkeypatch):
    def fake_urlopen(*args, **kwargs):
        return _Response({"request_id": "req-1", "environment": "staging"})

    monkeypatch.setattr(
        "elo.agent_intake.hermes_http_runtime_client.urlopen",
        fake_urlopen,
    )

    client = HermesHttpRuntimeClient("https://runtime.example", "secret")
    with pytest.raises(ValueError, match="environment=production"):
        client.execute({"request_id": "req-1"})


def test_production_client_preserves_request_identity_and_returns_runtime_facts(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["authorization"] = request.get_header("Authorization")
        captured["timeout"] = timeout
        captured["body"] = json.loads(request.data.decode("utf-8"))
        return _Response(
            {
                "request_id": "req-1",
                "environment": "production",
                "runtime_trace": "trace-1",
                "result": "executed",
            }
        )

    monkeypatch.setattr(
        "elo.agent_intake.hermes_http_runtime_client.urlopen",
        fake_urlopen,
    )

    client = HermesHttpRuntimeClient("https://runtime.example", "secret")
    result = client.execute({"request_id": "req-1", "skill_id": "EXT-ROUTE-HERMES"})

    assert captured["authorization"] == "Bearer secret"
    assert captured["timeout"] == 30.0
    assert captured["body"]["skill_id"] == "EXT-ROUTE-HERMES"
    assert result["environment"] == "production"
    assert result["runtime_trace"] == "trace-1"


def test_production_client_does_not_treat_invalid_json_as_execution(monkeypatch):
    class InvalidResponse(_Response):
        def __init__(self):
            self._payload = b"not-json"

    monkeypatch.setattr(
        "elo.agent_intake.hermes_http_runtime_client.urlopen",
        lambda *args, **kwargs: InvalidResponse(),
    )

    client = HermesHttpRuntimeClient("https://runtime.example", "secret")
    with pytest.raises(ValueError, match="invalid JSON"):
        client.execute({"request_id": "req-1"})
