"""Candidate policy for fail-closed pre-inference veto handling.

This module adapts a Hermes discovery into the existing ELO Core/Policy boundary.
It does not execute models, tools, memory providers, or business operations.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Any


class VetoDecision(str, Enum):
    PROCEED = "PROCEED"
    BLOCK = "BLOCK"
    INVALID = "INVALID"


@dataclass(frozen=True)
class PreInferenceVetoResult:
    decision: VetoDecision
    reason: str
    inference_allowed: bool
    external_memory_allowed: bool
    background_review_allowed: bool
    compaction_allowed: bool


def evaluate_pre_inference_veto(policy_result: Mapping[str, Any]) -> PreInferenceVetoResult:
    """Classify a policy result before any inference/context egress.

    Only an explicit ``allow`` or an explicit ``block`` with a non-empty message is
    accepted. Malformed/unknown decisions fail closed. A block disables inference and
    all auxiliary context egresses for the turn; it does not grant execution authority.
    """
    if not isinstance(policy_result, Mapping):
        return _blocked(VetoDecision.INVALID, "invalid_policy_result")

    action = policy_result.get("action")
    if not isinstance(action, str):
        return _blocked(VetoDecision.INVALID, "invalid_action")

    action = action.strip().lower()
    if action == "allow":
        return PreInferenceVetoResult(
            decision=VetoDecision.PROCEED,
            reason="explicit_allow",
            inference_allowed=True,
            external_memory_allowed=True,
            background_review_allowed=True,
            compaction_allowed=True,
        )

    if action == "block":
        message = policy_result.get("message")
        if not isinstance(message, str) or not message.strip():
            return _blocked(VetoDecision.INVALID, "block_requires_message")
        return _blocked(VetoDecision.BLOCK, "policy_block")

    return _blocked(VetoDecision.INVALID, "unknown_action")


def _blocked(decision: VetoDecision, reason: str) -> PreInferenceVetoResult:
    return PreInferenceVetoResult(
        decision=decision,
        reason=reason,
        inference_allowed=False,
        external_memory_allowed=False,
        background_review_allowed=False,
        compaction_allowed=False,
    )
