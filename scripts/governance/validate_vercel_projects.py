#!/usr/bin/env python3
"""Validate repository-side invariants for applications deployed to Vercel.

This does not pretend to inspect Vercel's remote project settings. It validates
what can be enforced from GitHub and emits explicit remediation for settings
that must match in the Vercel project.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP = {"node_modules", ".next", ".git", "dist", "build"}
FORBIDDEN_FLOATING = {"latest", "next", "canary", "*"}


def iter_package_files():
    for path in ROOT.rglob("package.json"):
        if any(part in SKIP for part in path.parts):
            continue
        yield path


def version_is_floating(value: object) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.strip().lower()
    return normalized in FORBIDDEN_FLOATING or normalized.startswith("latest@")} 


def main() -> int:
    errors: list[str] = []
    apps: list[tuple[Path, dict]] = []

    for path in iter_package_files():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue

        deps = {}
        deps.update(data.get("dependencies") or {})
        deps.update(data.get("devDependencies") or {})
        if "next" in deps:
            apps.append((path, data))

    if not apps:
        print("Vercel governance: no Next.js application detected.")
        return 0

    for package_path, data in apps:
        rel = package_path.relative_to(ROOT)
        print(f"Checking Next.js app: {rel.parent}")
        deps = data.get("dependencies") or {}
        dev = data.get("devDependencies") or {}
        all_deps = {**deps, **dev}

        if version_is_floating(all_deps.get("next")):
            errors.append(f"{rel}: Next.js version must not be floating: {all_deps.get('next')!r}")

        for name in ("typescript", "eslint", "@types/node", "@types/react", "@types/react-dom"):
            if name in all_deps and version_is_floating(all_deps[name]):
                errors.append(f"{rel}: {name} must not use a floating version: {all_deps[name]!r}")

        scripts = data.get("scripts") or {}
        if "build" not in scripts:
            errors.append(f"{rel}: missing scripts.build")

        engines = data.get("engines") or {}
        node = str(engines.get("node", "")).strip()
        if not node:
            errors.append(f"{rel}: engines.node must be declared for deterministic Vercel builds")
        elif not re.search(r"20|21|22|23|24", node):
            errors.append(f"{rel}: unsupported/unclear Node engine declaration: {node!r}")

        # A Vercel project must use the directory containing this package.json
        # as its Root Directory (or an explicitly documented parent contract).
        print(f"  expected Vercel Root Directory: {rel.parent}")
        print("  expected framework: Next.js")
        print(f"  declared build command: {scripts.get('build')}")
        print(f"  declared Node engine: {node or '<missing>'}")

    if errors:
        print("\nVercel governance FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("\nVercel governance PASS: repository-side deployment invariants are deterministic.")
    print("Remote Vercel settings still require project-level audit: Root Directory, Node.js, build/install commands and deployment status.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
