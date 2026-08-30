"""Executable login/security scenarios for ELO.

These tests intentionally use a local verifier boundary. They prove the login
policy and session lifecycle without pretending to call GitHub or ChatGPT.
Provider integration tests must supply real credentials separately.
"""

from dataclasses import dataclass
from enum import Enum
import time


class Decision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


@dataclass(frozen=True)
class Identity:
    provider_subject: str
    github_login: str
    role: str
    scopes: frozenset[str]


@dataclass
class Session:
    identity: Identity
    token: str
    expires_at: float
    active: bool = True


def authenticate(provider_subject: str, github_login: str, registry: dict[str, Identity]) -> Session | None:
    identity = registry.get(provider_subject)
    if identity is None or identity.github_login != github_login:
        return None
    return Session(identity, token=f"session:{provider_subject}:{github_login}", expires_at=time.time() + 300)


def authorize(session: Session | None, required_scope: str, operation: str) -> Decision:
    if session is None or not session.active or session.expires_at <= time.time():
        return Decision.DENY
    if required_scope not in session.identity.scopes:
        return Decision.DENY
    if operation in {"MERGE", "ADMIN"} and session.identity.role not in {"OWNER", "RELEASE_MANAGER"}:
        return Decision.DENY
    return Decision.ALLOW


def logout(session: Session) -> None:
    session.active = False


def test_login_once_reuses_authoritative_identity_and_scope():
    registry = {
        "chatgpt:operator-01": Identity(
            "chatgpt:operator-01", "salvbruno6-hue", "RELEASE_MANAGER", frozenset({"ELO_CORE", "ELO_SECURITY"})
        )
    }
    session = authenticate("chatgpt:operator-01", "salvbruno6-hue", registry)
    assert session is not None
    assert authorize(session, "ELO_SECURITY", "READ") is Decision.ALLOW
    assert authorize(session, "ELO_SECURITY", "MERGE") is Decision.ALLOW


def test_wrong_github_identity_is_denied():
    registry = {
        "chatgpt:operator-01": Identity(
            "chatgpt:operator-01", "salvbruno6-hue", "RELEASE_MANAGER", frozenset({"ELO_SECURITY"})
        )
    }
    assert authenticate("chatgpt:operator-01", "attacker", registry) is None


def test_valid_login_without_merge_scope_is_denied():
    registry = {
        "chatgpt:analyst-01": Identity(
            "chatgpt:analyst-01", "analyst", "ANALYST", frozenset({"ELO_SECURITY"})
        )
    }
    session = authenticate("chatgpt:analyst-01", "analyst", registry)
    assert authorize(session, "ELO_SECURITY", "READ") is Decision.ALLOW
    assert authorize(session, "ELO_SECURITY", "MERGE") is Decision.DENY


def test_logout_ends_session_and_requires_new_login():
    registry = {
        "chatgpt:operator-01": Identity(
            "chatgpt:operator-01", "salvbruno6-hue", "RELEASE_MANAGER", frozenset({"ELO_SECURITY"})
        )
    }
    session = authenticate("chatgpt:operator-01", "salvbruno6-hue", registry)
    assert session is not None
    logout(session)
    assert authorize(session, "ELO_SECURITY", "READ") is Decision.DENY
    new_session = authenticate("chatgpt:operator-01", "salvbruno6-hue", registry)
    assert new_session is not None
    assert authorize(new_session, "ELO_SECURITY", "READ") is Decision.ALLOW


def test_expired_session_is_denied():
    registry = {
        "chatgpt:operator-01": Identity(
            "chatgpt:operator-01", "salvbruno6-hue", "RELEASE_MANAGER", frozenset({"ELO_SECURITY"})
        )
    }
    session = authenticate("chatgpt:operator-01", "salvbruno6-hue", registry)
    assert session is not None
    session.expires_at = time.time() - 1
    assert authorize(session, "ELO_SECURITY", "READ") is Decision.DENY
