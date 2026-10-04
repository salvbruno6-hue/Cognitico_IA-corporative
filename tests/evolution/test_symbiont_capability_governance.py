from elo.agent_intake.implementation_loop_readiness import LoopReadiness
from elo.agent_intake.symbiont_implementation_view import (
    ImplementationOwnership,
    ImplementationViewPhase,
    create_implementation_view,
)
from elo.cognitive.symbiont_capability_evolution import (
    CapabilityEvolutionReview,
    CapabilityStatusReport,
    CapabilityCondition,
    CapabilityConditionStatus,
    CapabilityReadinessStatus,
)
from elo.cognitive.symbiont_capability_governance import (
    orchestrate_capability_governance,
)


def _view():
    return create_implementation_view(
        implementation_id="impl-1",
        phase=ImplementationViewPhase.END,
        candidate_id="EXT-TEST",
        owner="canonical-owner",
        functional_branch="cognitive/evolution",
        capability="EXT-TEST",
        source_ref="src:test",
        source_commit="commit:test",
        loop_stage="IMPLEMENTATION",
        ownership=ImplementationOwnership.EXTENSION,
        evidence_refs=("impl-view:1",),
        evolution_gate_status="REQUIRED",
        governance_status="READY_FOR_ELO_REVIEW",
        runtime_status="INTEGRATED",
    )


def _status():
    return CapabilityStatusReport(
        capability_id="EXT-TEST",
        capability_name="Test",
        owner="canonical-owner",
        authority="canonical-owner",
        status=CapabilityReadinessStatus.OPERATIONALLY_EVIDENCED,
        conditions=(
            CapabilityCondition(
                name="RUNTIME_INTEGRATION",
                status=CapabilityConditionStatus.VERIFIED,
                evidence_refs=("runtime:1",),
            ),
        ),
        missing_conditions=("PRODUCTION_OUTCOME",),
        blockers=(),
        evidence_refs=("runtime:1",),
        next_action="Continue governed observation.",
        production_proven=False,
    )


def _review():
    return CapabilityEvolutionReview(
        trigger_id="EVOLUÇÃO_DE_CAPACIDADES",
        status="ANALYSIS_READY",
        metrics=(),
        actions=(),
        evidence_refs=("evolution:1",),
    )


def _result(*, ready=True):
    return orchestrate_capability_governance(
        implementation_view=_view(),
        readiness=LoopReadiness(
            candidate_id="EXT-TEST",
            ready_for_loop=ready,
            missing=() if ready else ("provenance", "repeatability"),
        ),
        evolution_review=_review(),
        status_report=_status(),
    )


def test_orchestration_reuses_existing_authorities():
    result = _result()
    pairs = {(item.source, item.relation, item.target) for item in result.relations}
    assert ("SIMBIONTE", "DIAGNOSES", "EXT-TEST") in pairs
    assert ("Capability Registry", "EXPOSES", "EXT-TEST") in pairs
    assert ("Capability Selector", "SELECTS", "EXT-TEST") in pairs
    assert ("EXT-TEST", "OWNED_BY", "canonical-owner") in pairs
    assert ("ExecutionRouter", "ROUTES", "EXT-TEST") in pairs
    assert ("AgentOrchestrator", "DELEGATES", "EXT-TEST") in pairs
    assert ("ExecutionBoundary", "GOVERNS_EXECUTION", "EXT-TEST") in pairs
    assert ("CapabilityEvolutionReview", "HANDOFF_TO", "Evolution Gate") in pairs
    assert result.canonical_mutation is False


def test_orchestration_surfaces_readiness_blockers_without_authorizing():
    result = _result(ready=False)
    assert "readiness:provenance" in result.blockers
    assert "readiness:repeatability" in result.blockers
    assert result.canonical_mutation is False


def test_orchestration_never_converts_evolution_review_into_promotion():
    result = _result()
    gate_edges = [item for item in result.relations if item.target == "canonical promotion/merge decision"]
    assert gate_edges
    assert all(item.condition == "explicit authorization required" for item in gate_edges)


from elo.core.capability_registry import CapabilityProbe, CapabilityRegistry
from elo.cognitive.symbiont_capability_governance import (
    CapabilityVisibilityState,
    build_global_capability_visibility,
)


def test_global_visibility_reconciles_registry_and_implementation_views():
    registry = CapabilityRegistry((
        CapabilityProbe(
            "LOCAL_RUNTIME",
            "registered-capability",
            health_check=lambda: True,
            metadata={"capabilities": "registered-capability"},
        ),
    ))
    result = build_global_capability_visibility(
        registry_snapshot=registry.snapshot(),
        implementation_views=(_view(),),
        declared_capabilities=("declared-only",),
    )
    states = {item.capability_id: item.state for item in result.records}
    assert states["registered-capability"] is CapabilityVisibilityState.REGISTERED_WITHOUT_IMPLEMENTATION_VIEW
    assert states["EXT-TEST"] is CapabilityVisibilityState.IMPLEMENTED_NOT_REGISTERED
    assert states["declared-only"] is CapabilityVisibilityState.EXISTING_BUT_UNWIRED
    assert result.canonical_mutation is False


def test_global_visibility_copies_runtime_and_evolution_status_without_inference():
    registry = CapabilityRegistry((
        CapabilityProbe(
            "LOCAL_RUNTIME",
            "EXT-TEST",
            health_check=lambda: True,
            metadata={"capabilities": "EXT-TEST"},
        ),
    ))
    result = build_global_capability_visibility(
        registry_snapshot=registry.snapshot(),
        implementation_views=(_view(),),
    )
    record = result.records[0]
    assert record.state is CapabilityVisibilityState.REGISTERED_VISIBLE
    assert record.runtime_status == "INTEGRATED"
    assert record.evolution_status == "REQUIRED"
    assert record.evidence_refs == ("impl-view:1",)
