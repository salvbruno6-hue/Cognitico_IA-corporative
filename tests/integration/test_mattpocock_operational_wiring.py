"""Operational, bounded evidence for Orchestrator -> external skills -> Symbiont.

All 39 skills are invoked by a controlled local adapter; none runs vendor code.
This does not claim external provider or production runtime execution.
"""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json

import pytest

from elo.agent_intake.mattpocock_catalog import ExternalSkillCatalog, PINNED_SOURCE
from elo.application.use_cases.orchestrator import (
    AuthorizationDecision, GovernedOrchestrator, OrchestrationRequest,
)
from elo.core.execution_boundary import ExecutionStatus

ROOT = Path(__file__).resolve().parents[2]


def _request(skill_id: str, **changes):
    fields = dict(
        tenant_id="tenant-mt",
        principal_id="operator-1",
        domain="engineering",
        objective="evaluate this bounded test scenario",
        request_id="request-001",
        correlation_id="correlation-001",
        evidence_ids=("test:authorized-scenario",),
        authorization=AuthorizationDecision(
            authorized=True,
            authority="elo-authz",
            identity_id="operator-1",
            role="CANONICAL_ADMIN",
            evidence_ref="elo-authz:evidence-001",
            session_id="session-001",
            binding_id="binding-001",
            grant_id="grant-001",
            operation="execute",
            resource_id=skill_id,
            expires_at=(datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
        ),
    )
    fields.update(changes)
    return OrchestrationRequest(**fields)


def test_all_39_skills_reach_canonical_execution_boundary_and_symbiont_lab():
    catalog = ExternalSkillCatalog(ROOT)
    orchestrator = GovernedOrchestrator()
    called = []

    def controlled_executor(reference, execution_request):
        assert reference.manual_only is True
        assert reference.source_commit == PINNED_SOURCE
        assert reference.source_text.startswith("---")
        assert execution_request.action_id == reference.skill_id
        assert execution_request.authorization_id == "grant-001"
        called.append(reference.skill_id)
        return {"runtime_evidence_ref": "test:controlled-adapter:" + reference.name}

    assert len(catalog.skill_ids) == 39
    for skill_id in catalog.skill_ids:
        result = orchestrator.invoke_external_skill(
            _request(skill_id),
            skill_id=skill_id,
            catalog=catalog,
            approved_skill_ids=frozenset({skill_id}),
            executor=controlled_executor,
        )
        assert result.outcome.status is ExecutionStatus.EXECUTED
        assert result.outcome.executed
        assert result.outcome.provenance["runtime_evidence_ref"].startswith("test:controlled-adapter:")
        assert result.symbiont_decision is not None
        assert result.symbiont_decision.disposition == "REUSE"
        assert not result.symbiont_decision.candidate_creation_allowed
        assert result.symbiont_decision.pattern.source_commit == PINNED_SOURCE
        assert result.symbiont_decision.pattern.tenant_id == "tenant-mt"
    assert set(called) == set(catalog.skill_ids)


@pytest.mark.parametrize("reason", [
    "no_allowlist", "no_authorization", "noncanonical", "wrong_resource",
    "wrong_principal", "missing_evidence", "missing_correlation", "expired",
])
def test_unauthorized_or_incomplete_external_skill_never_invokes_executor(reason):
    skill_id = "mattpocock:tdd"
    request = _request(skill_id)
    approved = frozenset({skill_id})
    if reason == "no_allowlist":
        approved = frozenset()
    elif reason == "no_authorization":
        request = _request(skill_id, authorization=None)
    elif reason == "noncanonical":
        request = _request(skill_id, authorization=AuthorizationDecision(
            authorized=True, authority="caller", identity_id="operator-1",
            role="CANONICAL_ADMIN", evidence_ref="not-elo-authz",
            session_id="session-001", binding_id="binding-001",
            grant_id="grant-001", resource_id=skill_id,
            expires_at=(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat(),
        ))
    elif reason == "wrong_resource":
        request = _request(skill_id, authorization=_request("mattpocock:retro").authorization)
    elif reason == "wrong_principal":
        request = _request(skill_id, principal_id="another-principal")
    elif reason == "missing_evidence":
        request = _request(skill_id, evidence_ids=())
    elif reason == "missing_correlation":
        request = _request(skill_id, correlation_id="")
    elif reason == "expired":
        auth = _request(skill_id).authorization
        request = _request(skill_id, authorization=AuthorizationDecision(
            **{**vars(auth), "expires_at": "2020-01-01T00:00:00+00:00"}
        ))
    calls = []
    result = GovernedOrchestrator().invoke_external_skill(
        request, skill_id=skill_id, catalog=ExternalSkillCatalog(ROOT),
        approved_skill_ids=approved, executor=lambda *_: calls.append("called"),
    )
    assert result.outcome.status is ExecutionStatus.BLOCKED
    assert result.symbiont_decision is None
    assert calls == []


def test_unknown_source_and_tampered_content_fail_closed(tmp_path):
    catalog = ExternalSkillCatalog(ROOT)
    with pytest.raises(LookupError):
        catalog.read("mattpocock:missing")
    with pytest.raises(LookupError):
        catalog.read("../../etc/passwd")
    # Only copy an immutable miniature tree, never run vendor scripts.
    import shutil
    shutil.copytree(ROOT / "vendor" / "mattpocock-skills", tmp_path / "vendor" / "mattpocock-skills")
    shutil.copytree(ROOT / ".agents" / "skills", tmp_path / ".agents" / "skills")
    modified = tmp_path / "vendor/mattpocock-skills/skills/engineering/tdd/SKILL.md"
    modified.write_text(modified.read_text() + "\nunauthorized mutation\n")
    with pytest.raises(ValueError, match="integrity"):
        ExternalSkillCatalog(tmp_path).read("mattpocock:tdd")


def test_executor_must_return_runtime_evidence_before_symbiont_observes():
    skill_id = "mattpocock:code-review"
    result = GovernedOrchestrator().invoke_external_skill(
        _request(skill_id), skill_id=skill_id, catalog=ExternalSkillCatalog(ROOT),
        approved_skill_ids=frozenset({skill_id}),
        executor=lambda *_: {},
    )
    assert result.outcome.status is ExecutionStatus.FAILED
    assert result.symbiont_decision is None
    assert not result.outcome.executed
