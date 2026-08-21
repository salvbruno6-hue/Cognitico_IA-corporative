"""Canonical ELO identity, trust and capability boundary.

Authentication is external. This module binds an authenticated provider subject
from a trusted provider assertion to an authoritative ELO identity record. The
request may carry identity claims, but privileged role, enterprise context,
repository scope, capabilities and active state are never trusted from the
request itself. GitHub remains the infrastructure authorization boundary.
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
    identity: EloIdentity
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
    """Fail-closed trust evaluation for ELO-sensitive operations."""
    asserted = request.identity
    if not all((asserted.provider, asserted.provider_subject, request.repository, request.action, request.capability)):
        return TrustResult(TrustDecision.DENY, "missing_identity_or_scope")

    authoritative = registry.resolve(asserted.provider, asserted.provider_subject)
    if authoritative is None:
        return TrustResult(TrustDecision.DENY, "provider_identity_not_registered")

    # Provider subject is the lookup anchor; every privileged ELO claim must
    # match the authoritative record rather than being accepted from the request.
    if asserted != authoritative:
        return TrustResult(TrustDecision.DENY, "identity_claims_do_not_match_authority")

    if not authoritative.active:
        return TrustResult(TrustDecision.DENY, "identity_inactive")
    if request.repository not in authoritative.repository_scope:
        return TrustResult(TrustDecision.DENY, "repository_out_of_scope")
    if request.capability not in authoritative.capabilities:
        return TrustResult(TrustDecision.DENY, "capability_not_granted")
    if request.action in _CRITICAL_ACTIONS and authoritative.role is not EloRole.CANONICAL_ADMIN:
        return TrustResult(TrustDecision.DENY, "canonical_authority_required")
    return TrustResult(TrustDecision.ALLOW, "identity_scope_and_capability_verified")
