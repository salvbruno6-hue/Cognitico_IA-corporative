from elo.cognitive.operational_capacity_evidence_matrix import (
    CapacityEvidenceRow,
    CapacityMatrixState,
    OperationalEvidence,
    build_capacity_evidence_matrix_row,
    summarize_capacity_evidence_matrix,
)

STAGES = ("CHASSI", "ESCOVACAO", "PINTURA_TRATAMENTO", "PINTURA_MODULAR", "ACABAMENTO", "INSTALACOES", "TESTES")
SHEET = "google-sheets:PcP Multiteiner/17_CAPACIDADE!A2:K9"


def cap(cid: str, unit: str, stages: tuple[str, ...]) -> CapacityEvidenceRow:
    return CapacityEvidenceRow(cid, cid, 6.0, unit, stages, SHEET)


def test_component_unit_blocks_before_sector_inference():
    row = build_capacity_evidence_matrix_row(
        cap("CAP-001", "colunas/dia", ("ESCOVACAO",)),
        canonical_stage_codes=STAGES,
        operational_evidence=(),
    )
    assert row.state is CapacityMatrixState.NEEDS_UNIT_MODEL
    assert row.canonical_stage == "ESCOVACAO"
    assert row.canonical_mutation is False


def test_partially_mapped_repair_remains_blocked():
    row = build_capacity_evidence_matrix_row(
        cap("CAP-007", "módulos/dia", ("TESTES", "REPARO")),
        canonical_stage_codes=STAGES,
        operational_evidence=(),
    )
    assert row.state is CapacityMatrixState.NEEDS_STAGE_MAPPING
    assert row.canonical_stage is None


def test_real_sector_evidence_still_requires_canonical_work_center():
    row = build_capacity_evidence_matrix_row(
        cap("CAP-006", "estruturas/dia", ("CHASSI",)),
        canonical_stage_codes=STAGES,
        operational_evidence=(
            OperationalEvidence("SOLDA", ("CHASSI",), "supabase:mt_mao_obra_solda_preparacao_estrutura_modular", 2),
        ),
    )
    assert row.state is CapacityMatrixState.NEEDS_WORK_CENTER
    assert row.observed_sector == "SOLDA"
    assert row.confidence > 0.5


def test_multiple_real_sectors_are_not_arbitrated_by_inference():
    row = build_capacity_evidence_matrix_row(
        cap("CAP-006", "estruturas/dia", ("CHASSI",)),
        canonical_stage_codes=STAGES,
        operational_evidence=(
            OperationalEvidence("SOLDA", ("CHASSI",), "supabase:solda", 2),
            OperationalEvidence("PREPARACAO", ("CHASSI",), "supabase:preparacao", 1),
        ),
    )
    assert row.state is CapacityMatrixState.AMBIGUOUS_OPERATIONAL_SECTOR
    assert row.observed_sector is None


def test_simulated_resource_is_excluded_from_operational_authority():
    row = build_capacity_evidence_matrix_row(
        cap("CAP-005", "módulos/dia", ("ACABAMENTO",)),
        canonical_stage_codes=STAGES,
        operational_evidence=(
            OperationalEvidence("REC-001", ("ACABAMENTO",), "supabase:elo_sim_recursos", 1, simulated=True),
        ),
    )
    assert row.state is CapacityMatrixState.NEEDS_OPERATIONAL_EVIDENCE


def test_ready_for_proposal_requires_stage_sector_and_center():
    row = build_capacity_evidence_matrix_row(
        cap("CAP-ELE", "módulos/dia", ("INSTALACOES",)),
        canonical_stage_codes=STAGES,
        operational_evidence=(
            OperationalEvidence("ELÉTRICA", ("INSTALACOES",), "supabase:mt_mao_obra_kit_eletrico_m01", 1),
        ),
        stage_work_centers={"INSTALACOES": "CT-ELETRICA"},
    )
    assert row.state is CapacityMatrixState.READY_FOR_PROPOSAL
    assert row.work_center_ref == "CT-ELETRICA"
    assert row.canonical_mutation is False


def test_summary_never_authorizes_mutation():
    rows = (
        build_capacity_evidence_matrix_row(
            cap("CAP-005", "módulos/dia", ("ACABAMENTO",)),
            canonical_stage_codes=STAGES,
            operational_evidence=(),
        ),
    )
    summary = summarize_capacity_evidence_matrix(rows)
    assert summary["total"] == 1
    assert summary["canonical_mutation"] is False
