from elo.cognitive.reasoning.analytical_integrity import (
    BehavioralExpectation,
    EvidenceUse,
    EvidenceUsage,
    SourceRole,
    Temporality,
    assess_behavioral_conformance,
    assess_evidence_usage,
)
from elo.cognitive.reasoning.requirement_analysis import RequirementState


def _codes(usage: EvidenceUsage) -> set[str]:
    return {finding.code for finding in assess_evidence_usage(usage)}


def test_missing_evidence_cannot_be_promoted_to_current_fact():
    usage = EvidenceUsage(
        subject="estoque",
        state=RequirementState.MISSING,
        use=EvidenceUse.CURRENT_STATE_CLAIM,
    )
    assert "ELO-AI-001-UNRESOLVED-AS-FACT" in _codes(usage)


def test_inference_requires_explicit_label():
    usage = EvidenceUsage(
        subject="causa_atraso",
        state=RequirementState.INFERRED,
        use=EvidenceUse.DECISION_RECOMMENDATION,
        explicit_label=False,
    )
    assert "ELO-AI-002-UNLABELED-INFERENCE" in _codes(usage)


def test_labeled_inference_is_not_blocked_by_label_rule():
    usage = EvidenceUsage(
        subject="causa_atraso",
        state=RequirementState.INFERRED,
        use=EvidenceUse.ANALYSIS,
        explicit_label=True,
    )
    assert "ELO-AI-002-UNLABELED-INFERENCE" not in _codes(usage)


def test_conflict_must_remain_unresolved_outside_analysis():
    usage = EvidenceUsage(
        subject="capacidade",
        state=RequirementState.CONFLICT,
        use=EvidenceUse.CURRENT_STATE_CLAIM,
    )
    assert "ELO-AI-003-CONFLICT-SILENTLY-RESOLVED" in _codes(usage)


def test_historical_capacity_cannot_be_current_capacity():
    usage = EvidenceUsage(
        subject="fibra_modulos_dia",
        state=RequirementState.KNOWN,
        use=EvidenceUse.CURRENT_STATE_CLAIM,
        temporality=Temporality.HISTORICAL,
    )
    assert "ELO-AI-004-HISTORICAL-AS-CURRENT" in _codes(usage)


def test_theoretical_capacity_cannot_be_realized_capacity():
    usage = EvidenceUsage(
        subject="corte_dobra_modulos_dia",
        state=RequirementState.CALCULATED,
        use=EvidenceUse.CURRENT_STATE_CLAIM,
        temporality=Temporality.THEORETICAL,
    )
    assert "ELO-AI-005-THEORETICAL-AS-REALIZED" in _codes(usage)


def test_evidence_source_cannot_grant_action_authorization():
    usage = EvidenceUsage(
        subject="emitir_compra",
        state=RequirementState.DOCUMENTED,
        use=EvidenceUse.ACTION_AUTHORIZATION,
        source_role=SourceRole.EVIDENCE,
    )
    assert "ELO-AI-006-EVIDENCE-AS-AUTHORIZATION" in _codes(usage)


def test_authority_source_may_pass_authorization_boundary_check():
    usage = EvidenceUsage(
        subject="acao_autorizada",
        state=RequirementState.KNOWN,
        use=EvidenceUse.ACTION_AUTHORIZATION,
        source_role=SourceRole.AUTHORITY,
    )
    assert "ELO-AI-006-EVIDENCE-AS-AUTHORIZATION" not in _codes(usage)


def test_behavioral_conformance_detects_declared_vs_observed_divergence():
    result = assess_behavioral_conformance((
        BehavioralExpectation("historical-not-current", expected=True, observed=False, evidence_ids=("ev-1",)),
        BehavioralExpectation("preserve-conflict", expected=True, observed=True, evidence_ids=("ev-2",)),
    ))
    assert result[0].status == "DIVERGENT"
    assert result[0].evidence_ids == ("ev-1",)
    assert result[1].status == "CONFORMANT"
