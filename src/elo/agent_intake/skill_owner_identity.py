"""Candidate-only owner-aware skill identity derived from Hermes observations.

No plugin is loaded and no skill is activated here. The helper only normalizes
already-governed metadata so inventory evidence cannot collapse two skills that
share a display name but belong to different owners.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SkillIdentity:
    owner: str
    name: str

    @property
    def qualified_name(self) -> str:
        return f"{self.owner}:{self.name}"


def normalize_skill_identity(owner: str, name: str) -> SkillIdentity:
    owner = owner.strip()
    name = name.strip()
    if not owner or not name:
        raise ValueError("skill owner and name are required")
    if ":" in owner or ":" in name:
        raise ValueError("owner and name must be unqualified components")
    return SkillIdentity(owner=owner, name=name)


def identities_collide(left: SkillIdentity, right: SkillIdentity) -> bool:
    """Collision exists only when the full governed identity is identical."""
    return left == right


__all__ = ["SkillIdentity", "normalize_skill_identity", "identities_collide"]
