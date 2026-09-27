"""Testes do reader live de RLS."""
from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from elo.infrastructure.supabase_rls_reader import (
    SupabaseRLSStateReader,
)


class MockHTTPResponse:
    def __init__(self, body: bytes, status: int = 200):
        self._body = body
        self.status = status

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def _mock_urlopen(body: dict | list) -> MockHTTPResponse:
    payload = json.dumps(body).encode("utf-8")
    return MockHTTPResponse(payload)


def test_reader_rejects_empty_url():
    with pytest.raises(ValueError):
        SupabaseRLSStateReader("", "key")


def test_reader_rejects_empty_key():
    with pytest.raises(ValueError):
        SupabaseRLSStateReader("https://x.test", "")


def test_reader_reads_rls_on_with_policies():
    response = [{
        "table": "lista_mae",
        "rls_enabled": True,
        "policies": ["elo_lista_mae_select_consultation"],
    }]
    reader = SupabaseRLSStateReader("https://x.test", "key")
    with patch(
        "urllib.request.urlopen",
        return_value=_mock_urlopen(response),
    ):
        state = reader.read("lista_mae")

    assert state.table == "lista_mae"
    assert state.rls_enabled is True
    assert state.policies == (
        "elo_lista_mae_select_consultation",
    )
    assert state.read_error is None


def test_reader_reads_rls_off():
    response = [{
        "table": "fornecedor_cotacoes",
        "rls_enabled": False,
        "policies": [],
    }]
    reader = SupabaseRLSStateReader("https://x.test", "key")
    with patch(
        "urllib.request.urlopen",
        return_value=_mock_urlopen(response),
    ):
        state = reader.read("fornecedor_cotacoes")

    assert state.rls_enabled is False
    assert state.policies == ()


def test_reader_handles_table_not_found():
    response = [{
        "table": "missing",
        "rls_enabled": None,
        "policies": [],
        "error": "table_not_found",
    }]
    reader = SupabaseRLSStateReader("https://x.test", "key")
    with patch(
        "urllib.request.urlopen",
        return_value=_mock_urlopen(response),
    ):
        state = reader.read("missing")

    assert state.rls_enabled is None
    assert "table not found" in (state.read_error or "")


def test_reader_handles_network_error():
    import urllib.error

    reader = SupabaseRLSStateReader("https://x.test", "key")
    with patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.URLError("boom"),
    ):
        state = reader.read("lista_mae")

    assert state.rls_enabled is None
    assert "network error" in (state.read_error or "")


def test_reader_handles_empty_response():
    reader = SupabaseRLSStateReader("https://x.test", "key")
    with patch(
        "urllib.request.urlopen",
        return_value=MockHTTPResponse(b""),
    ):
        state = reader.read("x")

    assert state.rls_enabled is None
    assert state.read_error is not None


def test_reader_uses_postgrest_headers():
    captured: dict = {}

    def fake_urlopen(request, timeout=None):
        captured["url"] = request.full_url
        captured["headers"] = dict(request.header_items())
        captured["method"] = request.get_method()
        captured["data"] = request.data
        return _mock_urlopen([{
            "table": "x",
            "rls_enabled": True,
            "policies": [],
        }])

    reader = SupabaseRLSStateReader("https://x.test", "sk_test")
    with patch(
        "urllib.request.urlopen", side_effect=fake_urlopen
    ):
        reader.read("x")

    assert captured["url"].endswith(
        "/rest/v1/rpc/elo_read_rls_state"
    )
    assert captured["method"] == "POST"
    assert captured["headers"].get("Apikey") == "sk_test"
    body = json.loads(captured["data"].decode("utf-8"))
    assert body == {"p_tables": ["x"]}


def test_reader_normalizes_string_json_response():
    response = json.dumps([{
        "table": "x",
        "rls_enabled": True,
        "policies": [],
    }])
    reader = SupabaseRLSStateReader("https://x.test", "key")
    with patch(
        "urllib.request.urlopen",
        return_value=_mock_urlopen(response),
    ):
        state = reader.read("x")

    assert state.rls_enabled is True
