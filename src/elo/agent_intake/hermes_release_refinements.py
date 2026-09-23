"""Governed intake contracts for Hermes 0.21.4 refinements.

These contracts are observation/adaptation boundaries only. They do not call Hermes,
mutate Hermes, activate skills, query memory, execute tools, or perform business
operations. They normalize newly exposed Hermes semantics so existing ELO owners can
evaluate them without creating parallel authorities.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


@dataclass(frozen=True)
class SkillAutoLoadCandidate:
    candidate_id: str
    skills: Tuple[str, ...]
    source_revision: str
    candidate_only: bool = True
    canonical_mutation: bool = False


@dataclass(frozen=True)
class SessionSearchBoundsCandidate:
    candidate_id: str
    query: str
    after: str | None = None
    before: str | None = None
    allow_or_relaxed_retry: bool = True
    source_revision: str = ""
    candidate_only: bool = True
    canonical_mutation: bool = False


def observe_skill_autoload(metadata: Mapping[str, object], *, source_revision: str) -> SkillAutoLoadCandidate:
    """Normalize Hermes ``skills.auto_load`` metadata without activating skills."""
    raw = metadata.get("skills.auto_load", ())
    if raw is None:
        skills: tuple[str, ...] = ()
    elif isinstance(raw, str):
        skills = tuple(item.strip() for item in raw.split(",") if item.strip())
    else:
        try:
            skills = tuple(str(item).strip() for item in raw if str(item).strip())
        except TypeError as exc:
            raise ValueError("skills.auto_load must be a string or iterable") from exc
    if len(skills) != len(set(skills)):
        raise ValueError("skills.auto_load contains duplicate skills")
    return SkillAutoLoadCandidate(
        candidate_id="EXT-SKILL-AUTOLOAD-HERMES",
        skills=skills,
        source_revision=source_revision,
    )


def observe_session_search(
    *, query: str, after: str | None = None, before: str | None = None,
    source_revision: str,
) -> SessionSearchBoundsCandidate:
    """Capture bounded Hermes session-search semantics as candidate evidence."""
    if not query.strip():
        raise ValueError("query must not be empty")
    if after and before and after > before:
        raise ValueError("after must not be later than before")
    return SessionSearchBoundsCandidate(
        candidate_id="EXT-SESSION-SEARCH-BOUNDS-HERMES",
        query=query.strip(),
        after=after,
        before=before,
        source_revision=source_revision,
    )


def candidate_metadata(candidate: object) -> dict[str, object]:
    """Expose governance metadata without granting activation or promotion."""
    return {
        "candidate_only": getattr(candidate, "candidate_only"),
        "canonical_mutation": getattr(candidate, "canonical_mutation"),
        "authority": "elo_cognitive",
        "source": "hermes",
    }
