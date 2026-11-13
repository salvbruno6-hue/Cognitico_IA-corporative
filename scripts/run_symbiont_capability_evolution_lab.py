#!/usr/bin/env python3
"""Laboratory exercise for capability evolution using a validated downstream experience.

The laboratory proves the evaluation path without requiring the evaluated skill
to own production traffic. It is not production evidence and never promotes
the capability.
"""

from __future__ import annotations

import json

from elo.cognitive.symbiont_capability_evolution import CapabilityMetric, review_capabilities
from elo.cognitive.symbionte_lab import SymbiontLabAdapter, SymbiontLabObservation
from elo.core.learning_governance import GovernedLearningService
from elo.memory.persistent import PersistentMemoryStore


def run_lab() -> dict[str, object]:
    memory = PersistentMemoryStore()
    try:
        learning = GovernedLearningService(memory)
        observation = SymbiontLabObservation(
            observation_id="lab-evolution-capability-001",
            tenant_id="tenant-lab",
            domain="capability-evolution",
            decision_id="execution-router-experience-001",
            expected_outcome="validated downstream capability supplies the observed operational context",
            observed_outcome="validated downstream capability supplied the observed operational context",
            evidence_ids=("lab-evidence:execution-router-001",),
            source_ref="experience:execution-router-001",
            source_commit="main",
            hypothesis="capability evolution can evaluate a skill through a validated downstream experience",
            baseline="0.80",
            experiment="observe a validated downstream experience in the ELO laboratory",
            result="downstream experience corroborated the evaluated capability path",
            regression_status="PASS",
            generalization_status="CONFIRMED",
            risk="LOW",
            existing_owner="ELO Model/Tool Routing",
            scope="laboratory-only capability evolution evaluation",
            tenant_scope="tenant-lab",
            source_kind="experience",
        )
        lab_result = SymbiontLabAdapter(learning).evaluate(
            observation,
            principal_id="lab",
            dataset_version="lab-2026-09-25",
        )
        if lab_result.experience is None:
            raise RuntimeError("laboratory did not produce the expected experience record")

        metric = CapabilityMetric.from_indirect_experience(
            item="Progressive Tool Schema Disclosure",
            baseline=0.80,
            current=0.88,
            direction="maximize",
            evidence_refs=lab_result.experience.evidence_ids,
            measurement_period="2026-09",
            observer_capability="ExecutionRouter",
            experience_ref=lab_result.experience.experience_id,
        )
        review = review_capabilities(metrics=(metric,))
        return {
            "mode": "LAB_ONLY",
            "lab_observation": observation.observation_id,
            "observer_capability": metric.observer_capability,
            "experience_ref": metric.experience_ref,
            "evidence_mode": metric.evidence_mode,
            "curvature": "POSITIVE" if review.ready_for_analysis else "NOT_MEASURED",
            "status": review.status,
            "canonical_mutation": review.canonical_mutation,
            "production_evidence": False,
            "promotion_authorized": False,
            "next_step": "Use governed real operational evidence only if production activation is separately authorized.",
        }
    finally:
        memory.close()


def main() -> int:
    print(json.dumps(run_lab(), ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
