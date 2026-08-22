"""Governed ELO identity, environment and capability enforcement.

This module does not authenticate GitHub credentials itself. It consumes an
external identity assertion and turns it into an attributable ELO operator
binding. The external identity provider remains authoritative for credentials
and repository permissions.
"""
from dataclasses import dataclass, field
from enum import StrEnum
from secrets import token_urlsafe
from time import time


class Environment(StrEnum):
    ADM = "ADM"
    SPECIALIST = "SPECIALIST"
    VISITOR = "VISITOR"


class AuthMethod(StrEnum):
    DIRECT = "DIRECT"
    QR = "QR"


class Capability(StrEnum):
    CONSULT = "CONSULT"
    SPECIALIST_CONTRIBUTE = "SPECIALIST_CONTRIBUTE"
    COMMIT = "COMMIT"
    CREATE_PR = "CREATE_PR"
    MERGE_OPERATIONAL = "MERGE_OPERATIONAL"
    MERGE_STRUCTURAL = "MERGE_STRUCTURAL"
    VIEW_INTERNAL_ARCHITECTURE = "VIEW_INTERNAL_ARCHITECTURE"
    MANAGE_SECURITY = "MANAGE_SECURITY"


class Decision(StrEnum):
    ALLOW = "ALLOW"
    DENY = "DENY"


@dataclass(frozen=True)
class IdentityAssertion:
    """Assertion supplied by an external identity/authentication provider."""

    provider: str
    subject: str
    authenticated: bool
    github_subject: str | None = None


@dataclass(frozen=True)
class OperatorBinding:
    binding_id: str
    identity_subject: str
    github_subject: str
    environment: Environment
    capabilities: frozenset[Capability]
    repository_scope: frozenset[str]
    active: bool = True


@dataclass(frozen=True)
class AuthorizationResult:
    decision: Decision
    reason: str


@dataclass
class AuthorizationRegistry:
    """In-memory reference registry; persistence must use a protected store."""

    bindings: dict[str, OperatorBinding] = field(default_factory=dict)
    pending_challenges: dict[str, tuple[AuthMethod, float]] = field(default_factory=dict)

    def begin_admin_authorization(self, method: AuthMethod, ttl_seconds: int = 300) -> str:
        """Create a short-lived challenge; it is not itself an authorization."""
        challenge = token_urlsafe(24)
        self.pending_challenges[challenge] = (method, time() + ttl_seconds)
        return challenge

    def establish_admin_binding(
        self,
        challenge: str,
        assertion: IdentityAssertion,
        github_subject: str,
        repository_scope: set[str],
    ) -> OperatorBinding:
        pending = self.pending_challenges.get(challenge)
        if pending is None:
            raise PermissionError("authorization_challenge_not_found")
        _, expires_at = pending
        if time() > expires_at:
            self.pending_challenges.pop(challenge, None)
            raise PermissionError("authorization_challenge_expired")
        if not assertion.authenticated or assertion.github_subject != github_subject:
            raise PermissionError("identity_assertion_mismatch")
        self.pending_challenges.pop(challenge, None)
        binding = OperatorBinding(
            binding_id=token_urlsafe(18),
            identity_subject=assertion.subject,
            github_subject=github_subject,
            environment=Environment.ADM,
            capabilities=frozenset(
                {
                    Capability.CONSULT,
                    Capability.SPECIALIST_CONTRIBUTE,
                    Capability.COMMIT,
                    Capability.CREATE_PR,
                    Capability.MERGE_OPERATIONAL,
                    Capability.MERGE_STRUCTURAL,
                    Capability.VIEW_INTERNAL_ARCHITECTURE,
                }
            ),
            repository_scope=frozenset(repository_scope),
        )
        self.bindings[binding.binding_id] = binding
        return binding

    def authorize(
        self,
        binding_id: str,
        capability: Capability,
        repository: str | None = None,
        structural_change: bool = False,
    ) -> AuthorizationResult:
        binding = self.bindings.get(binding_id)
        if binding is None or not binding.active:
            return AuthorizationResult(Decision.DENY, "operator_binding_inactive_or_missing")

        if repository is not None and repository not in binding.repository_scope:
            return AuthorizationResult(Decision.DENY, "repository_outside_authorized_scope")

        if capability not in binding.capabilities:
            return AuthorizationResult(Decision.DENY, "capability_not_granted")

        if structural_change and capability != Capability.MERGE_STRUCTURAL:
            return AuthorizationResult(Decision.DENY, "structural_change_requires_structural_capability")

        if binding.environment in {Environment.VISITOR, Environment.SPECIALIST} and capability in {
            Capability.MERGE_OPERATIONAL,
            Capability.MERGE_STRUCTURAL,
            Capability.VIEW_INTERNAL_ARCHITECTURE,
            Capability.MANAGE_SECURITY,
        }:
            return AuthorizationResult(Decision.DENY, "environment_cannot_perform_privileged_operation")

        return AuthorizationResult(Decision.ALLOW, "authorized")


def classify_external_session(
    *,
    authenticated_identity: bool,
    specialist_authorized: bool,
) -> Environment:
    """Fail closed: unproven privilege becomes VISITOR."""
    if not authenticated_identity:
        return Environment.VISITOR
    if specialist_authorized:
        return Environment.SPECIALIST
    return Environment.VISITOR
