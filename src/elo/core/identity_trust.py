"""Canonical ELO identity, trust and capability boundary.

Authentication is external. This module binds a provider subject from a trusted
provider assertion to an authoritative ELO identity record. Privileged role,
enterprise context, repository scope, capabilities and active state are never
accepted from the request.
"""
from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


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
    """Unprivileged request context plus the authenticated provider subject.

    Authority attributes deliberately do not exist on this request object.
    They can therefore only be obtained from the authoritative registry.
    """

    provider: str
    provider_subject: str
    repository: str
    action: str
    capability: str


@dataclass(frozen=True)
class TrustResult:
    decision: TrustDecision
    reason: str


@dataclass(frozen=True)
class TrustedIdentityRegistry:
    """Immutable authoritative snapshot supplied by the identity layer."""

    identities: Mapping[str, EloIdentity]

    def resolve(self, provider: str, provider_subject: str) -> EloIdentity | None:
        return self.identities.get(f"{provider}:{provider_subject}")


_CRITICAL_ACTIONS = frozenset({
    "modify_cognitive_identity",
    "modify_core",
    "modify_canonical_memory",
    "modify_security_policy",
    "change_permissions",
    "promote_to_core",
    "merge_protected_change",
})


def evaluate_trust(request: TrustRequest, registry: TrustedIdentityRegistry) -> TrustResult:
    """Fail-closed trust evaluation using registry authority, never request claims."""
    if not all((request.provider, request.provider_subject, request.repository, request.action, request.capability)):
        return TrustResult(TrustDecision.DENY, "missing_identity_or_scope")

    # The provider subject is the only identity input. All privileged authority
    # attributes are resolved from the trusted registry and cannot be supplied
    # or overridden by the caller.
    authoritative = registry.resolve(request.provider, request.provider_subject)
    if authoritative is None:
        return TrustResult(TrustDecision.DENY, "provider_identity_not_registered")

    if not authoritative.active:
        return TrustResult(TrustDecision.DENY, "identity_inactive")
    if request.repository not in authoritative.repository_scope:
        return TrustResult(TrustDecision.DENY, "repository_out_of_scope")
    if request.capability not in authoritative.capabilities:
        return TrustResult(TrustDecision.DENY, "capability_not_granted")
    if request.action in _CRITICAL_ACTIONS and authoritative.role is not EloRole.CANONICAL_ADMIN:
        return TrustResult(TrustDecision.DENY, "canonical_authority_required")
    return TrustResult(TrustDecision.ALLOW, "identity_scope_and_capability_verified")
