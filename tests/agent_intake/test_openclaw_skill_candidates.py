from elo.agent_intake.openclaw_skill_candidates import (
    OPENCLAW_SKILLS_SOURCE,
    discover_skill_candidates,
)


REPOSITORY = "salvbruno6-hue/https-github.com-salvbruno6-hue-openclaw-dedicated"
REF = "codex/fix-plugin-config-diagnostics"


def test_openclaw_skill_candidates_preserve_concrete_source_provenance():
    candidates = discover_skill_candidates(
        [
            {"name": "example-skill", "path": "skills/example-skill"},
        ],
        source_repository=REPOSITORY,
        source_ref=REF,
    )

    assert len(candidates) == 1
    candidate = candidates[0]
    assert candidate.capability_id == "HERMES-SKILLS"
    assert candidate.skill_name == "example-skill"
    assert candidate.source_repository == REPOSITORY
    assert candidate.source_ref == REF
    assert candidate.source_path == "skills/example-skill"
    assert candidate.state == "CANDIDATE"
    assert candidate.promotion_state == "candidate_only"
    assert candidate.canonical_mutation is False


def test_openclaw_skill_candidates_consolidate_exact_duplicates_without_merging_distinct_skills():
    candidates = discover_skill_candidates(
        [
            {"name": "skill-a", "path": "skills/a"},
            {"name": "skill-a", "path": "skills/a"},
            {"name": "skill-a", "path": "skills/other-a"},
            {"name": "skill-b", "path": "skills/b"},
        ],
        source_repository=REPOSITORY,
        source_ref=REF,
    )

    assert [candidate.skill_name for candidate in candidates] == ["skill-a", "skill-a", "skill-b"]
    assert [candidate.source_path for candidate in candidates] == ["skills/a", "skills/other-a", "skills/b"]
    assert len({candidate.candidate_id for candidate in candidates}) == 3


def test_openclaw_skill_candidates_reject_incomplete_source_records():
    for invalid in ({"name": "", "path": "skills/a"}, {"name": "skill-a", "path": ""}):
        try:
            discover_skill_candidates(
                [invalid],
                source_repository=REPOSITORY,
                source_ref=REF,
            )
        except ValueError:
            pass
        else:
            raise AssertionError("incomplete OpenClaw skill metadata must be rejected")


def test_openclaw_skill_source_is_the_concrete_operational_skill_surface():
    assert OPENCLAW_SKILLS_SOURCE == "src/agents/skills/plugin-skills.ts"
