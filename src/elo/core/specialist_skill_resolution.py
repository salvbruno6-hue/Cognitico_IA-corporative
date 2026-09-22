"""Deterministic resolution of governed Forge specialist skills.

The Forge Specialist Skill Registry remains the source of truth. This module
resolves an explicitly supplied registry snapshot and does not create a second
registry, router, authority, permission model, or persistent state.
"""

from dataclasses import dataclass
from typing import Callable, Iterable, Mapping


_MATURITY_ORDER = {
    "DEFINED": 0,
    "STRUCTURED": 1,
    "TESTED": 2,
    "EMPIRICALLY_VALIDATED": 3,
    "GOVERNED": 4,
    "CANDIDATE_FOR_CORE_PROMOTION": 5,
}


@dataclass(frozen=True)
class SpecialistSkill:
    """Minimal runtime view of a Forge registry entry."""

    skill_id: str
    domain_family: str
    maturity: str
    scope: str = ""
    boundaries: str = ""
    authorization_required: bool = True


@dataclass(frozen=True)
class SpecialistSkillResolution:
    """Result of resolving one governed skill for a contextual domain."""

    status: str
    skill_id: str | None = None
    domain_family: str | None = None
    maturity: str | None = None
    reason: str = ""

    @property
    def resolved(self) -> bool:
        return self.status == "RESOLVED"


class SpecialistSkillResolver:
    """Resolve a skill from the canonical Forge registry snapshot.

    Resolution is deterministic: exact domain match, minimum maturity,
    authorization callback, then a stable skill-id tie-break. The resolver
    never persists, mutates, or promotes a skill.
    """

    def __init__(self, skills: Iterable[SpecialistSkill] = ()) -> None:
        self._skills = tuple(skills)

    @staticmethod
    def _maturity_level(value: str) -> int:
        return _MATURITY_ORDER.get(value, -1)

    def resolve(
        self,
        *,
        domain_family: str | None,
        authorized: Callable[[SpecialistSkill], bool] | None = None,
        minimum_maturity: str = "STRUCTURED",
    ) -> SpecialistSkillResolution:
        if not domain_family:
            return SpecialistSkillResolution("GAP", reason="domain_family is required")
        if minimum_maturity not in _MATURITY_ORDER:
            return SpecialistSkillResolution(
                "BLOCKED",
                domain_family=domain_family,
                reason="unknown minimum_maturity",
            )

        candidates = tuple(
            skill for skill in self._skills if skill.domain_family == domain_family
        )
        if not candidates:
            return SpecialistSkillResolution(
                "GAP",
                domain_family=domain_family,
                reason="no governed specialist skill is registered for the domain",
            )

        required_level = self._maturity_level(minimum_maturity)
        mature = tuple(
            skill
            for skill in candidates
            if self._maturity_level(skill.maturity) >= required_level
        )
        if not mature:
            return SpecialistSkillResolution(
                "BLOCKED",
                domain_family=domain_family,
                reason="registered skills do not meet minimum maturity",
            )

        if authorized is not None:
            authorized_candidates = tuple(skill for skill in mature if authorized(skill))
        else:
            authorized_candidates = tuple(
                skill for skill in mature if not skill.authorization_required
            )

        if not authorized_candidates:
            return SpecialistSkillResolution(
                "BLOCKED",
                domain_family=domain_family,
                reason="no candidate is authorized for this context",
            )

        # Stable tie-break: highest maturity first, then lexical skill id.
        selected = min(
            authorized_candidates,
            key=lambda skill: (-self._maturity_level(skill.maturity), skill.skill_id),
        )
        return SpecialistSkillResolution(
            "RESOLVED",
            skill_id=selected.skill_id,
            domain_family=selected.domain_family,
            maturity=selected.maturity,
            reason="resolved from governed Forge registry snapshot",
        )


def skill_from_registry_record(record: Mapping[str, object]) -> SpecialistSkill:
    """Convert a canonical Forge registry mapping into a runtime skill view."""

    skill_id = str(record.get("skill_id", "")).strip()
    domain_family = str(record.get("domain_family", "")).strip()
    maturity = str(record.get("maturity", "")).strip()
    if not skill_id or not domain_family or not maturity:
        raise ValueError("registry record requires skill_id, domain_family and maturity")

    return SpecialistSkill(
        skill_id=skill_id,
        domain_family=domain_family,
        maturity=maturity,
        scope=str(record.get("scope", "") or ""),
        boundaries=str(record.get("boundaries", "") or ""),
        authorization_required=bool(record.get("authorization_required", True)),
    )
