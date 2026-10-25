from __future__ import annotations

from fastapi.testclient import TestClient

from elo.interface.api import app


client = TestClient(app)


def _payload(**overrides):
    payload = {
        "tenant_id": "tenant-chat-api",
        "objective_id": "objective-chat-api",
        "objective_title": "Continuar dialogo autonomo ELO GPT",
        "workstream_id": "chat-prefinalization-api",
        "expected_checkpoint_version": None,
        "chat_draft": "rascunho GPT",
        "progress_token": "api-wakeup:1",
        "evidence_refs": ["evidence://api/wakeup/1"],
        "proposed_next_action": "EXECUTE_SECOND_GOVERNED_STEP",
        "objective_evidence_refs": ["evidence://api/objective"],
        "authorization_state": "VALID",
        "continuation_permitted": True,
        "objective_satisfied": False,
        "within_scope": True,
        "authority_available": True,
        "risk_level": "LOW",
        "evidence_state": "OBSERVED",
        "max_cycles": 6,
    }
    payload.update(overrides)
    return payload


def test_prefinalization_http_survives_two_independent_requests(tmp_path, monkeypatch) -> None:
    store_path = tmp_path / "objective-loop.sqlite"
    monkeypatch.setenv("ELO_SYMBIONT_EXECUTION_STORE_PATH", str(store_path))

    first = client.post("/elo/chat/prefinalize", json=_payload())
    assert first.status_code == 200, first.text
    first_body = first.json()
    assert first_body["decision"] == "CONTINUE"
    assert first_body["should_continue_automatically"] is True
    assert first_body["replay_count"] == 1
    assert first_body["next_trigger"]["trigger_type"] == "CONTINUE_OBJECTIVE"
    checkpoint = first_body["next_trigger"]["checkpoint_version"]
    assert checkpoint >= 2

    second = client.post(
        "/elo/chat/prefinalize",
        json=_payload(
            expected_checkpoint_version=checkpoint,
            progress_token="api-wakeup:2:complete",
            evidence_refs=["evidence://api/wakeup/2"],
            proposed_next_action="OBJECTIVE_COMPLETE",
            objective_satisfied=True,
            continuation_permitted=False,
        ),
    )
    assert second.status_code == 200, second.text
    second_body = second.json()
    assert second_body["decision"] == "COMPLETE"
    assert second_body["should_continue_automatically"] is False
    assert second_body["next_trigger"] is None


def test_prefinalization_http_fails_closed_without_durable_store(monkeypatch) -> None:
    monkeypatch.delenv("ELO_SYMBIONT_EXECUTION_STORE_PATH", raising=False)
    response = client.post("/elo/chat/prefinalize", json=_payload())
    assert response.status_code == 503
    assert "durable Symbiont execution store is not configured" in response.json()["detail"]


def test_prefinalization_http_rejects_stale_checkpoint(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ELO_SYMBIONT_EXECUTION_STORE_PATH", str(tmp_path / "stale.sqlite"))
    first = client.post("/elo/chat/prefinalize", json=_payload())
    assert first.status_code == 200

    stale = client.post(
        "/elo/chat/prefinalize",
        json=_payload(
            expected_checkpoint_version=1,
            progress_token="api-wakeup:stale",
            evidence_refs=["evidence://api/stale"],
        ),
    )
    assert stale.status_code == 400
    assert "stale objective checkpoint" in stale.json()["detail"]
