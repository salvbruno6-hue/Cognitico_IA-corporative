from elo.core.context_resolution import ContextEvidence, ContextPack, ContextQuery, ContextResolutionEngine, ContextSource
from elo.core.diagnostic_scenario_engine import DiagnosticLens, DiagnosticObservation, DiagnosticScenarioEngine
from elo.core.gpt_handoff import GPTDecisionHandoff
from elo.core.maturity_engine import MATURITY_DIMENSIONS, MaturityAssessment


def mature():
    return MaturityAssessment({dimension: 0.9 for dimension in MATURITY_DIMENSIONS})


def test_question_discovers_context_without_user_path():
    query = ContextQuery(
        "qual o estado da Multiteiner Caxias?",
        entity="Multiteiner",
        scope="Duque de Caxias",
        dimensions=("operacao", "pcp", "risco"),
    )
    pack = ContextResolutionEngine().resolve(query)
    assert pack.discovery_plan is not None
    assert pack.discovery_plan.entities == ("Multiteiner",)
    assert ContextResolutionEngine.candidate_sources(pack)


def test_local_scope_excludes_other_unit_evidence():
    query = ContextQuery("estado da Multiteiner Caxias", "Multiteiner", "Duque de Caxias")
    pack = ContextPack(
        query=query,
        sources=(
            ContextSource("caxias", "project", "authorized", "Duque de Caxias"),
            ContextSource("other", "project", "authorized", "São Paulo"),
        ),
        evidence=(
            ContextEvidence("caxias", "pedido local", 0.9),
            ContextEvidence("other", "pedido de outra unidade", 0.95),
        ),
    )
    assert [item.source_id for item in pack.scoped_evidence()] == ["caxias"]


def test_insufficient_context_blocks_specialist():
    query = ContextQuery("estado da Multiteiner Caxias", "Multiteiner", "Duque de Caxias")
    pack = ContextResolutionEngine().resolve(query)
    assert not pack.requires_specialist()
    try:
        GPTDecisionHandoff.from_context(
            objective="diagnóstico",
            context=pack,
            maturity=mature(),
        )
    except ValueError as exc:
        assert "scoped evidence" in str(exc)
    else:
        raise AssertionError("specialist handoff must require scoped evidence")


def test_same_problem_can_be_compared_through_multiple_lenses():
    engine = DiagnosticScenarioEngine()
    scenarios = (
        engine.build(
            "capacity",
            "atraso por capacidade",
            (DiagnosticObservation(DiagnosticLens.CAPACITY, "turno insuficiente", ("ev-1",), confidence=0.8),),
        ),
        engine.build(
            "material",
            "atraso por material",
            (DiagnosticObservation(DiagnosticLens.MATERIAL, "insumo crítico", ("ev-1", "ev-2"), confidence=0.8),),
        ),
    )
    result = engine.compare(scenarios)
    assert result["status"] == "COMPARABLE"
    assert result["shared_evidence"] == ("ev-1",)
    assert set(result["covered_lenses"]) == {DiagnosticLens.CAPACITY, DiagnosticLens.MATERIAL}


def test_maturity_threshold_controls_specialist_mode():
    scores = {dimension: 0.9 for dimension in MATURITY_DIMENSIONS}
    scores["evidence_analysis"] = 0.74
    assert MaturityAssessment(scores).mode == "DISCOVERY_ASSIST"
    scores["evidence_analysis"] = 0.75
    assert MaturityAssessment(scores).mode == "SPECIALIST_VALIDATION"
