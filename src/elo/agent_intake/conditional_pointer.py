"""Controlled information-to-capability pointer resolution for ELO.

This is a deterministic laboratory surface only. It does not persist data,
create capabilities, mutate canonical knowledge, authorize external actions,
or promote learning. Repeated resolution of the same input is idempotent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .native_capabilities import CAPABILITY_IDS


@dataclass(frozen=True, slots=True)
class ConditionalPointerEvidence:
    request_id: str
    tenant_scope: str
    condition: str
    matched_capability: str | None
    destination: str | None
    policy_required: bool
    status: str
    evidence: tuple[dict[str, Any], ...]
    learning_candidate: dict[str, Any]


_RULES: tuple[tuple[str, str, str, bool], ...] = (
    ("semantic-recall", "HERMES-MEMORY", "ELO_CONTEXT_MEMORY", True),
    ("context-resolution", "HERMES-CONTEXT", "ELO_CONTEXT", False),
    ("skill-execution", "HERMES-SKILLS", "ELO_SKILL_RUNTIME", True),
    ("tool-resolution", "HERMES-TOOLSETS", "ELO_ROUTING", True),
    ("delegation", "HERMES-DELEGATION", "ELO_ROUTING", True),
    ("schedule", "HERMES-AUTOMATION", "ELO_SCHEDULER", True),
    ("external-capability", "HERMES-MCP", "ELO_ROUTING", True),
    ("state-recovery", "HERMES-CHECKPOINT", "ELO_STATE_RECOVERY", False),
)


def _validate_rule_integrity() -> None:
    """Reject duplicate pointer identities without creating replacement data."""
    conditions = [condition for condition, *_ in _RULES]
    capabilities = [capability_id for _condition, capability_id, *_ in _RULES]

    if len(conditions) != len(set(conditions)):
        raise ValueError("conditional pointer rules contain duplicate conditions")
    if len(capabilities) != len(set(capabilities)):
        raise ValueError("conditional pointer rules contain duplicate capability identities")
    if any(capability_id not in CAPABILITY_IDS for capability_id in capabilities):
        raise ValueError("pointer rule references unknown native capability")


_validate_rule_integrity()


def resolve_pointer(*, request_id: str, tenant_scope: str, information: dict[str, Any]) -> ConditionalPointerEvidence:
    """Resolve an already-known relation without persistence or side effects."""
    condition = str(information.get("condition", "")).strip().lower()
    received = dict(information)

    for rule_condition, capability_id, destination, policy_required in _RULES:
        if condition == rule_condition:
            return ConditionalPointerEvidence(
                request_id=request_id,
                tenant_scope=tenant_scope,
                condition=condition,
                matched_capability=capability_id,
                destination=destination,
                policy_required=policy_required,
                status="resolved",
                evidence=(
                    {"information_received": received},
                    {"relation": {"condition": condition, "capability_id": capability_id}},
                    {"destination": destination, "policy_required": policy_required},
                ),
                learning_candidate={"promotion_state": "candidate_only", "canonical_mutation": False},
            )

    return ConditionalPointerEvidence(
        request_id=request_id,
        tenant_scope=tenant_scope,
        condition=condition,
        matched_capability=None,
        destination=None,
        policy_required=False,
        status="unresolved",
        evidence=({"information_received": received},),
        learning_candidate={"promotion_state": "candidate_only", "canonical_mutation": False},
    )


def validate_pointer_matrix(*, tenant_scope: str = "multiteiner") -> tuple[ConditionalPointerEvidence, ...]:
    results = tuple(
        resolve_pointer(
            request_id=f"pointer-{index:02d}",
            tenant_scope=tenant_scope,
            information={"condition": condition, "source": "controlled-lab"},
        )
        for index, (condition, _capability_id, _destination, _policy) in enumerate(_RULES, 1)
    )
    expected = {capability_id for _condition, capability_id, _destination, _policy in _RULES}
    if {result.matched_capability for result in results} != expected:
        raise AssertionError("conditional pointer matrix did not resolve one-to-one")
    if any(result.status != "resolved" for result in results):
        raise AssertionError("conditional pointer matrix contains unresolved conditions")
    if any(result.learning_candidate["canonical_mutation"] for result in results):
        raise AssertionError("conditional pointer lab attempted canonical mutation")
    return results


__all__ = ["ConditionalPointerEvidence", "resolve_pointer", "validate_pointer_matrix"]
