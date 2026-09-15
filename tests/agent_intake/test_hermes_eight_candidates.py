from pathlib import Path


CANDIDATES = {
    "HERMES-MEMORY": ("ELO Cognitive Memory", "structure + function"),
    "HERMES-SKILLS": ("ELO Native Skills Registry", "Skill + structure"),
    "HERMES-TOOLSETS": ("ELO Capability/Tool Registry", "structure + function"),
    "HERMES-CONTEXT": ("ELO Context Engine", "function + structure"),
    "HERMES-DELEGATION": ("ELO Worker/Delegation Engine", "function"),
    "HERMES-AUTOMATION": ("ELO Scheduler/Watchers", "function + Skill"),
    "HERMES-MCP": ("ELO External Capability Gateway", "structure + function"),
    "HERMES-CHECKPOINT": ("ELO State Recovery Engine", "structure + function"),
}


def test_eight_native_capability_candidates_are_registered():
    assert len(CANDIDATES) == 8
    assert len(set(CANDIDATES)) == 8
    assert all(target and kind for target, kind in CANDIDATES.values())


def test_candidate_manifest_preserves_candidate_only_boundary():
    manifest = Path("docs/architecture/ELO_HERMES_8_CANDIDATES.md").read_text(
        encoding="utf-8"
    )
    for candidate_id in CANDIDATES:
        assert candidate_id in manifest
    assert "All eight are intentionally `CANDIDATE`" in manifest
    assert "READY_FOR_APPROVAL is not approval" in manifest


def test_no_candidate_is_declared_validated_or_promoted_by_registration():
    manifest = Path("docs/architecture/ELO_HERMES_8_CANDIDATES.md").read_text(
        encoding="utf-8"
    )
    assert "VALIDATED" in manifest
    assert "EVOLUTION_GATE" in manifest
    assert "no candidate is marked green" in manifest
