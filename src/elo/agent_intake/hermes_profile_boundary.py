"""Governed intake boundary for Hermes profiles/Bot Mode.

This module records Hermes profile capabilities as candidate-only ELO
adaptations. It does not create profiles, execute agents, share memory,
authorize delegation, or promote candidates.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


CAPABILITY_ID = "EXT-PROFILE-HERMES"


class ProfileDisposition(str, Enum):
    OBSERVATION = "OBSERVATION"
    CANDIDATE = "CANDIDATE"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class ProfileSignal:
    profile_id: str
    tenant_scope: str
    source_refs: Tuple[str, ...]
    identity_digest: str
    isolated_state: bool
    explicit_activation: bool
    shared_canonical_memory: bool
    authority_transfer: bool


@dataclass(frozen=True, slots=True)
class ProfileAssessment:
    profile_id: str
    disposition: ProfileDisposition
    evidence_refs: Tuple[str, ...]
    canonical_authority: bool = False
    execution_permitted: bool = False
    promotion_permitted: bool = False


def assess_profile(signal: ProfileSignal) -> ProfileAssessment:
    if not signal.profile_id or not signal.tenant_scope or not signal.identity_digest:
        return ProfileAssessment(
            signal.profile_id,
            ProfileDisposition.REJECTED,
            signal.source_refs,
        )

    if not signal.source_refs or signal.authority_transfer:
        return ProfileAssessment(
            signal.profile_id,
            ProfileDisposition.REJECTED,
            signal.source_refs,
        )

    if signal.shared_canonical_memory:
        return ProfileAssessment(
            signal.profile_id,
            ProfileDisposition.OBSERVATION,
            signal.source_refs,
        )

    if not signal.isolated_state or not signal.explicit_activation:
        return ProfileAssessment(
            signal.profile_id,
            ProfileDisposition.OBSERVATION,
            signal.source_refs,
        )

    return ProfileAssessment(
        signal.profile_id,
        ProfileDisposition.CANDIDATE,
        signal.source_refs,
    )


__all__ = [
    "CAPABILITY_ID",
    "ProfileAssessment",
    "ProfileDisposition",
    "ProfileSignal",
    "assess_profile",
]
