"""FastAPI boundary for the ELO cognitive vertical slice."""

from __future__ import annotations

from time import perf_counter
from uuid import uuid4
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from elo.cognitive import CognitiveCore
from elo.cognitive.response.elo_gpt_dialogue import AuthorizationState, EvidenceState
from .chat_prefinalization import ChatPreFinalizationCommand, run_chat_prefinalization
from .contracts import CognitiveRequest, CognitiveResponse, ErrorContract
from .response import ResponseBuilder
from .session import SessionManager
from .pts_pos import render_pts_pos

app = FastAPI(title="ELO Interface API", version="0.1.0")
core = CognitiveCore()
session_manager = SessionManager()
response_builder = ResponseBuilder()


class PTSPosRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    session_id: str | None = None
    tenant_id: str
    principal_id: str | None = None
    dados: dict[str, Any]


class ChatPreFinalizationRequest(BaseModel):
    tenant_id: str
    objective_id: str
    objective_title: str
    workstream_id: str
    expected_checkpoint_version: int | None = None
    chat_draft: str = ""
    progress_token: str
    evidence_refs: list[str]
    proposed_next_action: str
    objective_evidence_refs: list[str]
    authorization_state: AuthorizationState
    continuation_permitted: bool = True
    objective_satisfied: bool = False
    within_scope: bool = True
    authority_available: bool = True
    risk_level: str = "LOW"
    evidence_state: EvidenceState = EvidenceState.OBSERVED
    max_cycles: int = 12


@app.get("/")
def root() -> dict[str, str]:
    return {"name": "ELO Interface API", "status": "running", "layer": "interface"}


def cognitive_endpoint(request: CognitiveRequest) -> CognitiveResponse:
    try:
        session = session_manager.get_or_create(request.session_id, user_id=request.user_id, principal_id=request.principal_id, tenant_id=request.tenant_id, domain=request.domain, context=request.context)
        started_at = perf_counter()
        session_manager.record_interaction(session, {"event": "cognitive.request", "request_id": request.request_id, "correlation_id": request.correlation_id, "tenant_id": request.tenant_id, "principal_id": request.principal_id, "domain": request.domain})
        result = core.process(request)
        response = response_builder.build(request, session.id, result, started_at=started_at)
        session_manager.record_interaction(session, {"event": "cognitive.response", "response_id": response.response_id, "request_id": response.request_id, "correlation_id": response.correlation_id, "tenant_id": response.tenant_id, "domain": response.domain})
        return response
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="ELO cognitive processing failed") from exc


@app.post("/cognitive", response_model=CognitiveResponse)
def cognitive(request: CognitiveRequest) -> CognitiveResponse:
    return cognitive_endpoint(request)


@app.post("/elo/chat/prefinalize")
def elo_chat_prefinalize(request: ChatPreFinalizationRequest) -> dict[str, object]:
    """Run exactly one governed ELO objective cycle before a GPT final response."""
    try:
        return run_chat_prefinalization(
            ChatPreFinalizationCommand(
                tenant_id=request.tenant_id,
                objective_id=request.objective_id,
                objective_title=request.objective_title,
                workstream_id=request.workstream_id,
                expected_checkpoint_version=request.expected_checkpoint_version,
                chat_draft=request.chat_draft,
                progress_token=request.progress_token,
                evidence_refs=tuple(request.evidence_refs),
                proposed_next_action=request.proposed_next_action,
                objective_evidence_refs=tuple(request.objective_evidence_refs),
                authorization_state=request.authorization_state,
                continuation_permitted=request.continuation_permitted,
                objective_satisfied=request.objective_satisfied,
                within_scope=request.within_scope,
                authority_available=request.authority_available,
                risk_level=request.risk_level,
                evidence_state=request.evidence_state,
                max_cycles=request.max_cycles,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="ELO chat pre-finalization failed") from exc


@app.post("/pts-pos")
def pts_pos(request: PTSPosRequest) -> dict[str, Any]:
    """Renderiza a PTS Pós pelo owner canônico; não persiste nem arbitra."""
    if not request.tenant_id.strip():
        raise HTTPException(status_code=400, detail="tenant_id é obrigatório.")
    try:
        markdown, integracao = render_pts_pos(request.dados)
        return {
            "request_id": request.request_id,
            "correlation_id": request.correlation_id,
            "session_id": request.session_id,
            "tenant_id": request.tenant_id,
            "status": "RENDERED",
            "markdown": markdown,
            "integracao": {
                "resultado_arbitrado": integracao.get("resultado_arbitrado", {}),
                "elo_aprender": integracao.get("elo_aprender", {}),
            },
            "provenance": {
                "owner": "08-ai/ELO/DIRETRIZES/PTS/POS_ORCAMENTO_RENDER.py",
                "operation": "render_pts_pos",
                "persisted": False,
                "arbitrated_automatically": False,
                "principal_id": request.principal_id,
            },
        }
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Falha ao renderizar PTS Pós pelo owner canônico.") from exc


@app.post("/sessions/{session_id}/clear")
def clear_session(session_id: str) -> dict[str, Any]:
    session_manager.delete(session_id)
    return {"session_id": session_id, "status": "cleared"}


def safe_cognitive(payload: dict[str, Any] | CognitiveRequest) -> CognitiveResponse | ErrorContract:
    try:
        request = payload if isinstance(payload, CognitiveRequest) else CognitiveRequest.model_validate(payload)
        return cognitive_endpoint(request)
    except Exception as exc:  # noqa: BLE001
        request_id = payload.request_id if isinstance(payload, CognitiveRequest) else payload.get("request_id")
        correlation_id = payload.correlation_id if isinstance(payload, CognitiveRequest) else payload.get("correlation_id")
        status = 400 if isinstance(exc, ValueError) else 403 if isinstance(exc, PermissionError) else 500
        return ErrorContract(code="INVALID_REQUEST" if status == 400 else "FORBIDDEN" if status == 403 else "COGNITIVE_PROCESSING_FAILED", message=str(exc) if status != 500 else "ELO cognitive processing failed", request_id=request_id, correlation_id=correlation_id, status_code=status)
