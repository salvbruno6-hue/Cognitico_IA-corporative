from elo.agent_intake.symbiont_implementation_view import (
    ImplementationOwnership,
    ImplementationViewPhase,
    create_implementation_view,
)
from elo.application.use_cases.orchestrator import GovernedOrchestrator
from elo.cognitive.symbiont_capability_governance import (
    CapabilityVisibilityState,
    build_global_capability_visibility,
)
from elo.core.capability_registry import CapabilityProbe, CapabilityRegistry


def _view():
    return create_implementation_view(
        implementation_id="impl-role-health",
        phase=ImplementationViewPhase.END,
        candidate_id="EXT-ROLE-HEALTH",
        owner="canonical-owner",
        functional_branch="cognitive/evolution",
        capability="EXT-ROLE-HEALTH",
        source_ref="src:role-health",
        source_commit="commit:role-health",
        loop_stage="IMPLEMENTATION",
        ownership=ImplementationOwnership.EXTENSION,
        evidence_refs=("impl-view:role-health",),
        evolution_gate_status="REQUIRED",
        governance_status="READY_FOR_ELO_REVIEW",
        runtime_status="INTEGRATED",
    )


def _registry():
    return CapabilityRegistry((
        CapabilityProbe(
            "LOCAL_RUNTIME",
            "EXT-ROLE-HEALTH",
            health_check=lambda: True,
            metadata={"capabilities": "EXT-ROLE-HEALTH"},
        ),
    ))


def test_symbiont_surfaces_required_runtime_wiring_gaps_without_inferring_links():
    result = build_global_capability_visibility(
        registry_snapshot=_registry().snapshot(),
        implementation_views=(_view(),),
        require_runtime_wiring=("EXT-ROLE-HEALTH",),
    )
    record = result.records[0]

    assert record.state is CapabilityVisibilityState.EXISTING_BUT_UNWIRED
    assert record.missing_runtime_links == (
        "consumer",
        "canonical_route",
        "execution_boundary",
    )
    assert record.consumer is None
    assert record.canonical_route is None
    assert record.execution_boundary is None
    assert result.canonical_mutation is False
    assert "missing_runtime_links=consumer,canonical_route,execution_boundary" in result.blockers[0]


def test_required_only_capability_is_not_invisible_when_wholly_missing():
    result = build_global_capability_visibility(
        registry_snapshot=(),
        implementation_views=(),
        require_runtime_wiring=("MISSING-RUNTIME-CAPABILITY",),
    )

    assert len(result.records) == 1
    record = result.records[0]
    assert record.capability_id == "MISSING-RUNTIME-CAPABILITY"
    assert record.state is CapabilityVisibilityState.EXISTING_BUT_UNWIRED
    assert record.registry_visible is False
    assert record.implementation_visible is False
    assert record.missing_runtime_links == (
        "consumer",
        "canonical_route",
        "execution_boundary",
    )
    assert result.blockers


def test_orchestrator_applies_symbiont_observation_but_does_not_self_authorize_fix():
    visibility = build_global_capability_visibility(
        registry_snapshot=_registry().snapshot(),
        implementation_views=(_view(),),
        require_runtime_wiring=("EXT-ROLE-HEALTH",),
    )

    orientation = GovernedOrchestrator().advise_capability(
        visibility,
        "EXT-ROLE-HEALTH",
    )

    assert orientation.action == "CONNECT_CANONICAL"
    assert orientation.authorized is False
    assert orientation.owner == "canonical-owner"


def test_orchestrator_can_mark_canonical_connection_action_only_when_explicitly_authorized():
    visibility = build_global_capability_visibility(
        registry_snapshot=_registry().snapshot(),
        implementation_views=(_view(),),
        require_runtime_wiring=("EXT-ROLE-HEALTH",),
    )

    orientation = GovernedOrchestrator().advise_capability(
        visibility,
        "EXT-ROLE-HEALTH",
        authorized_actions=frozenset({"CONNECT_CANONICAL"}),
    )

    assert orientation.action == "CONNECT_CANONICAL"
    assert orientation.authorized is True


def test_runtime_wiring_health_becomes_visible_only_with_explicit_evidence():
    result = build_global_capability_visibility(
        registry_snapshot=_registry().snapshot(),
        implementation_views=(_view(),),
        consumers={"EXT-ROLE-HEALTH": "CapabilitySelector"},
        canonical_routes={"EXT-ROLE-HEALTH": "ExecutionRouter"},
        execution_boundaries={"EXT-ROLE-HEALTH": "ExecutionBoundary"},
        require_runtime_wiring=("EXT-ROLE-HEALTH",),
    )
    record = result.records[0]

    assert record.state is CapabilityVisibilityState.REGISTERED_VISIBLE
    assert record.missing_runtime_links == ()
    assert record.consumer == "CapabilitySelector"
    assert record.canonical_route == "ExecutionRouter"
    assert record.execution_boundary == "ExecutionBoundary"
    assert result.blockers == ()


def test_symbiont_prioritizes_internal_alignment_before_new_capability_work():
    registry = _registry().snapshot()
    result = build_global_capability_visibility(
        registry_snapshot=registry,
        implementation_views=(_view(),),
        declared_capabilities=("REGISTERED-WITHOUT-VIEW",),
        require_runtime_wiring=("EXT-ROLE-HEALTH", "MISSING-RUNTIME-CAPABILITY"),
    )

    candidates = result.improvement_candidates

    assert candidates
    assert candidates[0].state is CapabilityVisibilityState.EXISTING_BUT_UNWIRED
    assert [item.capability_id for item in candidates] == result.as_dict()["improvement_candidates"]
    assert all(item.state is not CapabilityVisibilityState.REGISTERED_VISIBLE for item in candidates)


def test_orchestrator_consumes_first_symbiont_improvement_candidate_without_self_authorizing():
    visibility = build_global_capability_visibility(
        registry_snapshot=_registry().snapshot(),
        implementation_views=(_view(),),
        require_runtime_wiring=("EXT-ROLE-HEALTH",),
    )

    first = visibility.improvement_candidates[0]
    orientation = GovernedOrchestrator().advise_capability(visibility, first.capability_id)

    assert first.capability_id == "EXT-ROLE-HEALTH"
    assert orientation.action == "CONNECT_CANONICAL"
    assert orientation.authorized is False
