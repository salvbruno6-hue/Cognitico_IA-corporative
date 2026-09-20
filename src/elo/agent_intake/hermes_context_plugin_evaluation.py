from __future__ import annotations
from dataclasses import dataclass
from elo.agent_intake.hermes_context_plugin_boundary import ContextEnginePluginSignal, PluginDisposition, assess_context_engine_plugin
from elo.core.context_resolution import ContextQuery, ContextResolutionEngine

@dataclass(frozen=True)
class ContextPluginEvaluation:
    candidate_id: str
    baseline_success_rate: float
    adapted_success_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _task_success(engine: ContextResolutionEngine) -> bool:
    pack = engine.resolve(ContextQuery(question="Qual e o contexto autorizado para esta solicitacao?", tenant_id="multiteiner", domain="planning"))
    return bool(pack.discovery_plan is not None and pack.query.tenant_id == "multiteiner")

def evaluate_context_plugin_candidate() -> ContextPluginEvaluation:
    engine = ContextResolutionEngine()
    baseline_runs = tuple(_task_success(engine) for _ in range(5))
    signals = tuple(ContextEnginePluginSignal(signal_id=f"ctx-{i}", tenant_scope="multiteiner", plugin_id="lcm", engine_name="lcm", source_refs=("hermes:plugin:lcm",), explicit_activation=True, provenance_verified=True) for i in range(5))
    assessments = tuple(assess_context_engine_plugin(signal) for signal in signals)
    adapted_runs = tuple(assessment.disposition is PluginDisposition.CANDIDATE and _task_success(engine) for assessment in assessments)
    invalid = ContextEnginePluginSignal(signal_id="ctx-invalid", tenant_scope="multiteiner", plugin_id="lcm", engine_name="lcm", source_refs=("hermes:plugin:lcm",), explicit_activation=True, provenance_verified=False)
    invalid_assessment = assess_context_engine_plugin(invalid)
    baseline_rate = sum(baseline_runs) / len(baseline_runs)
    adapted_rate = sum(adapted_runs) / len(adapted_runs)
    boundary_rate = float(invalid_assessment.disposition is PluginDisposition.REJECTED)
    result = "RETEST" if adapted_rate <= baseline_rate else "EVOLUTION_GATE_REQUIRED"
    return ContextPluginEvaluation("EXT-CONTEXT-PLUGIN-HERMES", baseline_rate, adapted_rate, boundary_rate, baseline_runs == tuple(True for _ in baseline_runs) and adapted_runs == tuple(True for _ in adapted_runs), result)
