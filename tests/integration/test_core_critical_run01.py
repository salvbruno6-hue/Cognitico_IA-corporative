"""RUN-01 critical-path evidence for the canonical ELO Core loop.

The test intentionally stops at recommendation/handoff. Execution remains outside
CoreLoopEngine and requires a separate governed authorization boundary.
"""

from elo.core.context_resolution import ContextEvidence, ContextQuery, ContextResolutionEngine, ContextSource
from elo.core.core_loop import CoreLoopEngine, CoreLoopRequest
from elo.core.diagnostic_scenarios import DiagnosticLens, DiagnosticObservation, DiagnosticScenario, DiagnosticStatus


def build_context():
    engine = ContextResolutionEngine()
    pack = engine.resolve(ContextQuery("planejar capacidade sazonal", tenant_id="tenant-mt", domain="PCP"))
    return engine.enrich(
        pack,
        sources=(
            ContextSource("src-demand", "planning-record", "authorized", tenant_id="tenant-mt", domain="PCP"),
            ContextSource("src-capacity", "capacity-record", "authorized", tenant_id="tenant-mt", domain="PCP"),
        ),
        evidence=(
            ContextEvidence("src-demand", "seasonal demand evidence", 0.92, tenant_id="tenant-mt", domain="PCP"),
            ContextEvidence("src-capacity", "available capacity evidence", 0.91, tenant_id="tenant-mt", domain="PCP"),
        ),
    )


def observation(evidence_id, lens):
    return DiagnosticObservation(
        evidence_id=evidence_id,
        dimension=lens.value,
        value=0.9,
        statement=f"validated-{lens.value}",
        confidence=0.9,
        lens=lens,
        status=DiagnosticStatus.SUPPORTED,
    )


def test_run01_intent_context_evidence_reasoning_decision_next_action():
    context = build_context()
    observations = (
        observation("src-demand", DiagnosticLens.CUSTOMER),
        observation("src-demand", DiagnosticLens.TEMPORAL),
        observation("src-capacity", DiagnosticLens.CAPACITY),
        observation("src-capacity", DiagnosticLens.OPERATIONAL),
        observation("src-capacity", DiagnosticLens.RISK),
    )
    scenario = DiagnosticScenario(
        "run01-seasonal-capacity",
        "planejar capacidade sazonal sem inventar dados",
        observations=observations,
    )

    result = CoreLoopEngine().run(CoreLoopRequest(context, scenario, observations))

    assert result.status == "RECOMMENDATION"
    assert result.handoff_required is False
    assert result.confidence >= 0.7
    assert set(result.evidence_ids) == {"src-demand", "src-capacity"}
    assert set(result.covered_lenses) == {item.lens.value for item in observations}
    assert result.recommendation is not None
    assert result.can_execute is False


def test_run01_missing_evidence_becomes_gap_and_handoff():
    context = build_context()
    scenario = DiagnosticScenario("run01-gap", "planejar sem observações")
    result = CoreLoopEngine().run(CoreLoopRequest(context, scenario))

    assert result.status == "BLOCKED"
    assert result.handoff_required is True
    assert "no diagnostic evidence supplied" in result.gaps
    assert result.can_execute is False


def test_run01_conflict_does_not_become_decision():
    context = build_context()
    observations = (
        observation("src-demand", DiagnosticLens.CUSTOMER),
        DiagnosticObservation(
            evidence_id="src-capacity",
            dimension=DiagnosticLens.CAPACITY.value,
            value=0.2,
            statement="conflicting capacity finding",
            confidence=0.8,
            lens=DiagnosticLens.CAPACITY,
            status=DiagnosticStatus.CONFLICTING,
        ),
    )
    scenario = DiagnosticScenario("run01-conflict", "avaliar capacidade conflitante", observations=observations)
    result = CoreLoopEngine().run(CoreLoopRequest(context, scenario, observations))

    assert result.status == "HANDOFF"
    assert result.handoff_required is True
    assert "conflicting specialist evidence" in result.gaps
    assert result.recommendation is None
    assert result.can_execute is False
