"""Canonical ELO identity, trust and capability boundary.

Authentication is external. This module binds an authenticated principal to an
explicit ELO identity, role, repository scope and capability set. It never grants
GitHub permissions and never replaces repository/app security controls.
"""
from dataclasses import dataclass
from enum import StrEnum


class TrustDecision(StrEnum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class EloRole(StrEnum):
    CONSULTANT = "CONSULTANT"
    SPECIALIST = "SPECIALIST"
    OPERATOR = "OPERATOR"
    GOVERNANCE = "GOVERNANCE"
    CANONICAL_ADMIN = "CANONICAL_ADMIN"


@dataclass(frozen=True)
class EloIdentity:
    principal_id: str
    provider: str
    provider_subject: str
    role: EloRole
    enterprise_context: str
    repository_scope: tuple[str, ...]
    capabilities: frozenset[str]
    active: bool = True


@dataclass(frozen=True)
class TrustRequest:
    identity: EloIdentity
    repository: str
    action: str
    capability: str


@dataclass(frozen=True)
class TrustResult:
    decision: TrustDecision
    reason: str


_CRITICAL_ACTIONS = frozenset({
    "modify_cognitive_identity",
    "modify_core",
    "modify_canonical_memory",
    "modify_security_policy",
    "change_permissions",
    "promote_to_core",
    "merge_protected_change",
})


def evaluate_trust(request: TrustRequest) -> TrustResult:
    """Fail-closed trust evaluation for ELO-sensitive operations."""
    identity = request.identity
    if not identity.active:
        return TrustResult(TrustDecision.DENY, "identity_inactive")
    required = (
        identity.principal_id,
        identity.provider,
        identity.provider_subject,
        identity.enterprise_context,
        request.repository,
        request.action,
        request.capability,
    )
    if not all(required):
        return TrustResult(TrustDecision.DENY, "missing_identity_or_scope")
    if request.repository not in identity.repository_scope:
        return TrustResult(TrustDecision.DENY, "repository_out_of_scope")
    if request.capability not in identity.capabilities:
        return TrustResult(TrustDecision.DENY, "capability_not_granted")
    if request.action in _CRITICAL_ACTIONS and identity.role is not EloRole.CANONICAL_ADMIN:
        return TrustResult(TrustDecision.DENY, "canonical_authority_required")
    return TrustResult(TrustDecision.ALLOW, "identity_scope_and_capability_verified")
