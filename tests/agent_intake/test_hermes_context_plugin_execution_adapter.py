from elo.agent_intake.hermes_context_plugin_boundary import ContextEnginePluginSignal
from elo.agent_intake.hermes_context_plugin_execution_adapter import execute_context_plugin
from elo.core.execution_boundary import ExecutionRequest, ExecutionStatus

def _signal(**overrides):
    data = dict(
        signal_id="ctx-exec-001", tenant_scope="multiteiner", plugin_id="lcm",
        engine_name="lcm", source_refs=("hermes:plugin:lcm",),
        explicit_activation=True, provenance_verified=True,
    )
    data.update(overrides)
    return ContextEnginePluginSignal(**data)

def _request(**overrides):
    data = dict(
        request_id="exec-ctx-001", tenant_id="multiteiner",
        principal_id="principal-001", action_id="EXT-CONTEXT-PLUGIN-HERMES",
        authorization_id="auth-001", evidence_ids=("evidence-ctx-001",),
        correlation_id="corr-ctx-001",
        decision_pattern_candidate_ref="EXT-CONTEXT-PLUGIN-HERMES",
    )
    data.update(overrides)
    return ExecutionRequest(**data)

def test_context_plugin_execution_crosses_canonical_boundary():
    result = execute_context_plugin(
        _request(), signal=_signal(),
        question="Qual e o contexto autorizado para esta solicitacao?",
    )
    assert result.outcome.status is ExecutionStatus.EXECUTED
    assert result.outcome.executed is True
    assert result.outcome.request_id == "exec-ctx-001"
    assert result.outcome.authorization_id == "auth-001"
    assert result.outcome.correlation_id == "corr-ctx-001"
    assert result.outcome.decision_pattern_candidate_ref == "EXT-CONTEXT-PLUGIN-HERMES"
    assert result.adapted is True
    assert result.canonical_authority is False

def test_context_plugin_execution_fails_closed_without_governance_controls():
    result = execute_context_plugin(
        _request(authorization_id=None), signal=_signal(),
        question="Qual e o contexto autorizado para esta solicitacao?",
    )
    assert result.outcome.status is ExecutionStatus.BLOCKED
    assert result.outcome.executed is False
    assert result.outcome.provenance["execution"] == "not_attempted"

def test_context_plugin_execution_rejects_unverified_signal():
    result = execute_context_plugin(
        _request(), signal=_signal(provenance_verified=False),
        question="Qual e o contexto autorizado para esta solicitacao?",
    )
    assert result.outcome.status is ExecutionStatus.FAILED
    assert result.outcome.executed is False
    assert result.outcome.reason == "authorized_execution_failed:ValueError"
