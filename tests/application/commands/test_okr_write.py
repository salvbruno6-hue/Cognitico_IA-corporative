from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from elo.application.commands.okr_write import (
    GovernedOkrWriter,
    SnapshotBindingWrite,
    StrategicWriteAction,
    StrategicWriteGrant,
    binding_resource_ref,
    key_result_resource_ref,
    objective_resource_ref,
)
from elo.contracts.okr import KeyResult, KeyResultDirection, Objective, TargetApprovalState


class RecordingRepository:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object, str]] = []

    def upsert_objective(self, objective, *, authorization_ref: str) -> None:
        self.calls.append(("objective", objective, authorization_ref))

    def upsert_key_result(self, key_result, *, authorization_ref: str) -> None:
        self.calls.append(("key_result", key_result, authorization_ref))

    def bind_snapshot(self, binding, *, authorization_ref: str) -> None:
        self.calls.append(("binding", binding, authorization_ref))


def _grant(action: StrategicWriteAction, **overrides) -> StrategicWriteGrant:
    values = dict(
        authorized=True,
        authority="elo-authz",
        action=action,
        capability_code={
            StrategicWriteAction.PROPOSE: "PROPOSE",
            StrategicWriteAction.REVIEW: "REVIEW",
            StrategicWriteAction.APPROVE: "APPROVE",
            StrategicWriteAction.CANONICAL_WRITE: "CANONICAL_WRITE",
        }[action],
        tenant_id="tenant-a",
        resource_ref=objective_resource_ref("obj-1"),
        identity_id="identity-a",
        evidence_ref="elo-authz:req-1",
        grant_ref="grant-1",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
    )
    values.update(overrides)
    return StrategicWriteGrant(**values)


def _objective() -> Objective:
    return Objective(
        tenant_id="tenant-a",
        objective_id="obj-1",
        title="Aumentar previsibilidade operacional",
        evidence_refs=("ev-objective",),
    )


def _kr(*, state: TargetApprovalState = TargetApprovalState.DRAFT) -> KeyResult:
    return KeyResult(
        tenant_id="tenant-a",
        key_result_id="kr-1",
        objective_id="obj-1",
        title="Elevar aderência",
        metric_code="KPI_ADERENCIA",
        direction=KeyResultDirection.INCREASE,
        baseline=Decimal("50"),
        target=Decimal("80"),
        baseline_evidence_refs=("ev-baseline",),
        target_evidence_refs=("ev-target",),
        target_approval_state=state,
        target_approval_ref="approval-1" if state is TargetApprovalState.APPROVED else None,
    )


def test_proposal_requires_canonical_elo_authz_grant() -> None:
    repo = RecordingRepository()
    writer = GovernedOkrWriter(repo)

    with pytest.raises(PermissionError):
        writer.propose_objective(_objective(), _grant(StrategicWriteAction.PROPOSE, authority="local"))

    assert repo.calls == []


def test_proposal_rejects_cross_tenant_grant() -> None:
    repo = RecordingRepository()
    writer = GovernedOkrWriter(repo)

    with pytest.raises(PermissionError):
        writer.propose_objective(_objective(), _grant(StrategicWriteAction.PROPOSE, tenant_id="tenant-b"))

    assert repo.calls == []


def test_proposal_rejects_grant_for_different_resource() -> None:
    repo = RecordingRepository()
    writer = GovernedOkrWriter(repo)

    with pytest.raises(PermissionError):
        writer.propose_objective(
            _objective(),
            _grant(StrategicWriteAction.PROPOSE, resource_ref=objective_resource_ref("obj-2")),
        )

    assert repo.calls == []


def test_expired_grant_cannot_write() -> None:
    repo = RecordingRepository()
    writer = GovernedOkrWriter(repo)

    with pytest.raises(PermissionError):
        writer.propose_objective(
            _objective(),
            _grant(
                StrategicWriteAction.PROPOSE,
                expires_at=datetime.now(timezone.utc) - timedelta(seconds=1),
            ),
        )

    assert repo.calls == []


def test_capability_must_match_action() -> None:
    repo = RecordingRepository()
    writer = GovernedOkrWriter(repo)

    with pytest.raises(PermissionError):
        writer.propose_objective(
            _objective(),
            _grant(StrategicWriteAction.PROPOSE, capability_code="CANONICAL_WRITE"),
        )

    assert repo.calls == []


def test_draft_key_result_can_be_proposed_but_not_approved() -> None:
    repo = RecordingRepository()
    writer = GovernedOkrWriter(repo)
    draft = _kr()
    kr_resource = key_result_resource_ref(draft.key_result_id)

    writer.propose_key_result(
        draft,
        _grant(StrategicWriteAction.PROPOSE, resource_ref=kr_resource),
    )
    with pytest.raises(ValueError, match="APPROVED"):
        writer.approve_key_result(
            draft,
            _grant(StrategicWriteAction.APPROVE, resource_ref=kr_resource),
        )

    assert repo.calls[0][0] == "key_result"


def test_approved_key_result_requires_approve_action() -> None:
    repo = RecordingRepository()
    writer = GovernedOkrWriter(repo)
    approved = _kr(state=TargetApprovalState.APPROVED)
    kr_resource = key_result_resource_ref(approved.key_result_id)

    with pytest.raises(ValueError, match="proposal"):
        writer.propose_key_result(
            approved,
            _grant(StrategicWriteAction.PROPOSE, resource_ref=kr_resource),
        )

    writer.approve_key_result(
        approved,
        _grant(StrategicWriteAction.APPROVE, resource_ref=kr_resource),
    )
    assert repo.calls == [("key_result", approved, "elo-authz:req-1")]


def test_snapshot_binding_requires_review_grant_and_evidence() -> None:
    repo = RecordingRepository()
    writer = GovernedOkrWriter(repo)
    binding = SnapshotBindingWrite(
        tenant_id="tenant-a",
        key_result_id="kr-1",
        snapshot_id="11111111-1111-1111-1111-111111111111",
        evidence_refs=("ev-binding",),
    )
    resource = binding_resource_ref(binding.key_result_id, binding.snapshot_id)

    with pytest.raises(PermissionError):
        writer.bind_measurement_snapshot(
            binding,
            _grant(StrategicWriteAction.PROPOSE, resource_ref=resource),
        )

    writer.bind_measurement_snapshot(
        binding,
        _grant(StrategicWriteAction.REVIEW, resource_ref=resource),
    )
    assert repo.calls == [("binding", binding, "elo-authz:req-1")]


def test_snapshot_binding_without_evidence_is_rejected_at_contract_boundary() -> None:
    with pytest.raises(ValueError, match="evidence_refs"):
        SnapshotBindingWrite(
            tenant_id="tenant-a",
            key_result_id="kr-1",
            snapshot_id="11111111-1111-1111-1111-111111111111",
            evidence_refs=(),
        )
