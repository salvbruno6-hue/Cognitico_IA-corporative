from elo.cognitive.pcp_analytical_integrity import (
    guard_capacity_claim,
    guard_pcp_action_authorization,
)
from elo.cognitive.reasoning.analytical_integrity import SourceRole
from elo.cognitive.reasoning.requirement_analysis import RequirementState


def _codes(findings):
    return {finding.code for finding in findings}


def test_historical_pcp_capacity_is_not_promoted_to_current():
    findings = guard_capacity_claim(
        subject="fibra_modulos_dia",
        state=RequirementState.KNOWN,
        capacity_kind="HISTORICA",
    )
    assert "ELO-AI-004-HISTORICAL-AS-CURRENT" in _codes(findings)


def test_theoretical_pcp_capacity_is_not_promoted_to_realized_current():
    findings = guard_capacity_claim(
        subject="corte_dobra_modulos_dia",
        state=RequirementState.CALCULATED,
        capacity_kind="TEORICA",
    )
    assert "ELO-AI-005-THEORETICAL-AS-REALIZED" in _codes(findings)


def test_current_capacity_does_not_trigger_temporality_blocks():
    findings = guard_capacity_claim(
        subject="montagem_modulos_dia",
        state=RequirementState.DOCUMENTED,
        capacity_kind="ATUAL",
    )
    assert not _codes(findings) & {
        "ELO-AI-004-HISTORICAL-AS-CURRENT",
        "ELO-AI-005-THEORETICAL-AS-REALIZED",
    }


def test_mrp_evidence_does_not_authorize_purchase():
    findings = guard_pcp_action_authorization(
        subject="emitir_compra_pir40",
        state=RequirementState.CALCULATED,
        source_role=SourceRole.EVIDENCE,
    )
    assert "ELO-AI-006-EVIDENCE-AS-AUTHORIZATION" in _codes(findings)
