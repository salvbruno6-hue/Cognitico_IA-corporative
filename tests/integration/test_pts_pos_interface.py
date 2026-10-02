from fastapi.testclient import TestClient
from elo.interface.api import app

def _base_document() -> dict:
    return {
        "so": "SO 001.26",
        "cliente": "Cliente teste",
        "objeto": "Objeto teste",
        "matriz_principal": [{
            "n": 1, "ref_tecnica": "T-001", "topico": "teste", "ref_tr": "TR-001",
            "requisito": "requisito", "q_prev": 1, "q_orc": 1, "ref_orc": "ORC-001",
            "valor": 100, "status": "OK", "divergencia": "",
        }],
        "divergencias": [], "riscos": [], "pendencias": [], "checklist": {},
    }

def test_pts_pos_renderer_direct_smoke() -> None:
    from elo.interface.pts_pos import render_pts_pos

    markdown, integracao = render_pts_pos(_base_document())
    assert "PTS PÓS-ORÇAMENTO" in markdown
    assert integracao["resultado_arbitrado"]["status"] == "AGUARDANDO_ARBITRAGEM"

def test_pts_pos_endpoint_uses_canonical_renderer() -> None:
    response = TestClient(app).post("/pts-pos", json={
        "tenant_id": "multiteiner", "principal_id": "principal-test", "dados": _base_document(),
    })
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "RENDERED"
    assert "PTS PÓS-ORÇAMENTO" in payload["markdown"]
    assert payload["integracao"]["resultado_arbitrado"]["status"] == "AGUARDANDO_ARBITRAGEM"
    assert payload["integracao"]["elo_aprender"]["status"] == "CANDIDATA"
    assert payload["provenance"]["persisted"] is False
    assert payload["provenance"]["arbitrated_automatically"] is False

def test_pts_pos_endpoint_rejects_missing_tenant() -> None:
    response = TestClient(app).post("/pts-pos", json={"tenant_id": "", "dados": _base_document()})
    assert response.status_code == 400
