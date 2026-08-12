"""Public API for the ELO interface layer.

Imports are intentionally lazy so the cognitive core can depend on canonical
interface contracts without creating an import cycle through this package.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "app",
    "safe_cognitive",
    "AgentReference",
    "CognitiveRequest",
    "CognitiveResponse",
    "ErrorContract",
    "InMemorySessionStore",
    "Provenance",
    "ResponseBuilder",
    "Session",
    "SessionManager",
    "SessionStore",
    "SourceReference",
    "SuggestedAction",
]


def __getattr__(name: str) -> Any:
    if name in {"app", "safe_cognitive"}:
        from .api import app, safe_cognitive
        return {"app": app, "safe_cognitive": safe_cognitive}[name]
    if name in {
        "AgentReference",
        "CognitiveRequest",
        "CognitiveResponse",
        "ErrorContract",
        "Provenance",
        "SourceReference",
        "SuggestedAction",
    }:
        from .contracts import (
            AgentReference,
            CognitiveRequest,
            CognitiveResponse,
            ErrorContract,
            Provenance,
            SourceReference,
            SuggestedAction,
        )
        return {
            "AgentReference": AgentReference,
            "CognitiveRequest": CognitiveRequest,
            "CognitiveResponse": CognitiveResponse,
            "ErrorContract": ErrorContract,
            "Provenance": Provenance,
            "SourceReference": SourceReference,
            "SuggestedAction": SuggestedAction,
        }[name]
    if name == "ResponseBuilder":
        from .response import ResponseBuilder
        return ResponseBuilder
    if name in {"InMemorySessionStore", "Session", "SessionManager", "SessionStore"}:
        from .session import InMemorySessionStore, Session, SessionManager, SessionStore
        return {
            "InMemorySessionStore": InMemorySessionStore,
            "Session": Session,
            "SessionManager": SessionManager,
            "SessionStore": SessionStore,
        }[name]
    raise AttributeError(name)
