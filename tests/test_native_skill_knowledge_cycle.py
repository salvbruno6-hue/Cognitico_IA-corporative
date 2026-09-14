import pytest

from elo.cognitive.knowledge_capture import KnowledgeCaptureError, KnowledgeCaptureResult, NativeKnowledgeCapture
from elo.forge.skill_authoring import NativeSkillAuthoring, SkillAuthoringError, SkillCandidate


def provenance():
    return {"source_ref": "external-observation", "source_commit": "abc123"}


def test_skill_authoring_accepts_governed_candidate():
    candidate = NativeSkillAuthoring().prepare(
        skill_id="evidence-review",
        description="Review evidence and prepare a governed candidate.",
        version="0.1.0",
        platforms=["linux", "linux", "macos"],
        body="# Evidence Review\n\n## Verification\nEvery input is accounted for.",
        provenance=provenance(),
    )
    assert isinstance(candidate, SkillCandidate)
    assert candidate.platforms == ("linux", "macos")
    assert candidate.state == "CANDIDATE"


def test_skill_authoring_rejects_duplicate_and_bad_metadata():
    with pytest.raises(SkillAuthoringError):
        NativeSkillAuthoring().prepare(
            skill_id="existing-skill",
            description="Valid enough description.",
            version="0.1.0",
            platforms=["linux"],
            body="body",
            provenance=provenance(),
            existing_skill_ids=("existing-skill",),
        )
    with pytest.raises(SkillAuthoringError):
        NativeSkillAuthoring().prepare(
            skill_id="new-skill",
            description="A description that is intentionally much longer than the governed sixty character boundary and must fail.",
            version="0.1.0",
            platforms=["linux"],
            body="body",
            provenance=provenance(),
        )


def test_knowledge_capture_accepts_evidence_bearing_observation():
    result = NativeKnowledgeCapture().capture(
        observation_id="obs-1",
        tenant_id="tenant-a",
        domain="procurement",
        title="Bid review",
        concept="Compare normalized unit prices",
        evidence_ids=["ev-1"],
        provenance=provenance(),
        confidence="HIGH",
    )
    assert result.state == "OBSERVATION"
    assert len(result.fingerprint) == 64


def test_knowledge_capture_detects_duplicate_and_conflict():
    capture = NativeKnowledgeCapture()
    fp = capture.fingerprint(domain="procurement", title="Bid review", concept="Compare prices")
    duplicate = capture.capture(
        observation_id="obs-2", tenant_id="tenant-a", domain="procurement",
        title="Bid review", concept="Compare prices", evidence_ids=["ev-2"],
        provenance=provenance(), existing_fingerprints=(fp,),
    )
    assert isinstance(duplicate, KnowledgeCaptureResult)
    assert duplicate.status == "DUPLICATE"

    conflict = capture.capture(
        observation_id="obs-3", tenant_id="tenant-a", domain="procurement",
        title="Different framing", concept="Compare prices", evidence_ids=["ev-3"],
        provenance=provenance(), existing_concepts=("Compare prices",),
    )
    assert isinstance(conflict, KnowledgeCaptureResult)
    assert conflict.status == "CONFLICT_REVIEW"


def test_knowledge_capture_rejects_secrets_and_missing_evidence():
    with pytest.raises(KnowledgeCaptureError):
        NativeKnowledgeCapture().capture(
            observation_id="obs-4", tenant_id="tenant-a", domain="x",
            title="t", concept="c", evidence_ids=["ev"],
            provenance={"source_ref": "x", "source_commit": "y", "api_key": "forbidden"},
        )
    with pytest.raises(KnowledgeCaptureError):
        NativeKnowledgeCapture().capture(
            observation_id="obs-5", tenant_id="tenant-a", domain="x",
            title="t", concept="c", evidence_ids=[], provenance=provenance(),
        )
