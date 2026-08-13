from datetime import datetime, timezone

from elo.core.causal_reasoning import CausalAssessment
from elo.core.decision_memory import DecisionRecord
from elo.core.directory_intelligence import DirectoryAssessment, DirectorySemanticProfile
from elo.core.outcome_feedback import OutcomeFeedback
from elo.core.scenario_engine import Scenario, ScenarioAssumption, ScenarioOutcome
from elo.core.systemic_model import SystemicModel, SystemicNode, SystemicRelation
from elo.core.temporal_knowledge import TemporalValidity
from elo.core.uncertainty import UncertaintyAssessment


def test_systemic_model_returns_related_relations():
    model = SystemicModel(
        nodes=(SystemicNode("pedido", "process", "Pedido"), SystemicNode("estoque", "process", "Estoque")),
        relations=(SystemicRelation("pedido", "depends_on", "estoque", 0.9, ("ev-1",)),),
    )
    assert model.related_to("pedido")[0].target_id == "estoque"


def test_causal_assessment_validates_confidence():
    assessment = CausalAssessment("compra", "estoque", "PROBABLE_CAUSE", 0.8, ("ev-1",))
    assert assessment.is_confirmed is False


def test_scenario_adds_outcome_immutably():
    scenario = Scenario("s-1", (ScenarioAssumption("lead_time", "7d"),))
    outcome = ScenarioOutcome("s-1", "risco de atraso", 0.7, ("expedicao",))
    updated = scenario.add_outcome(outcome)
    assert scenario.outcomes == ()
    assert updated.outcomes == (outcome,)


def test_decision_and_feedback_keep_traceability():
    decision = DecisionRecord("d-1", "replanejar", "evitar ruptura", ("ev-1",), "OPERACIONAL", "o-1")
    feedback = OutcomeFeedback("d-1", "o-1", "reduzir atraso", "atraso reduzido", "SUPPORTED", ("ev-2",))
    assert decision.outcome_id == feedback.outcome_id


def test_temporal_validity():
    observed = datetime(2026, 8, 1, tzinfo=timezone.utc)
    validity = TemporalValidity(observed, observed)
    assert validity.is_valid_at(observed) is True


def test_uncertainty_and_directory_profiles_are_typed():
    assessment = UncertaintyAssessment("PROBABLE", 0.6, 2, "evidence incomplete")
    profile = DirectorySemanticProfile("src/elo/core", "runtime core", "cognitive boundaries", "canonical", "active")
    directory = DirectoryAssessment(profile.path, "REUSE", "canonical owner exists")
    assert assessment.confidence == 0.6
    assert directory.action == "REUSE"
