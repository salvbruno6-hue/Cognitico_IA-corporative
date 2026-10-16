"""Pure ELO-side skill inventory change detection inspired by Hermes.

No filesystem is read here and no skill is activated. Callers provide governed
skill metadata; this module only produces deterministic change evidence for the
existing ELO Knowledge & Skills owner.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class SkillInventoryDelta:
    before_digest: str
    after_digest: str
    added: tuple[str, ...]
    removed: tuple[str, ...]
    changed: tuple[str, ...]

    @property
    def has_change(self) -> bool:
        return self.before_digest != self.after_digest


def _normalize(inventory: Mapping[str, str]) -> tuple[tuple[str, str], ...]:
    normalized = tuple(sorted((str(name).strip(), str(signature).strip()) for name, signature in inventory.items()))
    if any(not name or not signature for name, signature in normalized):
        raise ValueError("skill inventory requires non-empty names and signatures")
    if len({name for name, _ in normalized}) != len(normalized):
        raise ValueError("skill inventory names must be unique")
    return normalized


def inventory_digest(inventory: Mapping[str, str]) -> str:
    payload = json.dumps(_normalize(inventory), separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def detect_skill_inventory_delta(before: Mapping[str, str], after: Mapping[str, str]) -> SkillInventoryDelta:
    old = dict(_normalize(before))
    new = dict(_normalize(after))
    old_names = set(old)
    new_names = set(new)
    return SkillInventoryDelta(
        before_digest=inventory_digest(old),
        after_digest=inventory_digest(new),
        added=tuple(sorted(new_names - old_names)),
        removed=tuple(sorted(old_names - new_names)),
        changed=tuple(sorted(name for name in old_names & new_names if old[name] != new[name])),
    )


__all__ = ["SkillInventoryDelta", "detect_skill_inventory_delta", "inventory_digest"]
