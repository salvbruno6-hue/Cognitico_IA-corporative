"""Controlled functional evaluation for EXT-CONTEXT-PLUGIN-HERMES."""
from __future__ import annotations

from dataclasses import dataclass

from elo.agent_intake.hermes_context_plugin_adapter import ContextPluginAdapter
from elo.agent_intake.hermes_context_plugin_boundary import (
    ContextEnginePluginSignal,
    PluginDisposition,
    assess_context_engine_plugin,
)
from elo.core.context_resolution import ContextQuery, ContextResolutionEngine


@dataclass(frozen=True)
class ContextPluginEvaluation:
    candidate_id: str
    baseline_success_rate: float
    adapted_success_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str


def _query(engine: ContextResolutionEngine):
    return engine.resolve(
        ContextQuery(
            question="Qual e o contexto autorizado para esta solicitacao?",
            tenant_id="multiteiner",
            domain="planning",
        )
    )


def _task_success(pack) -> bool:
    scoped = pack.scoped_sources()
    return bool(
        pack.discovery_plan is not None
        and pack.query.tenant_id == "multiteiner"
        and any(
            source.source_type == "context-plugin"
            and source.authority == "ELO Context"
            for source in scoped
        )
    )


def evaluate_context_plugin_candidate() -> ContextPluginEvaluation:
    baseline_engine = ContextResolutionEngine()
    baseline_runs = tuple(
        _task_success(_query(baseline_engine)) for _ in range(5)
    )

    adapted_engine = ContextResolutionEngine()
    adapter = ContextPluginAdapter(adapted_engine)
    adapted_runs = []
    assessments = []

    for i in range(5):
        signal = ContextEnginePluginSignal(
            signal_id=f"ctx-{i}",
            tenant_scope="multiteiner",
            plugin_id="lcm",
            engine_name="lcm",
            source_refs=("hermes:plugin:lcm",),
            explicit_activation=True,
            provenance_verified=True,
        )
        result = adapter.adapt(_query(adapted_engine), signal)
        assessments.append(result.assessment)
        adapted_runs.append(
            result.adapted
            and result.assessment.disposition is PluginDisposition.CANDIDATE
            and _task_success(result.pack)
        )

    invalid = ContextEnginePluginSignal(
        signal_id="ctx-invalid",
        tenant_scope="multiteiner",
        plugin_id="lcm",
        engine_name="lcm",
        source_refs=("hermes:plugin:lcm",),
        explicit_activation=True,
        provenance_verified=False,
    )
    invalid_assessment = assess_context_engine_plugin(invalid)

    baseline_rate = sum(baseline_runs) / len(baseline_runs)
    adapted_rate = sum(adapted_runs) / len(adapted_runs)
    boundary_rate = float(
        invalid_assessment.disposition is PluginDisposition.REJECTED
        and all(not assessment.canonical_authority for assessment in assessments)
    )
    repeatable = (
        all(assessment.disposition is PluginDisposition.CANDIDATE for assessment in assessments)
        and all(baseline_runs)
        is False
        and all(adapted_runs)
    )
    result = "EVOLUTION_GATE_REQUIRED" if adapted_rate > baseline_rate and repeatable else "RETEST"

    return ContextPluginEvaluation(
        "EXT-CONTEXT-PLUGIN-HERMES",
        baseline_rate,
        adapted_rate,
        boundary_rate,
        repeatable,
        result,
    )
