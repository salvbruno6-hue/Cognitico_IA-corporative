from elo.application.use_cases.orchestration_views import (
    OrchestrationAudience,
    OrchestrationView,
    OrchestrationViewComposer,
)
from elo.cognitive.symbiont_capability_governance import GlobalCapabilityVisibility


def _empty_operational_context():
    return {
        "governed_discovery": {
            "scope": "cross_domain_demand_and_impacts",
            "linked_records": {},
        },
        "evidence_by_source": {},
    }


def test_admin_has_both_systemic_and_operational_views():
    composer = OrchestrationViewComposer()

    systemic = composer.systemic_view(
        audience=OrchestrationAudience.ELO_ADMIN,
        visibility=GlobalCapabilityVisibility(records=()),
    )
    operational = composer.operational_view(
        audience=OrchestrationAudience.ELO_ADMIN,
        forge_context=_empty_operational_context(),
    )

    assert systemic.view is OrchestrationView.SYSTEMIC
    assert operational.view is OrchestrationView.OPERATIONAL
    assert systemic.read_only is True
    assert operational.read_only is True


def test_developer_has_both_systemic_and_operational_views():
    composer = OrchestrationViewComposer()

    systemic = composer.systemic_view(
        audience=OrchestrationAudience.ELO_DEVELOPER,
        visibility=GlobalCapabilityVisibility(records=()),
    )
    operational = composer.operational_view(
        audience=OrchestrationAudience.ELO_DEVELOPER,
        forge_context=_empty_operational_context(),
    )

    assert systemic.view is OrchestrationView.SYSTEMIC
    assert operational.view is OrchestrationView.OPERATIONAL


def test_corporate_operator_remains_operational_only():
    composer = OrchestrationViewComposer()

    operational = composer.operational_view(
        audience=OrchestrationAudience.CORPORATE_OPERATOR,
        forge_context=_empty_operational_context(),
    )
    assert operational.view is OrchestrationView.OPERATIONAL

    try:
        composer.systemic_view(
            audience=OrchestrationAudience.CORPORATE_OPERATOR,
            visibility=GlobalCapabilityVisibility(records=()),
        )
    except PermissionError:
        pass
    else:
        raise AssertionError("corporate operator must remain operational-only")
