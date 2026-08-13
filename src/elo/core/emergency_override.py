"""Governed emergency override for infrastructure-only validation failures.

This module never converts an unknown or failed test result into PASS. It
only represents an explicitly approved, auditable exception when validation
infrastructure is unavailable and architectural/security gates are otherwise
satisfied.
"""

from dataclasses import dataclass
from enum import StrEnum


class OverrideStatus(StrEnum):
    DENIED = "DENIED"
    PENDING = "PENDING"
    APPROVED = "APPROVED"


ALLOWED_FAILURE_CLASS = "INFRASTRUCTURE_FAILURE"


@dataclass(frozen=True)
class EmergencyOverrideRequest:
    commit_sha: str
    failure_class: str
    reason: str
    architecture_compatible: bool
    human_approved: bool
    risk_accepted: bool
    follow_up_required: bool = True

    def evaluate(self) -> OverrideStatus:
        if self.failure_class != ALLOWED_FAILURE_CLASS:
            return OverrideStatus.DENIED
        if not self.architecture_compatible or not self.human_approved or not self.risk_accepted:
            return OverrideStatus.PENDING
        if not self.follow_up_required:
            return OverrideStatus.DENIED
        return OverrideStatus.APPROVED

    @property
    def validation_status(self) -> str:
        return "UNKNOWN"

    @property
    def merge_metadata(self) -> dict[str, str]:
        return {
            "validation_status": self.validation_status,
            "override": "GOVERNED",
            "follow_up_required": str(self.follow_up_required).lower(),
        }
