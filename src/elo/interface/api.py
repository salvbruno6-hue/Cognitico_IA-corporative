"""FastAPI layer for the ELO cognitive interface."""

from __future__ import annotations

from time import perf_counter
from typing import Any

from fastapi import FastAPI, HTTPException

from elo.cognitive import CognitiveCore

from .contracts import CognitiveRequest, CognitiveResponse
from .response import ResponseBuilder
from .session import SessionManager

app = FastAPI(title="ELO Interface API", version="0.1.0")

core = CognitiveCore()
session_manager = SessionManager()
response_builder = ResponseBuilder()


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "ELO Interface API",
        "status": "running",
        "layer": "interface",
    }


@app.post("/cognitive", response_model=CognitiveResponse)
def cognitive_endpoint(request: CognitiveRequest) -> CognitiveResponse:
    try:
        session = session_manager.get_or_create(
            request.session_id,
            user_id=request.user_id,
            tenant_id=request.tenant_id,
            domain=request.domain,
            context=request.context,
        )

        started_at = perf_counter()
        interaction_context = {
            "request_id": request.request_id,
            "message": request.message,
            "domain": request.domain,
            "tenant_id": request.tenant_id,
            "user_id": request.user_id,
            "context": request.context,
        }
        session_manager.record_interaction(session, interaction_context)

        core_result = core.process(
            {
                "message": request.message,
                "session_id": session.id,
                "user_id": request.user_id,
                "tenant_id": request.tenant_id,
                "domain": request.domain,
                "context": request.context,
            }
        )

        response = response_builder.build(
            request=request,
            session_id=session.id,
            result=core_result,
            started_at=started_at,
        )

        session_manager.record_interaction(
            session,
            {
                "response_id": response.response_id,
                "confidence": response.confidence,
                "domain": response.domain,
                "provenance": response.provenance.model_dump(),
            },
        )
        return response

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="ELO cognitive processing failed") from exc


@app.post("/sessions/{session_id}/clear")
def clear_session(session_id: str) -> dict[str, Any]:
    session_manager.delete(session_id)
    return {"session_id": session_id, "status": "cleared"}
