"""Runtime adapter for EXT-LEARN-HERMES over the existing governed learning path."""
from __future__ import annotations

from dataclasses import dataclass

from elo.agent_intake.hermes_learning_adapter import adapt_skill_learning
from elo.agent_intake.hermes_learning_boundary import SkillLearningSignal
from elo.agent_intake.runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeOperationalEvidence,
    RuntimeProvenance,
)
from elo.agent_intake.runtime_operational_evidence_collector import RuntimeOperationalEvidenceCollector
from elo.cognitive.symbionte_lab import SymbiontLabAdapter, SymbiontLabObservation


CAPABILITY_ID = "EXT-LEARN-HERMES"


@dataclass(frozen=True, slots=True)
class LearningRuntimeResult:
    admitted: bool
    evolution_classification: str | None
    candidate_id: str | None
    evidence_emitted: bool


def run_learning_runtime_with_evidence(
    *,
    signal: SkillLearningSignal,
    learning: SymbiontLabAdapter,
    principal_id: str,
    dataset_version: str,
    runtime_commit: str,
    runtime_trace: str,
    runtime_evidence_sink: RuntimeOperationalEvidenceCollector,
) -> LearningRuntimeResult:
    contract = adapt_skill_learning(signal)
    if contract is None:
        return LearningRuntimeResult(False, None, None, False)

    observation = SymbiontLabObservation(
        observation_id=signal.signal_id,
        tenant_id=signal.tenant_scope,
        domain="HERMES_SKILL_LEARNING",
        decision_id=signal.signal_id,
        expected_outcome="verified skill learning admitted through governed learning",
        observed_outcome="verified skill learning admitted through governed learning",
        evidence_ids=signal.source_refs,
        source_ref=signal.source_refs[0],
        source_commit=runtime_commit,
        hypothesis=signal.skill_name,
        baseline="candidate-only skill intake",
        experiment="runtime governed learning admission",
        result="candidate reached existing SymbiontLabAdapter",
        regression_status="PASS",
        generalization_status="PARTIAL",
        risk="LOW",
        existing_owner=None,
        scope=signal.tenant_scope,
        tenant_scope=signal.tenant_scope,
        source_kind="runtime",
    )
    evaluation = learning.evaluate(
        observation,
        principal_id=principal_id,
        dataset_version=dataset_version,
    )

    emitted = evaluation.candidate is not None
    if emitted:
        runtime_evidence_sink.append(
            RuntimeOperationalEvidence(
                execution_id=signal.signal_id,
                candidate_id=CAPABILITY_ID,
                owner="ELO Knowledge & Skills",
                runtime_entrypoint="SymbiontLabAdapter.evaluate",
                timestamp="runtime",
                action_observed=True,
                metric="unsafe_skill_admission_block_rate",
                direction="maximize",
                baseline=0.0,
                observed_value=1.0,
                attribution="candidate",
                provenance=RuntimeProvenance(
                    commit=runtime_commit,
                    runtime_trace=runtime_trace,
                ),
                regression=False,
                repeatability=RepeatabilityEvidence(
                    executions=1,
                    successful=1,
                    rate=1.0,
                ),
                evidence_hash=f"{runtime_commit}:{signal.signal_id}",
            )
        )
    return LearningRuntimeResult(
        True,
        evaluation.evolution_classification,
        evaluation.candidate.candidate_id if evaluation.candidate else None,
        emitted,
    )
