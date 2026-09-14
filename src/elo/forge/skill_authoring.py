"""Governed, provider-neutral authoring of ELO Forge capabilities.

This module extracts reusable authoring discipline from external skill systems
without making any provider a canonical authority. It validates a proposed
capability artifact and returns a candidate; it never writes the Forge registry,
changes Core, grants authorization, or promotes knowledge.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping


class SkillAuthoringError(ValueError):
    """Raised when a skill candidate violates the native ELO authoring contract."""


@dataclass(frozen=True)
class SkillCandidate:
    skill_id: str
    description: str
    version: str
    platforms: tuple[str, ...]
    body: str
    provenance: Mapping[str, str]
    state: str = "CANDIDATE"


class NativeSkillAuthoring:
    """Validate and prepare a governed Forge skill candidate."""

    _NAME = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
    _SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

    def prepare(
        self,
        *,
        skill_id: str,
        description: str,
        version: str,
        platforms: tuple[str, ...] | list[str],
        body: str,
        provenance: Mapping[str, str],
        existing_skill_ids: tuple[str, ...] = (),
    ) -> SkillCandidate:
        skill_id = skill_id.strip()
        description = description.strip()
        version = version.strip()
        body = body.strip()
        normalized_platforms = tuple(sorted({p.strip().lower() for p in platforms if p.strip()}))
        if not self._NAME.fullmatch(skill_id):
            raise SkillAuthoringError("skill_id must be lowercase kebab-case and <= 64 characters")
        if skill_id in set(existing_skill_ids):
            raise SkillAuthoringError("existing skill must be extended or reconciled, not duplicated")
        if not description or len(description) > 60 or not description.endswith("."):
            raise SkillAuthoringError("description must be one sentence, <= 60 characters, ending with a period")
        if not self._SEMVER.fullmatch(version):
            raise SkillAuthoringError("version must use semantic versioning")
        if not normalized_platforms:
            raise SkillAuthoringError("at least one platform is required")
        if not body:
            raise SkillAuthoringError("skill body is required")
        if not provenance.get("source_ref") or not provenance.get("source_commit"):
            raise SkillAuthoringError("provenance requires source_ref and source_commit")
        return SkillCandidate(
            skill_id=skill_id,
            description=description,
            version=version,
            platforms=normalized_platforms,
            body=body,
            provenance=dict(provenance),
        )
