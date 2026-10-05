from dataclasses import dataclass

from elo.application.use_cases.orchestrator import OrchestrationRequest
from elo.core.execution_boundary import ExecutionOutcome, ExecutionStatus
from elo.cognitive.response import orchestration_orientation_hook as hook
from elo.cognitive.response.intelligent_orchestration_response import (
    OrchestrationResponseComposer,
)


@dataclass
class Selection:
    capability_name: str = "EXT-TEST"


def _outcome():
    return ExecutionOutcome(
        request_id="request-1",
        status=ExecutionStatus.EXECUTED,
        executed=True,
        reason="authorized_execution_completed",
        provenance={"execution": "executed"},
        evidence_ids=("evidence-1",),
        correlation_id="corr-1",
    )


def _request():
    return OrchestrationRequest(
        tenant_id="tenant-a",
        principal_id="principal-1",
        domain="cognitive",
        objective="test",
        evidence_ids=("evidence-1",),
        request_id="request-1",
        correlation_id="corr-1",
    )


def test_composer_integrates_real_orientation_builder():
    result = OrchestrationResponseComposer().compose(
        request=_request(),
        selection=Selection(),
        outcome=_outcome(),
    )

    assert result.status == "EXECUTED"
    assert result.orientation is not None
    assert result.orientation.confidence.value == "insufficient"
    assert "Orientação observada" in result.response
    assert "orientação rastreável" in result.response


def test_composer_works_when_builder_is_unavailable(monkeypatch):
    monkeypatch.setattr(hook, "is_builder_available", lambda: False)

    result = OrchestrationResponseComposer().compose(
        request=_request(),
        selection=Selection(),
        outcome=_outcome(),
    )

    assert result.orientation is None
    assert "O que funcionou" in result.response


def test_composer_preserves_response_when_orientation_raises(monkeypatch):
    monkeypatch.setattr(
        hook,
        "derive_orientation",
        lambda **_: (_ for _ in ()).throw(RuntimeError("builder failure")),
    )

    result = OrchestrationResponseComposer().compose(
        request=_request(),
        selection=Selection(),
        outcome=_outcome(),
    )

    assert result.status == "EXECUTED"
    assert result.orientation is None
    assert "O que funcionou" in result.response
    assert "Orientação observada" not in result.response


def test_composer_accepts_orientation_from_hook(monkeypatch):
    @dataclass(frozen=True)
    class FakeOrientation:
        diagnosis: str = "estado observável"
        next_step: str = "reavaliar pelo fluxo canônico"

    monkeypatch.setattr(
        hook,
        "derive_orientation",
        lambda **_: FakeOrientation(),
    )

    result = OrchestrationResponseComposer().compose(
        request=_request(),
        selection=Selection(),
        outcome=_outcome(),
    )

    assert result.orientation is not None
    assert result.orientation.diagnosis == "estado observável"
    assert "estado observável" in result.response
    assert "reavaliar pelo fluxo canônico" in result.response


def test_hook_fails_soft_for_missing_capability():
    assert hook.derive_orientation(capability="") is None


def test_hook_fails_soft_when_builder_is_unavailable(monkeypatch):
    monkeypatch.setattr(hook, "_load_builder", lambda: None)
    assert hook.derive_orientation(capability="EXT-TEST") is None
