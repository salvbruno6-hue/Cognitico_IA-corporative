"""Integrity and manual-only invocation gates for the external skills snapshot.

No vendor scripts are executed by these tests.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor" / "mattpocock-skills"
AGENTS = ROOT / ".agents" / "skills"


def test_source_catalog_is_complete_and_immutably_pinned():
    manifest = json.loads((VENDOR / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["source"] == "mattpocock/skills"
    assert manifest["commit"] == "4ae2317ddb22b046e26455e4f9c9b3aaaf62212d"
    assert manifest["plugin_version"] == "1.3.2"
    assert manifest["license"] == "MIT"
    assert manifest["skills_count"] == 39
    assert manifest["source_file_count"] == 114
    assert manifest["promoted_count"] == 27
    assert (VENDOR / "LICENSE").read_text(encoding="utf-8").startswith("MIT License")

    expected = manifest["original_files"]
    actual_paths = {str(path.relative_to(VENDOR))
                    for path in (VENDOR / "skills").rglob("*") if path.is_file()}
    assert len(expected) == 114
    assert set(expected) == actual_paths
    for path, expected_sha in expected.items():
        content = (VENDOR / path).read_bytes()
        obj = b"blob " + str(len(content)).encode("ascii") + b"\0" + content
        assert hashlib.sha1(obj).hexdigest() == expected_sha, path


def test_all_39_skills_are_discoverable_but_not_implicitly_invocable():
    manifest = json.loads((VENDOR / "manifest.json").read_text(encoding="utf-8"))
    installed = manifest["installed_skills"]
    assert len(installed) == 39
    assert {s["category"] for s in installed} == {
        "engineering", "productivity", "misc", "in-progress"}
    names = [s["name"] for s in installed]
    assert len(set(names)) == 39
    discovered = {p.parent.name for p in AGENTS.glob("mattpocock-*/SKILL.md")}
    assert discovered == {f"mattpocock-{name}" for name in names}

    for skill in installed:
        wrapper = ROOT / skill["wrapper"]
        text = wrapper.read_text(encoding="utf-8")
        assert "disable-model-invocation: true" in text
        assert skill["source"] in text
        assert "Evolution Gate" in text
        assert not skill["automatic_invocation"]
        cfg = wrapper.parent / "agents" / "openai.yaml"
        assert "allow_implicit_invocation: false" in cfg.read_text(encoding="utf-8")
        assert (ROOT / skill["source"]).is_file()


def test_external_import_does_not_override_existing_supabase_skills():
    assert (AGENTS / "supabase" / "SKILL.md").exists()
    assert (AGENTS / "supabase-postgres-best-practices" / "SKILL.md").exists()
