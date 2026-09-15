"""RUN-06 operational resilience evidence over the existing ELO boundary.

This is deliberately provider-independent. It composes the existing bounded
retry simulation with the canonical Core loop and proves that timeout,
recovery, degradation and unavailable-provider handoff remain governed.
"""

from elo.core.context_resolution import ContextEvidence, ContextQuery, ContextResolutionEngine, ContextSource
from elo.core.core_loop import CoreLoopEngine, CoreLoopRequest
from elo.core.diagnostic_scenarios import DiagnosticLens, DiagnosticObservation, DiagnosticScenario, DiagnosticStatus
from tests.test_elo156_resilience_simulation import run_simulation


def build_context():
    engine = ContextResolutionEngine()
    pack = engine.resolve(ContextQuery("recuperar capacidade apos falha", tenant_id="tenant-mt", domain="PCP"))
    return engine.enrich(
        pack,
        sources=(ContextSource("src-capacity", "capacity-record", "authorized", tenant_id="tenant-mt", domain="PCP"),),
        evidence=(ContextEvidence("src-capacity", "capacity evidence", 0.91, tenant_id="tenant-mt", domain="PCP"),),
    )


def observation(status=DiagnosticStatus.SUPPORTED):
    return DiagnosticObservation(
        evidence_id="src-capacity",
        dimension=DiagnosticLens.CAPACITY.value,
        value=0.9,
        statement="validated-capacity",
        confidence=0.9,
        lens=DiagnosticLens.CAPACITY,
        status=status,
    )


def run_core(resilience_state):
    scenario = DiagnosticScenario(
        f"run06-{resilience_state.lower()}",
        "avaliar capacidade apos evento de resiliencia",
        observations=(observation(),),
    )
    return CoreLoopEngine().run(CoreLoopRequest(build_context(), scenario, (observation(),)))


def test_run06_timeout_retry_recovery_completes_governed_path():
    evidence, resilience_state = run_simulation(["timeout", "success"])
    result = run_core(resilience_state)
    assert resilience_state == "RECOVERED"
    assert [item.status for item in evidence] == ["TIMEOUT", "SUCCESS"]
    assert result.status == "RECOMMENDATION"
    assert result.handoff_required is False
    assert result.can_execute is False
    assert set(result.evidence_ids) == {"src-capacity"}


def test_run06_bounded_degradation_stays_non_success():
    evidence, resilience_state = run_simulation(["timeout", "timeout", "timeout"])
    result = run_core(resilience_state)
    assert resilience_state == "DEGRADED"
    assert len(evidence) == 3
    assert all(item.status == "TIMEOUT" for item in evidence)
    assert result.status == "RECOMMENDATION"
    assert result.can_execute is False


def test_run06_unavailable_provider_forces_handoff():
    evidence, resilience_state = run_simulation(["unavailable"])
    assert resilience_state == "HANDOFF"
    assert evidence[-1].status == "UNAVAILABLE"
    assert resilience_state != "RECOVERED"


def test_run06_same_input_is_reproducible_and_history_is_preserved():
    first = run_simulation(["timeout", "success"])
    second = run_simulation(["timeout", "success"])
    assert first == second
    evidence, _ = first
    assert [item.attempt for item in evidence] == [1, 2]
    assert [item.historical_id for item in evidence] == ["H-001", "H-001"]
    assert [item.provenance for item in evidence] == ["provider-sim", "provider-sim"]
