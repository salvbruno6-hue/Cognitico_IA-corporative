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


def test_production_client_requires_token():
    client = HermesHttpRuntimeClient("https://runtime.example", "")
    with pytest.raises(ValueError, match="token"):
        client.execute({"request_id": "req-1"})


def test_production_client_preserves_identity_and_runtime_facts(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["authorization"] = request.get_header("Authorization")
        captured["timeout"] = timeout
        captured["body"] = json.loads(request.data.decode("utf-8"))
        return _Response({
            "request_id": "req-1",
            "environment": "production",
            "runtime_trace": "trace-1",
            "result": "executed",
        })

    monkeypatch.setattr("elo.agent_intake.hermes_http_runtime_client.urlopen", fake_urlopen)
    result = HermesHttpRuntimeClient("https://runtime.example", "secret").execute(
        {"request_id": "req-1", "skill_id": "EXT-ROUTE-HERMES"}
    )

    assert captured["authorization"] == "Bearer secret"
    assert captured["timeout"] == 30.0
    assert captured["body"]["skill_id"] == "EXT-ROUTE-HERMES"
    assert result["environment"] == "production"
    assert result["runtime_trace"] == "trace-1"


def test_production_client_rejects_request_identity_mismatch(monkeypatch):
    monkeypatch.setattr(
        "elo.agent_intake.hermes_http_runtime_client.urlopen",
        lambda *args, **kwargs: _Response({"request_id": "other", "environment": "production"}),
    )
    with pytest.raises(ValueError, match="request_id"):
        HermesHttpRuntimeClient("https://runtime.example", "secret").execute({"request_id": "req-1"})


def test_production_client_rejects_non_production_response(monkeypatch):
    monkeypatch.setattr(
        "elo.agent_intake.hermes_http_runtime_client.urlopen",
        lambda *args, **kwargs: _Response({"request_id": "req-1", "environment": "staging"}),
    )
    with pytest.raises(ValueError, match="environment=production"):
        HermesHttpRuntimeClient("https://runtime.example", "secret").execute({"request_id": "req-1"})


def test_production_client_does_not_treat_invalid_json_as_execution(monkeypatch):
    class InvalidResponse(_Response):
        def __init__(self):
            self._payload = b"not-json"

    monkeypatch.setattr(
        "elo.agent_intake.hermes_http_runtime_client.urlopen",
        lambda *args, **kwargs: InvalidResponse(),
    )
    with pytest.raises(ValueError, match="invalid JSON"):
        HermesHttpRuntimeClient("https://runtime.example", "secret").execute({"request_id": "req-1"})
