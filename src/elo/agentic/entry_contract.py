"""Canonical entry boundary for AI connections to the ELO repository.

This module validates the *entry contract* only. It does not authenticate
GitHub, authorize operators, read the repository, execute tools, persist
memory, or promote knowledge. Those responsibilities remain with their
existing canonical owners.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


class ELOAIEntryError(ValueError):
    """Base error for fail-closed ELO AI entry validation."""


class ELOAIEntryMode(StrEnum):
    READ_ONLY_CONSULTATION = "READ_ONLY_CONSULTATION"
    AUTHORIZED_SPECIALIST = "AUTHORIZED_SPECIALIST"
    GOVERNED_EXECUTION = "GOVERNED_EXECUTION"


class ELOAIEntryState(StrEnum):
    READY = "READY"
    BLOCKED = "BLOCKED"


class ELOAIEntryBlock(StrEnum):
    BOOTSTRAP_INCOMPLETE = "BOOTSTRAP_INCOMPLETE"
    ACCESS_SCOPE_VIOLATION = "ACCESS_SCOPE_VIOLATION"
    IDENTITY_UNBOUND = "IDENTITY_UNBOUND"
    AUTHORIZATION_REQUIRED = "AUTHORIZATION_REQUIRED"
    CONTRACT_CONFLICT = "CONTRACT_CONFLICT"


DEFAULT_BOOTSTRAP_ARTIFACTS: tuple[str, ...] = (
    "AGENTS.md",
    "ELO_REPOSITORY_NAVIGATION_RULES.md",
    "ELO_AI_AGENT_WORKING_RULES.md",
    "ELO_OPERATING_RULES.md",
    "ELO_CONSTRAINTS.md",
    "ELO_BOOTSTRAP.md",
)


@dataclass(frozen=True)
class ELOAIEntryRequest:
    repository: str
    connector: str
    session_id: str
    repository_ref: str = "main"
    requested_mode: ELOAIEntryMode = ELOAIEntryMode.READ_ONLY_CONSULTATION
    tenant_id: str | None = None
    domain: str | None = None
    principal_id: str | None = None
    request_id: str | None = None
    correlation_id: str | None = None
    authorization_scope: str | None = None
    authenticated_github_identity: str | None = None
    elo_operator_record: str | None = None
    capability: str | None = None
    operation_classification: str | None = None

    def __post_init__(self) -> None:
        if not self.repository.strip():
            raise ELOAIEntryError("repository is required")
        if not self.connector.strip():
            raise ELOAIEntryError("connector is required")
        if not self.session_id.strip():
            raise ELOAIEntryError("session_id is required")
        if not self.repository_ref.strip():
            raise ELOAIEntryError("repository_ref is required")


@dataclass(frozen=True)
class ELOAIEntrySession:
    repository: str
    connector: str
    session_id: str
    repository_ref: str
    mode: ELOAIEntryMode
    state: ELOAIEntryState
    bootstrap_artifacts: tuple[str, ...]
    tenant_id: str | None = None
    domain: str | None = None
    principal_id: str | None = None
    request_id: str | None = None
    correlation_id: str | None = None
    authorization_scope: str | None = None
    block: ELOAIEntryBlock | None = None

    @property
    def execution_binding_ready(self) -> bool:
        """Indicate that the entry contract accepted the execution binding.

        This is not an authorization decision. The canonical authorization
        system remains responsible for granting the actual operation.
        """
        return self.state is ELOAIEntryState.READY and self.mode is ELOAIEntryMode.GOVERNED_EXECUTION


class ELOAIEntryGate:
    """Fail-closed validator for the connection-to-ELO boundary."""

    def __init__(self, *, bootstrap_artifacts: tuple[str, ...] = DEFAULT_BOOTSTRAP_ARTIFACTS) -> None:
        self.bootstrap_artifacts = tuple(dict.fromkeys(bootstrap_artifacts))
        if not self.bootstrap_artifacts:
            raise ELOAIEntryError("bootstrap_artifacts cannot be empty")

    def establish(
        self,
        request: ELOAIEntryRequest,
        *,
        readable_artifacts: tuple[str, ...],
        access_scope_valid: bool = True,
        contract_conflict: bool = False,
    ) -> ELOAIEntrySession:
        readable = set(readable_artifacts)
        common = dict(
            repository=request.repository,
            connector=request.connector,
            session_id=request.session_id,
            repository_ref=request.repository_ref,
            mode=request.requested_mode,
            bootstrap_artifacts=self.bootstrap_artifacts,
            tenant_id=request.tenant_id,
            domain=request.domain,
            principal_id=request.principal_id,
            request_id=request.request_id,
            correlation_id=request.correlation_id,
            authorization_scope=request.authorization_scope,
        )

        missing = tuple(item for item in self.bootstrap_artifacts if item not in readable)
        if missing:
            return ELOAIEntrySession(
                **common,
                state=ELOAIEntryState.BLOCKED,
                block=ELOAIEntryBlock.BOOTSTRAP_INCOMPLETE,
            )

        if not access_scope_valid:
            return ELOAIEntrySession(
                **common,
                state=ELOAIEntryState.BLOCKED,
                block=ELOAIEntryBlock.ACCESS_SCOPE_VIOLATION,
            )

        if contract_conflict:
            return ELOAIEntrySession(
                **common,
                state=ELOAIEntryState.BLOCKED,
                block=ELOAIEntryBlock.CONTRACT_CONFLICT,
            )

        if request.requested_mode is ELOAIEntryMode.READ_ONLY_CONSULTATION:
            return ELOAIEntrySession(**common, state=ELOAIEntryState.READY)

        if not request.principal_id or not request.authorization_scope:
            return ELOAIEntrySession(
                **common,
                state=ELOAIEntryState.BLOCKED,
                block=ELOAIEntryBlock.IDENTITY_UNBOUND,
            )

        if request.requested_mode is ELOAIEntryMode.AUTHORIZED_SPECIALIST:
            if not (
                request.tenant_id
                and request.domain
                and request.authenticated_github_identity
                and request.elo_operator_record
                and request.capability
            ):
                return ELOAIEntrySession(
                    **common,
                    state=ELOAIEntryState.BLOCKED,
                    block=ELOAIEntryBlock.AUTHORIZATION_REQUIRED,
                )
            return ELOAIEntrySession(**common, state=ELOAIEntryState.READY)

        if not (
            request.authenticated_github_identity
            and request.elo_operator_record
            and request.capability
            and request.operation_classification
            and request.request_id
            and request.correlation_id
        ):
            return ELOAIEntrySession(
                **common,
                state=ELOAIEntryState.BLOCKED,
                block=ELOAIEntryBlock.AUTHORIZATION_REQUIRED,
            )

        return ELOAIEntrySession(**common, state=ELOAIEntryState.READY)

    @staticmethod
    def from_request_context(
        *,
        repository: str,
        connector: str,
        requested_mode: ELOAIEntryMode,
        session_id: str,
        repository_ref: str = "main",
        context: Mapping[str, str],
    ) -> ELOAIEntryRequest:
        return ELOAIEntryRequest(
            repository=repository,
            connector=connector,
            session_id=session_id,
            repository_ref=repository_ref,
            requested_mode=requested_mode,
            tenant_id=context.get("tenant_id"),
            domain=context.get("domain"),
            principal_id=context.get("principal_id"),
            request_id=context.get("request_id"),
            correlation_id=context.get("correlation_id"),
            authorization_scope=context.get("authorization_scope"),
            authenticated_github_identity=context.get("authenticated_github_identity"),
            elo_operator_record=context.get("elo_operator_record"),
            capability=context.get("capability"),
            operation_classification=context.get("operation_classification"),
        )
