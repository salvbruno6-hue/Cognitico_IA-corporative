"""Governed evidence contract for protected instruction surfaces.

This module extends the existing ExecutionBoundary/security owners. It does not
authorize writes, create a second security authority, or perform redaction.
It classifies surfaces that require explicit authorization and/or redaction.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum

class SurfaceKind(StrEnum):
    AGENTS = "AGENTS"
    SKILL = "SKILL"
    MEMORY = "MEMORY"
    LOG = "LOG"
    CHECKPOINT = "CHECKPOINT"
    ACP = "ACP"

class SurfaceDisposition(StrEnum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    REDACT_REQUIRED = "REDACT_REQUIRED"

_PROTECTED_INSTRUCTION_KINDS = frozenset({SurfaceKind.AGENTS, SurfaceKind.SKILL, SurfaceKind.MEMORY})
_REDACTION_KINDS = frozenset({SurfaceKind.LOG, SurfaceKind.CHECKPOINT, SurfaceKind.ACP})

@dataclass(frozen=True, slots=True)
class ProtectedInstructionSurface:
    surface_id: str
    kind: SurfaceKind
    path: str
    write_requested: bool = False
    write_authorized: bool = False
    external_exposure: bool = False
    redaction_applied: bool = False

@dataclass(frozen=True, slots=True)
class SurfaceAssessment:
    surface_id: str
    disposition: SurfaceDisposition
    reason: str
    requires_existing_authorization: bool
    requires_redaction: bool

def assess_protected_surface(surface: ProtectedInstructionSurface) -> SurfaceAssessment:
    if not surface.surface_id.strip() or not surface.path.strip():
        raise ValueError("surface identity and path are required")
    requires_auth = surface.kind in _PROTECTED_INSTRUCTION_KINDS
    requires_redaction = surface.kind in _REDACTION_KINDS and surface.external_exposure
    if requires_auth and surface.write_requested and not surface.write_authorized:
        return SurfaceAssessment(surface.surface_id, SurfaceDisposition.BLOCK,
            "protected_instruction_write_requires_existing_authorization", True, requires_redaction)
    if requires_redaction and not surface.redaction_applied:
        return SurfaceAssessment(surface.surface_id, SurfaceDisposition.REDACT_REQUIRED,
            "external_exposure_requires_redaction", requires_auth, True)
    return SurfaceAssessment(surface.surface_id, SurfaceDisposition.ALLOW,
        "surface_respects_existing_governance_boundary", requires_auth, requires_redaction)
