"""Canonical identity boundary (ELO Soul).

The canonical identity is intentionally read-only at runtime. Architectural
changes must be performed through an explicit governance process.
"""

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class EloCanonicalIdentity:
    name: str
    purpose: str
    architecture_version: str
    cognitive_core_path: str
    principles: tuple[str, ...]
    canonical_boundaries: tuple[str, ...]
    governance_policy: str
    current_verified_state: str
    metadata: Mapping[str, str]


class CanonicalIdentityRegistry:
    """Read-only registry for the ELO's canonical identity."""

    def __init__(self, identity: EloCanonicalIdentity) -> None:
        self._identity = identity

    def get(self) -> EloCanonicalIdentity:
        return self._identity

    def propose_change(self, reason: str) -> dict[str, str]:
        if not reason.strip():
            raise ValueError("reason is required")
        return {
            "type": "ARCHITECTURAL_CHANGE_PROPOSAL",
            "reason": reason,
            "requires_governance_gate": "true",
        }
