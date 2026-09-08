from __future__ import annotations

import pytest

from elo.cognitive.agents.hermes_skill_runtime import (
    IntentSpec,
    build_skill_execution_envelope,
    validate_skill_candidate,
)


def test_intent_spec_builds_governed_hermes_envelope_without_infrastructure():
    intent = IntentSpec(
        request_id="req-001",
        intent="create skill for governed procurement workflow",
        tenant_scope="multiteiner",
        mission_class="operational",
        authorized_capabilities=("skill:read", "skill:create"),
        skill_name="procurement-workflow",
        context={"domain": "commercial"},
    )

    envelope = build_skill_execution_envelope(intent)

    assert envelope["governance"]["authority"] == "elo_cognitive"
    assert envelope["governance"]["execution_runtime"] == "hermes"
    assert envelope["governance"]["learning_boundary"] == "candidate_only"
    assert "project_id" not in envelope
    assert "project_ref" not in envelope


def test_intent_spec_rejects_infrastructure_in_context():
    with pytest.raises(ValueError):
        IntentSpec(
            request_id="req-002",
            intent="execute",
            tenant_scope="multiteiner",
            mission_class="operational",
            authorized_capabilities=("skill:read",),
            context={"project_ref": "must-not-cross"},
        )


def test_skill_candidate_remains_noncanonical():
    validate_skill_candidate({"status": "candidate_only", "observation": "reusable workflow"})


def test_skill_candidate_rejects_canonical_fields():
    with pytest.raises(ValueError):
        validate_skill_candidate(
            {"status": "pending", "canonical_knowledge": {"claim": "forbidden"}}
        )
