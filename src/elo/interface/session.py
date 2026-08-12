"""Session abstractions for the ELO cognitive interface."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import RLock
from typing import Any, Protocol
from uuid import uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class Session:
    id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str | None = None
    principal_id: str | None = None
    tenant_id: str | None = None
    domain: str | None = None
    context: dict[str, Any] = field(default_factory=dict)
    interactions: list[dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def add_interaction(self, interaction: dict[str, Any]) -> None:
        self.interactions.append(dict(interaction))
        self.updated_at = utc_now()

    def update_context(self, values: dict[str, Any]) -> None:
        self.context.update(values)
        self.updated_at = utc_now()


class SessionStore(Protocol):
    def get(self, session_id: str) -> Session | None: ...
    def save(self, session: Session) -> None: ...
    def delete(self, session_id: str) -> None: ...


class InMemorySessionStore:
    """Development-only store; replaceable without changing callers."""

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}
        self._lock = RLock()

    def get(self, session_id: str) -> Session | None:
        with self._lock:
            return self._sessions.get(session_id)

    def save(self, session: Session) -> None:
        with self._lock:
            session.updated_at = utc_now()
            self._sessions[session.id] = session

    def delete(self, session_id: str) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)


class SessionManager:
    def __init__(self, store: SessionStore | None = None) -> None:
        self.store = store or InMemorySessionStore()

    def get_or_create(self, session_id: str | None = None, *, user_id: str | None = None, principal_id: str | None = None, tenant_id: str | None = None, domain: str | None = None, context: dict[str, Any] | None = None) -> Session:
        if not tenant_id:
            raise ValueError("tenant_id is required")
        if session_id:
            existing = self.store.get(session_id)
            if existing is not None:
                if existing.tenant_id != tenant_id:
                    raise PermissionError("session does not belong to tenant")
                if existing.principal_id and principal_id and existing.principal_id != principal_id:
                    raise PermissionError("session does not belong to principal")
                if domain is not None:
                    existing.domain = domain
                if context:
                    existing.update_context(context)
                self.store.save(existing)
                return existing
        session = Session(id=session_id or str(uuid4()), user_id=user_id, principal_id=principal_id or user_id, tenant_id=tenant_id, domain=domain, context=dict(context or {}))
        self.store.save(session)
        return session

    def record_interaction(self, session: Session, interaction: dict[str, Any]) -> None:
        session.add_interaction(interaction)
        self.store.save(session)

    def delete(self, session_id: str) -> None:
        self.store.delete(session_id)
