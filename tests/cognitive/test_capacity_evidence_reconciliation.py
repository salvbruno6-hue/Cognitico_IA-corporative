from math import inf, nan

from elo.cognitive.capacity_evidence_reconciliation import (
    CapacityReconciliationState,
    EmpiricalCapacityEvidence,
    reconcile_capacity_evidence,
    summarize_capacity_reconciliation,
)


CANONICAL_STAGES = (
    "TRIAGEM",
    "CHASSI",
    "ESCOVACAO",
    "PINTURA_TRATAMENTO",
    "ACABAMENTO_BRANCO",
    "ESTOQUE_ESTRUTURAS",
    "MOVIMENTACAO",
    "PISO",
    "TETO",
    "COLUNAS",
    "TRILHO",
    "PINTURA_MODULAR",
    "PAREDES",
    "INSTALACOES",
    "ACABAMENTO",
    "TESTES",
    "LIBERACAO",
)
SOURCE = "google-sheets:PcP Multiteiner/17_CAPACIDADE!A2:K9"


def ev(evidence_id: str, unit: str, stages: tuple[str, ...]) -> EmpiricalCapacityEvidence:
    return EmpiricalCapacityEvidence(
        evidence_id=evidence_id,
        activity=evidence_id,
        quantity_per_day=6,
        unit=unit,
        stage_codes=stages,
        source_ref=SOURCE,
    )


def test_component_level_capacity_requires_conversion_instead_of_inventing_modules():
    result = reconcile_capacity_evidence(
        ev("CAP-001", "colunas/dia", ("ESCOVACAO",)),
        canonical_stage_codes=CANONICAL_STAGES,
    )

    assert result.state is CapacityReconciliationState.NEEDS_UNIT_CONVERSION
    assert result.matched_stage == "ESCOVACAO"
    assert result.next_required_condition == "governed_unit_conversion_or_component_model"
    assert result.canonical_mutation is False


def test_direct_module_capacity_still_requires_stage_work_center_before_persistence():
    result = reconcile_capacity_evidence(
        ev("CAP-005", "módulos/dia", ("ACABAMENTO",)),
        canonical_stage_codes=CANONICAL_STAGES,
        stage_work_centers={},
    )

    assert result.state is CapacityReconciliationState.NEEDS_WORK_CENTER
    assert result.matched_stage == "ACABAMENTO"
    assert result.canonical_unit == "MODULOS_DIA"
    assert result.next_required_condition == "canonical_stage_work_center"


def test_unrelated_work_center_does_not_make_capacity_ready():
    result = reconcile_capacity_evidence(
        ev("CAP-005", "módulos/dia", ("ACABAMENTO",)),
        canonical_stage_codes=CANONICAL_STAGES,
        stage_work_centers={"CHASSI": "CT-ESTRUTURA"},
    )

    assert result.state is CapacityReconciliationState.NEEDS_WORK_CENTER
    assert result.work_center_ref is None


def test_partially_mapped_repair_semantics_remain_blocked():
    result = reconcile_capacity_evidence(
        ev("CAP-007", "módulos/dia", ("TESTES", "REPARO")),
        canonical_stage_codes=CANONICAL_STAGES,
        stage_work_centers={"TESTES": "CT-QUALIDADE"},
    )

    assert result.state is CapacityReconciliationState.NEEDS_STAGE_MAPPING
    assert result.matched_stage == "TESTES"
    assert result.next_required_condition == "canonical_stage_mapping"
    assert "REPARO" in result.detail
    assert result.canonical_mutation is False


def test_multiple_real_canonical_stage_matches_are_ambiguous():
    result = reconcile_capacity_evidence(
        ev("CAP-X", "módulos/dia", ("ACABAMENTO", "TESTES")),
        canonical_stage_codes=CANONICAL_STAGES,
    )

    assert result.state is CapacityReconciliationState.AMBIGUOUS_STAGE
    assert result.next_required_condition == "single_canonical_stage"


def test_ready_only_after_stage_unit_and_stage_work_center_are_explicit():
    result = reconcile_capacity_evidence(
        ev("CAP-005", "módulos/dia", ("ACABAMENTO",)),
        canonical_stage_codes=CANONICAL_STAGES,
        stage_work_centers={"ACABAMENTO": "CT-MONTAGEM-FINAL"},
    )

    assert result.state is CapacityReconciliationState.READY_FOR_CANONICALIZATION
    assert result.work_center_ref == "CT-MONTAGEM-FINAL"
    assert result.next_required_condition is None
    assert result.canonical_mutation is False


def test_summary_exposes_next_semantic_conditions_without_mutation():
    results = (
        reconcile_capacity_evidence(
            ev("CAP-001", "colunas/dia", ("ESCOVACAO",)),
            canonical_stage_codes=CANONICAL_STAGES,
        ),
        reconcile_capacity_evidence(
            ev("CAP-005", "módulos/dia", ("ACABAMENTO",)),
            canonical_stage_codes=CANONICAL_STAGES,
        ),
    )

    summary = summarize_capacity_reconciliation(results)
    assert summary["total"] == 2
    assert summary["counts"]["NEEDS_UNIT_CONVERSION"] == 1
    assert summary["counts"]["NEEDS_WORK_CENTER"] == 1
    assert summary["canonical_mutation"] is False


def test_non_positive_empirical_capacity_fails_closed():
    try:
        EmpiricalCapacityEvidence(
            evidence_id="CAP-NEG",
            activity="invalid",
            quantity_per_day=0,
            unit="módulos/dia",
            stage_codes=("ACABAMENTO",),
            source_ref=SOURCE,
        )
    except ValueError as exc:
        assert "finite number greater than zero" in str(exc)
    else:
        raise AssertionError("non-positive capacity must fail closed")


def test_non_finite_empirical_capacity_fails_closed():
    for value in (nan, inf):
        try:
            EmpiricalCapacityEvidence(
                evidence_id="CAP-NON-FINITE",
                activity="invalid",
                quantity_per_day=value,
                unit="módulos/dia",
                stage_codes=("ACABAMENTO",),
                source_ref=SOURCE,
            )
        except ValueError as exc:
            assert "finite number greater than zero" in str(exc)
        else:
            raise AssertionError("non-finite capacity must fail closed")
