from elo.cognitive.learning.methodology import EvidenceKind, MethodEvidence, discover_tenant_method
from elo.cognitive.memory.evaluation import RetrievalEvaluation
from elo.cognitive.reasoning.task_planning import build_default_plan


def test_tenant_discovery_excludes_other_tenants():
    evidence = [
        MethodEvidence("budget", "estimate", "unit", "m2", EvidenceKind.OBSERVED, "a.xlsx", "a"),
        MethodEvidence("budget", "estimate", "unit", "kg", EvidenceKind.OBSERVED, "b.xlsx", "b"),
    ]
    method = discover_tenant_method(evidence, "a")
    assert method.resolve("unit") == "m2"
    assert len(method.evidence) == 1


def test_default_plan_requires_verification_before_recording():
    plan = build_default_plan("prepare an estimate")
    assert plan.steps[-2].kind.value == "verify"
    assert plan.steps[-1].depends_on == ("verify",)


def test_memory_quality_requires_isolation_and_provenance():
    evaluation = RetrievalEvaluation("q1", 10, 8, 10, 20.0, True, True)
    evaluation.validate()
    assert evaluation.precision == 0.8
    assert evaluation.recall == 0.8
    assert evaluation.admissible
