from elo.agent_intake.hermes_functional_value_proof import classify
from elo.agent_intake.hermes_hook_evaluation import evaluate


def test_hook_has_candidate_attributed_functional_gain():
    evaluation = evaluate()
    evidence = classify(
        "EXT-HOOK-HERMES",
        baseline=evaluation.baseline_detection_rate,
        adapted=evaluation.adapted_detection_rate,
        metric="lifecycle_guardrail_detection_rate",
        direction="maximize",
        repeatable=evaluation.repeatable,
        regressions=(),
        attribution="CANDIDATE_ATTRIBUTED",
        proof_scope="controlled lifecycle guardrail detection task",
        provenance_refs=evaluation.provenance_refs,
    )
    assert evidence.functional_gain_proven
    assert evidence.gain == 1.0
    assert evaluation.boundary_integrity


def test_owner_or_boundary_attribution_cannot_cross_functional_gate():
    evidence = classify(
        "EXT-HOOK-HERMES",
        baseline=0.0,
        adapted=1.0,
        metric="lifecycle_guardrail_detection_rate",
        direction="maximize",
        repeatable=True,
        regressions=(),
        attribution="BOUNDARY_ATTRIBUTED",
        proof_scope="contract-only",
        provenance_refs=("controlled-eval:hook/1",),
    )
    assert not evidence.functional_gain_proven
