from elo.core.consultative_orchestration import ConsultativeOrchestrator
from elo.core.context_resolution import (
    ContextEvidence,
    ContextPack,
    ContextQuery,
    ContextResolutionEngine,
    ContextSource,
)
from elo.core.maturity_engine import MaturityAssessment


def _base_pack(*, uncertainties=(), gaps=(), sources=(), evidence=()):
    query = ContextQuery(question="avaliar atendimento", domain="PCP")
    resolved = ContextResolutionEngine().resolve(query)
    return ContextPack(
        query=resolved.query,
        discovery_plan=resolved.discovery_plan,
        sources=sources,
        evidence=evidence,
        uncertainties=uncertainties,
        gaps=gaps,
    )


def _maturity():
    return MaturityAssessment(scores={})


def test_simple_clean_handoff_does_not_activate_eaif_refinement():
    handoff = ConsultativeOrchestrator().prepare(
        context=_base_pack(),
        maturity=_maturity(),
        objective="responder consulta simples",
    )
    assert handoff.analytical_refinement == "NONE"
    assert handoff.analytical_checks == ()
    assert "analytical-integrity" not in handoff.specialist_instruction()


def test_uncertainty_activates_targeted_refinement():
    handoff = ConsultativeOrchestrator().prepare(
        context=_base_pack(uncertainties=("capacidade ainda não revalidada",)),
        maturity=_maturity(),
        objective="avaliar capacidade",
    )
    assert handoff.analytical_refinement == "TARGETED"
    assert handoff.analytical_refinement_reasons
    payload = handoff.consultation_payload()
    assert payload["analytical_refinement"] == "TARGETED"
    assert payload["analytical_checks"]
    assert "analytical-integrity" in payload["specialist_instruction"]


def test_explicit_conflict_activates_deep_refinement():
    handoff = ConsultativeOrchestrator().prepare(
        context=_base_pack(),
        maturity=_maturity(),
        objective="resolver divergência",
        analytical_conflicts=("estoque fonte A difere da fonte B",),
    )
    assert handoff.analytical_refinement == "DEEP"
    assert "counterevidence" in handoff.specialist_instruction()


def test_consequential_action_with_gap_activates_deep_refinement():
    handoff = ConsultativeOrchestrator().prepare(
        context=_base_pack(gaps=("saldo disponível não comprovado",)),
        maturity=_maturity(),
        objective="avaliar compra",
        consequential_action=True,
    )
    assert handoff.analytical_refinement == "DEEP"
    assert handoff.decision_required is True


def test_explicit_historical_temporal_validity_activates_targeted_refinement():
    source = ContextSource(
        source_id="capacity-history",
        source_type="operational",
        authority="PCP",
        domain="PCP",
        temporal_validity="historical",
    )
    evidence = ContextEvidence(
        source_id="capacity-history",
        fact="6 modules/day",
        confidence=0.9,
        domain="PCP",
        temporal_validity="historical",
    )
    handoff = ConsultativeOrchestrator().prepare(
        context=_base_pack(sources=(source,), evidence=(evidence,)),
        maturity=_maturity(),
        objective="avaliar capacidade atual",
    )
    assert handoff.analytical_refinement == "TARGETED"
    assert any("historical" in reason or "historical" in check for reason in handoff.analytical_refinement_reasons for check in handoff.analytical_checks)


def test_arbitrary_temporal_window_is_not_invented_as_risk():
    source = ContextSource(
        source_id="current-window",
        source_type="operational",
        authority="PCP",
        domain="PCP",
        temporal_validity="2026-10-01/2026-10-31",
    )
    handoff = ConsultativeOrchestrator().prepare(
        context=_base_pack(sources=(source,)),
        maturity=_maturity(),
        objective="consulta de período",
    )
    assert handoff.analytical_refinement == "NONE"
