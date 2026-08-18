from elo.core.context_resolution import ContextEvidence, ContextQuery, ContextResolutionEngine, ContextSource
from elo.core.core_loop import CoreLoopEngine, CoreLoopRequest
from elo.core.diagnostic_scenarios import DiagnosticLens, DiagnosticObservation, DiagnosticScenario, DiagnosticStatus


def context():
    engine = ContextResolutionEngine()
    pack = engine.resolve(ContextQuery("avaliar capacidade", tenant_id="tenant-a", domain="PCP"))
    return engine.enrich(
        pack,
        sources=(ContextSource("e1", "document", "external", tenant_id="tenant-a", domain="PCP"),),
        evidence=(ContextEvidence("e1", "capacity evidence", 0.9, tenant_id="tenant-a", domain="PCP"),),
    )


def observation(evidence_id, lens, confidence=0.9, status=DiagnosticStatus.SUPPORTED):
    return DiagnosticObservation(
        evidence_id=evidence_id,
        dimension=lens.value,
        value=0.9,
        statement=f"finding-{lens.value}",
        confidence=confidence,
        lens=lens,
        status=status,
    )


def test_core_loop_covers_multiple_lenses_without_execution_authority():
    observations = (
        observation("e1", DiagnosticLens.OPERATIONAL),
        observation("e1", DiagnosticLens.CAPACITY),
        observation("e1", DiagnosticLens.MATERIAL),
        observation("e1", DiagnosticLens.FINANCIAL),
        observation("e1", DiagnosticLens.CUSTOMER),
        observation("e1", DiagnosticLens.RISK),
        observation("e1", DiagnosticLens.TEMPORAL),
        observation("e1", DiagnosticLens.SYSTEMIC),
    )
    scenario = DiagnosticScenario("s1", "avaliar capacidade", observations=observations)
    result = CoreLoopEngine().run(CoreLoopRequest(context(), scenario, observations))
    assert result.status == "RECOMMENDATION"
    assert set(result.covered_lenses) == {lens.value for lens in DiagnosticLens if lens != DiagnosticLens.EVIDENCE}
    assert result.can_execute is False


def test_core_loop_blocks_conflicting_evidence_and_requires_handoff():
    observations = (
        observation("e1", DiagnosticLens.OPERATIONAL),
        observation("e1", DiagnosticLens.CAPACITY, status=DiagnosticStatus.CONFLICTING),
    )
    scenario = DiagnosticScenario("s2", "avaliar conflito", observations=observations)
    result = CoreLoopEngine().run(CoreLoopRequest(context(), scenario, observations))
    assert result.status == "HANDOFF"
    assert result.handoff_required is True
    assert "conflicting specialist evidence" in result.gaps


def test_core_loop_blocks_low_confidence_and_never_mutates_context():
    pack = context()
    observations = (observation("e1", DiagnosticLens.OPERATIONAL, confidence=0.4),)
    scenario = DiagnosticScenario("s3", "avaliar baixa confiança", observations=observations)
    before = pack
    result = CoreLoopEngine().run(CoreLoopRequest(pack, scenario, observations, minimum_confidence=0.7))
    assert result.status == "HANDOFF"
    assert result.handoff_required is True
    assert pack == before


def test_core_loop_with_no_observations_is_blocked_not_invented():
    scenario = DiagnosticScenario("s4", "avaliar sem evidência")
    result = CoreLoopEngine().run(CoreLoopRequest(context(), scenario))
    assert result.status == "BLOCKED"
    assert result.evidence_ids == ("e1",)
    assert result.handoff_required is True
