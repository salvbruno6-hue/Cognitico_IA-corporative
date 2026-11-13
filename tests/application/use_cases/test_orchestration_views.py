from elo.application.use_cases.orchestration_views import (
    OrchestrationAudience,
    OrchestrationView,
    OrchestrationViewComposer,
)
from elo.cognitive.symbiont_capability_governance import (
    CapabilityVisibilityRecord,
    CapabilityVisibilityState,
    GlobalCapabilityVisibility,
)


def _visibility():
    return GlobalCapabilityVisibility(
        records=(
            CapabilityVisibilityRecord(
                capability_id="cap:healthy",
                registry_visible=True,
                available=True,
                implementation_visible=True,
                owner="core",
                runtime_status="OBSERVED",
                evolution_status="CANONICAL",
                evidence_refs=("ev:healthy",),
                state=CapabilityVisibilityState.REGISTERED_VISIBLE,
            ),
            CapabilityVisibilityRecord(
                capability_id="cap:unwired",
                registry_visible=False,
                available=False,
                implementation_visible=True,
                owner="forge",
                runtime_status="NOT_PROVEN",
                evolution_status="INDETERMINADO",
                evidence_refs=("ev:unwired",),
                state=CapabilityVisibilityState.EXISTING_BUT_UNWIRED,
            ),
        )
    )


def test_systemic_view_is_admin_developer_only_and_humanizes_capability_skill_gaps():
    composer = OrchestrationViewComposer()
    result = composer.systemic_view(
        audience=OrchestrationAudience.ELO_ADMIN,
        visibility=_visibility(),
        skill_statuses=(
            {
                "skill_id": "skill:budget-analysis",
                "state": "PARCIAL",
                "reason": "runtime evidence is incomplete",
                "positive_impact": "When functional, budget analysis can explain why a solicitation should proceed, be revised or be declined using governed evidence.",
                "recommendation": "Connect the skill to its governed runtime evidence before depending on it.",
                "evidence_refs": ("ev:skill",),
            },
        ),
    )

    assert result.view is OrchestrationView.SYSTEMIC
    assert result.status == "ATTENTION"
    assert result.read_only is True
    assert result.canonical_mutation is False
    assert {item.code for item in result.diagnostics} >= {"cap:unwired", "skill:budget-analysis"}
    assert any("reduzindo pontos cegos" in item.impact for item in result.diagnostics if item.code == "cap:unwired")
    assert {chart.chart_id for chart in result.charts} == {"capability_visibility", "systemic_gaps"}
    assert set(result.evidence_refs) == {"ev:healthy", "ev:unwired", "ev:skill"}


def test_systemic_view_rejects_corporate_operator():
    composer = OrchestrationViewComposer()
    try:
        composer.systemic_view(
            audience=OrchestrationAudience.CORPORATE_OPERATOR,
            visibility=_visibility(),
        )
    except PermissionError as exc:
        assert "administrator/developer" in str(exc)
    else:
        raise AssertionError("corporate operator must not receive the systemic ELO view")


def test_operational_view_exposes_forge_domains_without_promoting_missing_data():
    composer = OrchestrationViewComposer()
    context = {
        "governed_discovery": {
            "scope": "cross_domain_demand_and_impacts",
            "linked_records": {
                "elo_sim_demanda": [{"id": "DEM-1", "quantidade": 20}],
                "elo_sim_demanda_recursos": [{"demanda_id": "DEM-1", "horas": 65}],
                "v_elo_pcp_cobertura_demanda_externa": [{"estado_cobertura": "DEFICIT_FABRICACAO"}],
                "v_elo_pcp_carga_capacidade_periodo": [],
                "v_elo_pcp_dados_pendentes": [
                    {
                        "codigo": "HISTORICO_COMPARAVEL",
                        "bloqueia_execucao": True,
                        "motivo": "historical comparable demand is missing",
                        "pergunta_gpt": "Informe o histórico comparável na fonte autorizada.",
                    }
                ],
                "elo_orcamento_decisoes": [{"status": "AGUARDANDO_VALIDACAO"}],
            },
            "not_scoped": [{"table_name": "mt_ordens_reparo", "reason": "no safe relationship"}],
        },
        "evidence_by_source": {
            "elo_sim_demanda": ["ev:demand"],
            "v_elo_pcp_cobertura_demanda_externa": ["ev:coverage"],
        },
    }

    result = composer.operational_view(
        audience=OrchestrationAudience.CORPORATE_INTERFACE,
        forge_context=context,
    )

    assert result.view is OrchestrationView.OPERATIONAL
    assert result.status == "OBSERVED"
    assert result.operational_sections["demand"][0]["id"] == "DEM-1"
    assert result.operational_sections["capacity"] == []
    assert result.operational_sections["budget_learning"][0]["status"] == "AGUARDANDO_VALIDACAO"
    assert result.diagnostics[0].state == "BLOQUEADO_POR_DADOS"
    assert "não converte ausência" in result.charts[0].note
    assert set(result.evidence_refs) == {"ev:demand", "ev:coverage"}
    assert result.canonical_mutation is False
