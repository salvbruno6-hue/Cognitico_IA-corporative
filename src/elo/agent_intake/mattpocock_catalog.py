"""Verified external skill reference adapter, subordinate to ELO canonical authorities.

Vendors are untrusted data; this module never executes skill text or scripts.
Skills are not registered as canonical Core or Forge skills merely by import.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path
import json
from typing import Mapping

PINNED_SOURCE = "4ae2317ddb22b046e26455e4f9c9b3aaaf62212d"
SOURCE_REPOSITORY = "mattpocock/skills"


@dataclass(frozen=True, slots=True)
class ExternalSkillReference:
    skill_id: str
    name: str
    category: str
    source_ref: str
    source_commit: str
    git_blob_sha: str
    source_text: str
    upstream_promoted: bool
    manual_only: bool = True

    @property
    def evidence_ref(self) -> str:
        return f"git-blob:{self.git_blob_sha}"


def _file_at(root: Path, relative: str) -> Path:
    """Refuse traversal and symlink escape even when a manifest is modified."""
    if not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError("skill catalog path is not a safe repository-relative path")
    base = root.resolve()
    target = (base / relative).resolve()
    if not target.is_relative_to(base):
        raise ValueError("skill catalog path escapes the canonical repository")
    if not target.is_file():
        raise ValueError("skill catalog source file is missing")
    return target


def _git_hash(content: bytes) -> str:
    return sha1(b"blob " + str(len(content)).encode("ascii") + b"\0" + content).hexdigest()


class ExternalSkillCatalog:
    """Read-only transport of the immutable vendored Matt Pocock catalog.

    This class is not a registry, a skill selector, an authorization authority,
    a policy store, an agent launcher, or an execution boundary.
    """

    def __init__(self, root: Path | None = None):
        self.root = (root or Path(__file__).resolve().parents[3]).resolve()
        location = _file_at(self.root, "vendor/mattpocock-skills/manifest.json")
        manifest: Mapping[str, object] = json.loads(location.read_text(encoding="utf-8"))
        if (
            manifest.get("source") != SOURCE_REPOSITORY
            or manifest.get("commit") != PINNED_SOURCE
            or manifest.get("skills_count") != 39
            or manifest.get("source_file_count") != 114
            or manifest.get("promoted_count") != 27
        ):
            raise ValueError("external skill catalog source or inventory drift")
        original = manifest.get("original_files")
        installed = manifest.get("installed_skills")
        if not isinstance(original, dict) or len(original) != 114:
            raise ValueError("external skill file inventory is incomplete")
        if not isinstance(installed, list) or len(installed) != 39:
            raise ValueError("external skill names are incomplete")
        lookup: dict[str, Mapping[str, object]] = {}
        for skill in installed:
            if not isinstance(skill, dict):
                raise ValueError("invalid skill descriptor")
            name = skill.get("name")
            category = skill.get("category")
            path = skill.get("source")
            wrapper = skill.get("wrapper")
            if not isinstance(name, str) or not name or "/" in name:
                raise ValueError("invalid external skill identity")
            if category not in {"engineering", "productivity", "misc", "in-progress"}:
                raise ValueError("invalid external skill category")
            expected_path = f"vendor/mattpocock-skills/skills/{category}/{name}/SKILL.md"
            if path != expected_path or skill.get("automatic_invocation") is not False:
                raise ValueError("skill source, scope or manual-only policy mismatch")
            if wrapper != f".agents/skills/mattpocock-{name}/SKILL.md":
                raise ValueError("external skill wrapper mismatch")
            wrapper_text = _file_at(self.root, wrapper).read_text(encoding="utf-8")
            policy = _file_at(
                self.root, f".agents/skills/mattpocock-{name}/agents/openai.yaml"
            ).read_text(encoding="utf-8")
            if (
                "disable-model-invocation: true" not in wrapper_text
                or "allow_implicit_invocation: false" not in policy
            ):
                raise ValueError("external skill implicit execution is prohibited")
            source_path = path.removeprefix("vendor/mattpocock-skills/")
            if source_path not in original or name in lookup:
                raise ValueError("missing or duplicate external skill identity")
            lookup[name] = skill
        self._lookup = lookup
        self._hashes = original

    @property
    def skill_ids(self) -> tuple[str, ...]:
        return tuple(sorted(f"mattpocock:{name}" for name in self._lookup))

    def read(self, skill_id: str) -> ExternalSkillReference:
        """Read verified source bytes. Never interpret, install or run them."""
        if not isinstance(skill_id, str) or not skill_id.startswith("mattpocock:"):
            raise LookupError("unknown external skill identifier")
        name = skill_id.removeprefix("mattpocock:")
        entry = self._lookup.get(name)
        if entry is None:
            raise LookupError("unknown external skill identifier")
        path = str(entry["source"])
        relative = path.removeprefix("vendor/mattpocock-skills/")
        expected_sha = self._hashes[relative]
        data = _file_at(self.root, path).read_bytes()
        if _git_hash(data) != expected_sha:
            raise ValueError("external skill source integrity mismatch")
        return ExternalSkillReference(
            skill_id=skill_id,
            name=name,
            category=str(entry["category"]),
            source_ref=path,
            source_commit=PINNED_SOURCE,
            git_blob_sha=expected_sha,
            source_text=data.decode("utf-8"),
            upstream_promoted=entry["upstream_promoted"] is True,
        )


__all__ = ["ExternalSkillCatalog", "ExternalSkillReference", "PINNED_SOURCE"]
