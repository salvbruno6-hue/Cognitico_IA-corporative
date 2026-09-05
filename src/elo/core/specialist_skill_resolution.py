"""Deterministic resolution of a governed Forge specialist skill.

The Forge Specialist Skill Registry remains the source of truth. This module
only resolves an already supplied registry snapshot; it does not define a
second registry, router, authority, or permission model.
"""

from dataclasses import dataclass
from typing import Callable, Iterable, Mapping


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
    reason: str = ""

    @property
    def resolved(self) -> bool:
        return self.status == "RESOLVED"


class SpecialistSkillResolver:
    """Resolve a skill from the canonical Forge registry snapshot."""

    def __init__(self, skills: Iterable[SpecialistSkill] = ()) -> None:
        self._skills = tuple(skills)

    def resolve(
        self,
        *,
        domain_family: str | None,
        authorized: Callable[[SpecialistSkill], bool] | None = None,
        minimum_maturity: str = "STRUCTURED",
    ) -> SpecialistSkillResolution:
        if not domain_family:
            return SpecialistSkillResolution("GAP", reason="domain_family is required")

        candidates = tuple(
            skill for skill in self._skills
            if skill.domain_family == domain_family
        )
        if not candidates:
            return SpecialistSkillResolution(
                "GAP",
                domain_family=domain_family,
                reason="no governed specialist skill is registered for the domain",
            )

        maturity_order = {
            "DEFINED": 0,
            "STRUCTURED": 1,
            "TESTED": 2,
            "EMPIRICALLY_VALIDATED": 3,
            "GOVERNED": 4,
            "CANDIDATE_FOR_CORE_PROMOTION": 5,
        }
        required_level = maturity_order.get(minimum_maturity, 1)
        eligible = tuple(
            skill for skill in candidates
            if maturity_order.get(skill.maturity, -1) >= required_level
        )
        if not eligible:
            return SpecialistSkillResolution(
                "GAP",
                domain_family=domain_family,
                reason="registered skill maturity is below the required threshold",
            )

        authorized_candidates = tuple(
            skill for skill in eligible
            if not skill.authorization_required or (authorized is not None and authorized(skill))
        )
        if not authorized_candidates:
            return SpecialistSkillResolution(
                "BLOCKED",
                domain_family=domain_family,
                reason="specialist authorization was not established",
            )

        selected = sorted(authorized_candidates, key=lambda skill: skill.skill_id)[0]
        return SpecialistSkillResolution(
            "RESOLVED",
            skill_id=selected.skill_id,
            domain_family=selected.domain_family,
            reason="resolved from canonical Forge Specialist Skill Registry snapshot",
        )


def skill_from_registry_record(record: Mapping[str, object]) -> SpecialistSkill:
    """Adapt one declarative Forge registry record without copying the registry."""
    required = ("skill_id", "domain_family", "maturity")
    missing = [field for field in required if not record.get(field)]
    if missing:
        raise ValueError(f"invalid specialist skill registry record; missing: {missing}")
    return SpecialistSkill(
        skill_id=str(record["skill_id"]),
        domain_family=str(record["domain_family"]),
        maturity=str(record["maturity"]),
        scope=str(record.get("scope", "")),
        boundaries=str(record.get("boundaries", "")),
        authorization_required=bool(record.get("authorization_required", True)),
    )
