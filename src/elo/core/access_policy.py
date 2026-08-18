"""Canonical access policy for ELO external consultation and specialist sessions.

Authentication identifies a principal; authorization determines what that principal may do.
The policy deliberately defaults external consultation to read-only and keeps repository/site
security outside the ELO cognitive layer.
"""
from dataclasses import dataclass
from enum import StrEnum


class SessionMode(StrEnum):
    READ_ONLY_CONSULTATION = "READ_ONLY_CONSULTATION"
    AUTHORIZED_SPECIALIST = "AUTHORIZED_SPECIALIST"


class AccessDecision(StrEnum):
    ALLOW = "ALLOW"
    DENY = "DENY"


@dataclass(frozen=True)
class AccessRequest:
    principal_id: str
    role: str
    domain: str
    enterprise_context: str
    scope: str
    action: str
    session_mode: SessionMode = SessionMode.READ_ONLY_CONSULTATION
    write_permission: bool = False
    external_action_permission: bool = False


@dataclass(frozen=True)
class AccessResult:
    decision: AccessDecision
    reason: str


_READ_ACTIONS = frozenset({"consult", "search", "inspect_issue", "inspect_pr", "inspect_workflow", "answer"})
_SPECIALIST_ACTIONS = frozenset({"provide_feedback", "propose_parameter", "propose_change", "validate_domain_result"})
_ALWAYS_DENIED = frozenset(
    {
        "modify_core",
        "modify_canonical_memory",
        "modify_security_policy",
        "modify_access_policy",
        "change_permissions",
        "delete_historical_evidence",
        "promote_to_core",
        "access_unrelated_repository",
        "access_owner_site",
        "access_secrets",
    }
)


def authorize(request: AccessRequest) -> AccessResult:
    """Apply fail-closed ELO session authorization rules."""
    required = (
        request.principal_id,
        request.role,
        request.domain,
        request.enterprise_context,
        request.scope,
        request.action,
    )
    if not all(required):
        return AccessResult(AccessDecision.DENY, "missing_identity_or_scope")

    if request.action in _ALWAYS_DENIED:
        return AccessResult(AccessDecision.DENY, "action_outside_elo_authority")

    if request.session_mode == SessionMode.READ_ONLY_CONSULTATION:
        if request.write_permission or request.external_action_permission:
            return AccessResult(AccessDecision.DENY, "consultation_mode_is_read_only")
        if request.action not in _READ_ACTIONS:
            return AccessResult(AccessDecision.DENY, "action_not_allowed_in_consultation")
        return AccessResult(AccessDecision.ALLOW, "read_only_consultation_allowed")

    if request.session_mode == SessionMode.AUTHORIZED_SPECIALIST:
        if request.action in _READ_ACTIONS or request.action in _SPECIALIST_ACTIONS:
            return AccessResult(AccessDecision.ALLOW, "scoped_specialist_action_allowed")
        if request.action.startswith("execute_") and not request.external_action_permission:
            return AccessResult(AccessDecision.DENY, "execution_requires_explicit_external_authority")
        if request.write_permission and request.action.startswith("write_"):
            return AccessResult(AccessDecision.ALLOW, "scoped_specialist_write_allowed")
        return AccessResult(AccessDecision.DENY, "action_not_allowed_for_specialist_scope")

    return AccessResult(AccessDecision.DENY, "unknown_session_mode")
