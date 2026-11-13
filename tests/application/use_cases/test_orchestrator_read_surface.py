from elo.application.use_cases.orchestrator import GovernedOrchestrator
from elo.application.use_cases.orchestrator_read_surface import GovernedOrchestratorReadSurface
from elo.application.use_cases.orchestration_views import OrchestrationAudience, OrchestrationView
from elo.cognitive.symbiont_capability_governance import GlobalCapabilityVisibility


def test_read_surface_builds_systemic_view_without_mutation():
    surface = GovernedOrchestratorReadSurface.build(GovernedOrchestrator())
    result = surface.systemic_overview(
        audience=OrchestrationAudience.ELO_DEVELOPER,
        visibility=GlobalCapabilityVisibility(records=()),
    )

    assert result.view is OrchestrationView.SYSTEMIC
    assert result.read_only is True
    assert result.canonical_mutation is False


def test_operational_read_surface_projects_existing_context_only():
    surface = GovernedOrchestratorReadSurface.build(GovernedOrchestrator())
    context = {
        "governed_discovery": {
            "scope": "cross_domain_demand_and_impacts",
            "linked_records": {
                "elo_sim_demanda": [{"id": "DEM-1"}],
                "v_elo_pcp_carga_capacidade_periodo": [],
            },
        },
        "evidence_by_source": {"elo_sim_demanda": ["ev:demand"]},
    }

    result = surface.operational_overview(
        audience=OrchestrationAudience.CORPORATE_INTERFACE,
        forge_context=context,
    )

    assert result.view is OrchestrationView.OPERATIONAL
    assert result.operational_sections["demand"] == [{"id": "DEM-1"}]
    assert result.operational_sections["capacity"] == []
    assert result.evidence_refs == ("ev:demand",)
    assert result.read_only is True
    assert result.canonical_mutation is False
