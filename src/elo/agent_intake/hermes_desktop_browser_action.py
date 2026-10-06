"""Candidate-only evidence contract for controlled desktop-browser navigation.

This module does not navigate, click, submit, authenticate, or execute external effects.
It reuses canonical ExecutionBoundary/ExecutionRouter ownership for any future execution.
"""
from dataclasses import dataclass
from enum import StrEnum
from urllib.parse import urlparse
import hashlib


class BrowserActionKind(StrEnum):
    NAVIGATE_READ = "NAVIGATE_READ"
    EXTRACT_READ = "EXTRACT_READ"
    CLICK = "CLICK"
    SUBMIT = "SUBMIT"
    WRITE = "WRITE"


class BrowserDisposition(StrEnum):
    CANDIDATE_ONLY = "CANDIDATE_ONLY"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class DesktopBrowserAction:
    request_id: str
    tenant_id: str
    principal_id: str
    mission_id: str
    url: str
    domain_scope: str
    action_kind: BrowserActionKind
    provenance_ref: str
    authorization_id: str | None = None


@dataclass(frozen=True)
class BrowserActionAssessment:
    request_id: str
    disposition: BrowserDisposition
    execution_permitted: bool
    reason: str
    url_digest: str
    provenance_ref: str


_MUTATING = frozenset({
    BrowserActionKind.CLICK,
    BrowserActionKind.SUBMIT,
    BrowserActionKind.WRITE,
})


def assess_browser_action(action: DesktopBrowserAction) -> BrowserActionAssessment:
    parsed = urlparse(action.url)
    digest = hashlib.sha256(action.url.encode("utf-8")).hexdigest()

    if not all((action.request_id, action.tenant_id, action.principal_id,
                action.mission_id, action.url, action.domain_scope,
                action.provenance_ref)):
        return BrowserActionAssessment(
            action.request_id, BrowserDisposition.BLOCKED, False,
            "missing_browser_action_controls", digest, action.provenance_ref,
        )

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return BrowserActionAssessment(
            action.request_id, BrowserDisposition.BLOCKED, False,
            "invalid_navigation_target", digest, action.provenance_ref,
        )

    if action.action_kind in _MUTATING:
        return BrowserActionAssessment(
            action.request_id, BrowserDisposition.BLOCKED, False,
            "state_changing_browser_action_outside_candidate_scope",
            digest, action.provenance_ref,
        )

    if action.authorization_id is not None:
        return BrowserActionAssessment(
            action.request_id, BrowserDisposition.CANDIDATE_ONLY, False,
            "authorization_recorded_but_execution_requires_canonical_boundary",
            digest, action.provenance_ref,
        )

    return BrowserActionAssessment(
        action.request_id, BrowserDisposition.CANDIDATE_ONLY, False,
        "read_only_browser_action_candidate_not_executable",
        digest, action.provenance_ref,
    )
