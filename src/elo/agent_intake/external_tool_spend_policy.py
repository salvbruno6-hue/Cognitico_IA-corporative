"""Candidate-only spend governance for external tool calls.

Adapted from a Hermes MCP invariant without transferring execution authority.
The policy is deterministic, side-effect free and fail-closed. It never dispatches
a tool and never mutates canonical ELO state.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True, slots=True)
class SpendDecision:
    allowed: bool
    requires_human_approval: bool
    reason: str
    projected_total: Decimal | None


def evaluate_external_tool_spend(
    *,
    declared_cost: str | int | float | Decimal | None,
    running_total: str | int | float | Decimal,
    spend_limit: str | int | float | Decimal | None,
    unattended: bool,
) -> SpendDecision:
    """Evaluate cost policy before dispatch; malformed declarations fail closed."""
    if declared_cost is None or spend_limit is None:
        return SpendDecision(True, False, "no_declared_spend_policy", None)
    try:
        cost = Decimal(str(declared_cost))
        total = Decimal(str(running_total))
        limit = Decimal(str(spend_limit))
    except (InvalidOperation, ValueError):
        return SpendDecision(False, False, "invalid_spend_policy", None)
    if not all(value.is_finite() for value in (cost, total, limit)):
        return SpendDecision(False, False, "invalid_spend_policy", None)
    if cost < 0 or total < 0 or limit < 0:
        return SpendDecision(False, False, "invalid_spend_policy", None)
    projected = total + cost
    if projected <= limit:
        return SpendDecision(True, False, "within_spend_limit", projected)
    if unattended:
        return SpendDecision(False, False, "spend_limit_exceeded_unattended", projected)
    return SpendDecision(False, True, "spend_limit_exceeded_requires_approval", projected)


__all__ = ["SpendDecision", "evaluate_external_tool_spend"]
