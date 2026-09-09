"""Automatic runtime context resolution for agentic ELO queries.

This module centralizes the already-canonical Supabase ELO Forge project
reference so callers do not have to expose infrastructure identifiers in
natural-language requests. It is intentionally read-only and configuration
only; credentials remain outside source control.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


DEFAULT_ELO_FORGE_PROJECT_REF = "fxbpevjrkwhbicpmecow"
DEFAULT_ELO_FORGE_URL = f"https://{DEFAULT_ELO_FORGE_PROJECT_REF}.supabase.co"


class RuntimeContextError(RuntimeError):
    """Raised when the governed ELO runtime context cannot be resolved safely."""


@dataclass(frozen=True)
class ELORuntimeContext:
    project_ref: str
    supabase_url: str
    source_name: str = "supabase_elo_forge"
    read_only: bool = True


def resolve_runtime_context() -> ELORuntimeContext:
    """Resolve the governed ELO Forge project without requiring user input.

    An explicit environment override is accepted, but an absent override falls
    back to the canonical Forge project already declared by the repository's
    routing configuration. No alternate project is guessed.
    """
    project_ref = (
        os.getenv("ELO_FORGE_SUPABASE_PROJECT_REF")
        or os.getenv("ELO_SUPABASE_PROJECT_REF")
        or DEFAULT_ELO_FORGE_PROJECT_REF
    ).strip()
    if not project_ref:
        raise RuntimeContextError("ELO Forge project reference is not configured")

    explicit_url = (os.getenv("ELO_FORGE_SUPABASE_URL") or os.getenv("SUPABASE_URL") or "").strip()
    supabase_url = explicit_url.rstrip("/") if explicit_url else f"https://{project_ref}.supabase.co"

    expected_host = f"{project_ref}.supabase.co"
    if not supabase_url.endswith(expected_host):
        raise RuntimeContextError(
            "Supabase URL does not match the resolved ELO Forge project reference"
        )

    return ELORuntimeContext(project_ref=project_ref, supabase_url=supabase_url)
