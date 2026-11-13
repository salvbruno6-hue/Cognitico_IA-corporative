"""Bounded ingestion of concrete OpenClaw skills into the ELO candidate loop.

OpenClaw is an operational experience source for concrete skill candidates.
It is not an ELO authority and is never copied into the native runtime merely
because a source file exists. This module only creates explicit, traceable
candidate records; validation, execution and Evolution Gate remain ELO-owned.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

OPENCLAW_SKILLS_SOURCE = "src/agents/skills/plugin-skills.ts"


@dataclass(frozen=True, slots=True)
class OpenClawSkillCandidate:
    candidate_id: str
    capability_id: str
    skill_name: str
    source_repository: str
    source_ref: str
    source_path: str
    mechanism: str
    state: str = "CANDIDATE"
    promotion_state: str = "candidate_only"
    canonical_mutation: bool = False


def discover_skill_candidates(
    skills: Iterable[Mapping[str, str]],
    *,
    source_repository: str,
    source_ref: str,
    capability_id: str = "HERMES-SKILLS",
) -> tuple[OpenClawSkillCandidate, ...]:
    """Convert concrete OpenClaw skill metadata into bounded ELO candidates.

    Input records must provide ``name`` and ``path``. Empty values are rejected.
    The source path is preserved verbatim for provenance and is not interpreted
    as executable code. Duplicate ``name`` + ``path`` pairs are consolidated.
    """
    if not source_repository.strip() or not source_ref.strip():
        raise ValueError("source_repository and source_ref are required")
    if not capability_id.strip():
        raise ValueError("capability_id is required")

    candidates: list[OpenClawSkillCandidate] = []
    seen: set[tuple[str, str]] = set()
    for item in skills:
        name = item.get("name", "").strip()
        path = item.get("path", "").strip()
        if not name or not path:
            raise ValueError("each skill candidate requires name and path")
        key = (name, path)
        if key in seen:
            continue
        seen.add(key)
        candidate_id = f"OPENCLAW-SKILL::{name}::{path}"
        candidates.append(
            OpenClawSkillCandidate(
                candidate_id=candidate_id,
                capability_id=capability_id,
                skill_name=name,
                source_repository=source_repository,
                source_ref=source_ref,
                source_path=path,
                mechanism="OpenClaw concrete operational skill",
            )
        )
    return tuple(candidates)


__all__ = ["OPENCLAW_SKILLS_SOURCE", "OpenClawSkillCandidate", "discover_skill_candidates"]
