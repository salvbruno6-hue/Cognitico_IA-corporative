from elo.security.protected_instruction_surfaces import (
    ProtectedInstructionSurface, SurfaceDisposition, SurfaceKind, assess_protected_surface,
)

def test_protected_instruction_write_requires_existing_authorization():
    result = assess_protected_surface(ProtectedInstructionSurface("AGENTS-1", SurfaceKind.AGENTS, "AGENTS.md", True, False))
    assert result.disposition == SurfaceDisposition.BLOCK
    assert result.requires_existing_authorization is True

def test_authorized_protected_instruction_write_is_not_a_new_authority():
    result = assess_protected_surface(ProtectedInstructionSurface("SKILL-1", SurfaceKind.SKILL, "skills/example/SKILL.md", True, True))
    assert result.disposition == SurfaceDisposition.ALLOW

def test_external_checkpoint_exposure_requires_redaction():
    result = assess_protected_surface(ProtectedInstructionSurface("CHECKPOINT-1", SurfaceKind.CHECKPOINT, "checkpoint.json", False, False, True, False))
    assert result.disposition == SurfaceDisposition.REDACT_REQUIRED
    assert result.requires_redaction is True

def test_redacted_acp_exposure_is_allowed():
    result = assess_protected_surface(ProtectedInstructionSurface("ACP-1", SurfaceKind.ACP, "acp-event", False, False, True, True))
    assert result.disposition == SurfaceDisposition.ALLOW

def test_memory_read_without_write_does_not_require_write_authorization():
    result = assess_protected_surface(ProtectedInstructionSurface("MEMORY-1", SurfaceKind.MEMORY, "memory"))
    assert result.disposition == SurfaceDisposition.ALLOW
    assert result.requires_existing_authorization is True

def test_missing_surface_identity_is_rejected():
    try:
        assess_protected_surface(ProtectedInstructionSurface("", SurfaceKind.AGENTS, "AGENTS.md"))
    except ValueError as exc:
        assert "identity" in str(exc)
    else:
        raise AssertionError("invalid surface identity must be rejected")
