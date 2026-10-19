from elo.cognitive.work_center_evidence import (
    OperationalSectorEvidence,
    WorkCenterEvidenceState,
    assess_work_center_evidence,
    summarize_work_center_evidence,
)


STAGES = (
    "CHASSI",
    "ESCOVACAO",
    "PINTURA_TRATAMENTO",
    "PINTURA_MODULAR",
    "INSTALACOES",
    "ACABAMENTO",
    "TESTES",
)


def test_real_sector_with_explicit_stage_is_candidate_not_mutation():
    assessment = assess_work_center_evidence(
        OperationalSectorEvidence(
            sector="ELÉTRICA",
            source_ref="supabase:mt_mao_obra_kit_eletrico_m01",
            observation_count=1,
            canonical_stage_codes=("INSTALACOES",),
            production_per_shift=4,
            shift_minutes=540,
        ),
        active_stage_codes=STAGES,
    )

    assert assessment.state is WorkCenterEvidenceState.OBSERVED_CANDIDATE
    assert assessment.matched_stage == "INSTALACOES"
    assert assessment.next_required_condition == "governed_work_center_registration"
    assert assessment.canonical_mutation is False


def test_real_sector_without_explicit_stage_mapping_remains_review_candidate():
    assessment = assess_work_center_evidence(
        OperationalSectorEvidence(
            sector="CORTE E DOBRA",
            source_ref="supabase:mt_tempo_fabricacao_estrutura_modular",
            observation_count=9,
        ),
        active_stage_codes=STAGES,
    )

    assert assessment.state is WorkCenterEvidenceState.NEEDS_STAGE_MAPPING
    assert assessment.next_required_condition == "governed_stage_mapping"
    assert assessment.evidence_strength == 0.5


def test_simulated_resource_is_rejected_as_canonical_evidence():
    assessment = assess_work_center_evidence(
        OperationalSectorEvidence(
            sector="REC-001",
            source_ref="supabase:elo_sim_recursos",
            observation_count=1,
            canonical_stage_codes=("CHASSI",),
            simulated=True,
        ),
        active_stage_codes=STAGES,
    )

    assert assessment.state is WorkCenterEvidenceState.REJECT_SIMULATED
    assert assessment.evidence_strength == 0
    assert assessment.canonical_mutation is False


def test_partial_or_unknown_stage_mapping_does_not_become_candidate():
    assessment = assess_work_center_evidence(
        OperationalSectorEvidence(
            sector="SOLDA",
            source_ref="supabase:mt_mao_obra_solda_preparacao_estrutura_modular",
            observation_count=2,
            canonical_stage_codes=("CHASSI", "SOLDA_TETO"),
            production_per_shift=2,
            shift_minutes=540,
        ),
        active_stage_codes=STAGES,
    )

    assert assessment.state is WorkCenterEvidenceState.NEEDS_STAGE_MAPPING
    assert assessment.matched_stage == "CHASSI"
    assert "SOLDA_TETO" in assessment.detail


def test_zero_observation_cannot_create_candidate():
    assessment = assess_work_center_evidence(
        OperationalSectorEvidence(
            sector="PINTURA",
            source_ref="test:no-observations",
            observation_count=0,
            canonical_stage_codes=("PINTURA_TRATAMENTO",),
        ),
        active_stage_codes=STAGES,
    )

    assert assessment.state is WorkCenterEvidenceState.INSUFFICIENT_EVIDENCE


def test_summary_separates_candidates_from_unresolved_evidence():
    assessments = (
        assess_work_center_evidence(
            OperationalSectorEvidence(
                sector="ELÉTRICA",
                source_ref="supabase:mt_mao_obra_kit_eletrico_m01",
                observation_count=1,
                canonical_stage_codes=("INSTALACOES",),
                production_per_shift=4,
                shift_minutes=540,
            ),
            active_stage_codes=STAGES,
        ),
        assess_work_center_evidence(
            OperationalSectorEvidence(
                sector="CORTE E DOBRA",
                source_ref="supabase:mt_tempo_fabricacao_estrutura_modular",
                observation_count=9,
            ),
            active_stage_codes=STAGES,
        ),
    )

    summary = summarize_work_center_evidence(assessments)
    assert summary["counts"]["OBSERVED_CANDIDATE"] == 1
    assert summary["counts"]["NEEDS_STAGE_MAPPING"] == 1
    assert summary["candidate_sectors"] == ("ELÉTRICA",)
    assert summary["canonical_mutation"] is False
