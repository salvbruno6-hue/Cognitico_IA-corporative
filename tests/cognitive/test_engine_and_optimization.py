from elo.cognitive.context import CognitiveContext, ContextItem
from elo.cognitive.engine import CognitiveEngine
from elo.cognitive.optimization import CognitiveOptimizer, EvaluationRecord


def test_engine_routes_high_risk_to_deliberative_search_and_requires_verification():
    context = CognitiveContext(task="avaliar uma decisão crítica")
    plan = CognitiveEngine().plan(context, complexity=0.9, risk=0.9, uncertainty=0.8)
    assert plan.capability == "deliberative_search"
    assert plan.reasoning_depth == 3
    assert plan.verification_required is True


def test_engine_verification_uses_context_evidence():
    context = CognitiveContext(
        task="responder",
        evidence=(ContextItem("fact", "valid", "source-a", confidence=0.95),),
    )
    result = CognitiveEngine().verify("answer", context, required_confidence=0.9)
    assert result.accepted is True


def test_optimizer_only_proposes_when_gain_and_latency_gate_pass():
    optimizer = CognitiveOptimizer()
    proposal = optimizer.propose(
        EvaluationRecord("reasoning", 0.70, 100, 10),
        EvaluationRecord("reasoning", 0.75, 95, 12),
    )
    assert proposal.promotion_eligible is True
    assert proposal.score_delta == 0.05


def test_optimizer_rejects_latency_regression_without_gain():
    proposal = CognitiveOptimizer().propose(
        EvaluationRecord("reasoning", 0.80, 100, 10),
        EvaluationRecord("reasoning", 0.805, 130, 10),
    )
    assert proposal.promotion_eligible is False
