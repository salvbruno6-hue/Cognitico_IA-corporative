"""Deterministic resolution and pre-intake assessment of governed Forge specialist skills.

The Forge Specialist Skill Registry remains the source of truth. This module
resolves an explicitly supplied registry snapshot and provides a read-only
pre-intake assessment that checks whether the components required by a proposed
skill already exist before Symbiont intake proceeds.

The pre-intake assessment never creates a skill, registry entry, capability,
permission, persistence record, or learning promotion.
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

_COMPONENT_STATUS = {"FOUND", "PARTIAL", "MISSING"}


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


@dataclass(frozen=True)
class SkillPreIntakeComponent:
    """Evidence about one component required by a proposed skill."""

    name: str
    status: str
    path: str = ""
    gap: str = ""

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("pre-intake component name is required")
        if self.status not in _COMPONENT_STATUS:
            raise ValueError(f"unknown pre-intake component status: {self.status}")


@dataclass(frozen=True)
class SkillPreIntakeResult:
    """Read-only composition/readiness result consumed by Symbiont intake."""

    skill_id: str
    domain_family: str
    status: str
    decision: str
    readiness_score: float
    components: tuple[SkillPreIntakeComponent, ...]
    existing_skill_id: str | None = None
    evidence: tuple[dict[str, object], ...] = ()

    @property
    def ready_for_intake(self) -> bool:
        return self.decision == "READY_FOR_INTAKE"

    @property
    def develop_first(self) -> bool:
        return self.decision == "DEVELOP_FIRST"

    @property
    def reuse_existing(self) -> bool:
        return self.decision == "REUSE_EXISTING"


class SpecialistSkillResolver:
    """Resolve skills and assess proposed-skill pre-intake.

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

    def pre_intake(
        self,
        *,
        skill_id: str,
        domain_family: str,
        required_components: Iterable[SkillPreIntakeComponent],
        authorized: Callable[[SpecialistSkill], bool] | None = None,
        minimum_maturity: str = "STRUCTURED",
    ) -> SkillPreIntakeResult:
        """Check composition readiness before Symbiont creates/absorbs a skill.

        The supplied component inventory is evidence only. Existing governed
        skills are checked first so an equivalent capability is reused instead
        of producing a duplicate skill.
        """
        if not skill_id.strip():
            raise ValueError("skill_id is required")
        if not domain_family.strip():
            raise ValueError("domain_family is required")

        components = tuple(required_components)
        if not components:
            return SkillPreIntakeResult(
                skill_id=skill_id,
                domain_family=domain_family,
                status="BLOCKED",
                decision="DEVELOP_FIRST",
                readiness_score=0.0,
                components=(),
                evidence=(
                    {"reason": "no required components were supplied"},
                ),
            )

        duplicate = self._resolve_existing_for_pre_intake(
            domain_family=domain_family,
            authorized=authorized,
            minimum_maturity=minimum_maturity,
        )
        if duplicate.resolved:
            return SkillPreIntakeResult(
                skill_id=skill_id,
                domain_family=domain_family,
                status="REUSE_EXISTING",
                decision="REUSE_EXISTING",
                readiness_score=1.0,
                components=components,
                existing_skill_id=duplicate.skill_id,
                evidence=(
                    {"reason": "existing governed specialist skill matches the domain"},
                    {"existing_skill_id": duplicate.skill_id, "maturity": duplicate.maturity},
                ),
            )

        found = sum(component.status == "FOUND" for component in components)
        readiness = round(found / len(components), 3)
        missing_or_partial = tuple(
            component
            for component in components
            if component.status != "FOUND"
        )

        if missing_or_partial:
            status = "BLOCKED"
            decision = "DEVELOP_FIRST"
            reason = "required components are missing or only partially available"
        else:
            status = "READY"
            decision = "READY_FOR_INTAKE"
            reason = "required components are available and no governed duplicate was resolved"

        return SkillPreIntakeResult(
            skill_id=skill_id,
            domain_family=domain_family,
            status=status,
            decision=decision,
            readiness_score=readiness,
            components=components,
            evidence=(
                {"reason": reason},
                {"required_components": len(components), "found_components": found},
            ),
        )

    def _resolve_existing_for_pre_intake(
        self,
        *,
        domain_family: str,
        authorized: Callable[[SpecialistSkill], bool] | None,
        minimum_maturity: str,
    ) -> SpecialistSkillResolution:
        """Resolve only a reusable existing skill; never invent one."""
        return self.resolve(
            domain_family=domain_family,
            authorized=authorized,
            minimum_maturity=minimum_maturity,
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
