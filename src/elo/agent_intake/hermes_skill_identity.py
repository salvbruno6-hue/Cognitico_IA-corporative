"""Governed skill-execution identity boundary derived from Hermes observations.

This adapter validates identity metadata already carried by ELO's canonical
HermesExecutionRequest. It does not authorize, execute, persist memory, or
promote learning.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence

SKILL_CAPABILITIES = frozenset({"skill:create", "skill:execute"})


def validate_skill_execution_identity(
    *,
    context: Mapping[str, object],
    authorized_capabilities: Sequence[str],
) -> None:
    """Require skill and decision identity only for governed skill execution."""
    if not SKILL_CAPABILITIES.intersection(authorized_capabilities):
        return

    skill_id = context.get("skill_id")
    decision_id = context.get("decision_id")

    if not isinstance(skill_id, str) or not skill_id.strip():
        raise ValueError("skill_id is required for governed skill execution")

    if not isinstance(decision_id, str) or not decision_id.strip():
        raise ValueError("decision_id is required for governed skill execution")


__all__ = ["SKILL_CAPABILITIES", "validate_skill_execution_identity"]
