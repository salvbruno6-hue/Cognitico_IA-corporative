"""Controlled capability-policy resolution attached to existing ELO routing.

Laboratory only: deterministic, side-effect free, no authorization grant,
no external execution, no canonical mutation, and no learning promotion.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .native_capabilities import CAPABILITY_IDS


@dataclass(frozen=True, slots=True)
class CapabilityPolicyEvidence:
    request_id: str
    tenant_scope: str
    capability_id: str | None
    policy: str
    authorized: bool
    scope_ok: bool
    risk: str
    approval_required: bool
    status: str
    evidence: tuple[dict[str, Any], ...]
    learning_candidate: dict[str, Any]


def resolve_capability_policy(*, request_id: str, tenant_scope: str, capability_id: str, policy: str, authorized: bool, requested_scope: str, allowed_scope: str, risk: str = "low") -> CapabilityPolicyEvidence:
    """Evaluate policy signals without granting permission or executing anything."""
    if capability_id not in CAPABILITY_IDS:
        return _result(request_id, tenant_scope, None, policy, False, False, risk, False, "unresolved", "unknown capability")
    policy = policy.strip().lower()
    risk = risk.strip().lower()
    policy_allows = policy == "allowlist"
    scope_ok = requested_scope == allowed_scope and bool(requested_scope)
    approval_required = risk in {"high", "critical"}
    permitted = bool(authorized and policy_allows and scope_ok and not approval_required)
    status = "authorized" if permitted else "blocked"
    return _result(request_id, tenant_scope, capability_id, policy, permitted, scope_ok, risk, approval_required, status, "policy evaluated")


def _result(request_id: str, tenant_scope: str, capability_id: str | None, policy: str, authorized: bool, scope_ok: bool, risk: str, approval_required: bool, status: str, reason: str) -> CapabilityPolicyEvidence:
    return CapabilityPolicyEvidence(
        request_id=request_id, tenant_scope=tenant_scope, capability_id=capability_id,
        policy=policy, authorized=authorized, scope_ok=scope_ok, risk=risk,
        approval_required=approval_required, status=status,
        evidence=({"reason": reason}, {"policy": policy, "scope_ok": scope_ok, "risk": risk, "approval_required": approval_required}),
        learning_candidate={"promotion_state": "candidate_only", "canonical_mutation": False},
    )


__all__ = ["CapabilityPolicyEvidence", "resolve_capability_policy"]
