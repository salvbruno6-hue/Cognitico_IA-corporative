from elo.cognitive.composite_stage_routing import (
    CompositeSectorEvidence,
    CompositeStageRoutingState,
    assess_composite_stage_routing,
)


def sector(name: str, count: int, source: str, *stages: str) -> CompositeSectorEvidence:
    return CompositeSectorEvidence(name, count, source, tuple(stages))


def test_chassi_multiple_real_sectors_become_routing_proposal_not_single_center():
    assessment = assess_composite_stage_routing(
        stage_code="CHASSI",
        sector_evidence=(
            sector("CORTE E DOBRA", 9, "supabase:mt_tempo_fabricacao_estrutura_modular", "CHASSI"),
            sector("PREPARACAO", 1, "supabase:mt_mao_obra_solda_preparacao_estrutura_modular", "CHASSI"),
            sector("SOLDA", 2, "supabase:mt_mao_obra_solda_preparacao_estrutura_modular", "CHASSI"),
        ),
        aggregate_capacity_per_day=4,
        aggregate_capacity_unit="estruturas/dia",
        capacity_source_ref="google-sheets:PcP Multiteiner/17_CAPACIDADE!CAP-006",
        canonical_route_count=0,
    )

    assert assessment.state is CompositeStageRoutingState.READY_FOR_ROUTING_PROPOSAL
    assert assessment.constituent_sectors == ("CORTE E DOBRA", "PREPARACAO", "SOLDA")
    assert assessment.aggregate_capacity_per_day == 4
    assert assessment.next_required_condition == "governed_route_and_work_center_registration"
    assert assessment.canonical_mutation is False


def test_single_sector_does_not_prove_composite_stage():
    assessment = assess_composite_stage_routing(
        stage_code="CHASSI",
        sector_evidence=(sector("SOLDA", 2, "supabase:solda", "CHASSI"),),
        aggregate_capacity_per_day=4,
        aggregate_capacity_unit="estruturas/dia",
        capacity_source_ref="sheet:CAP-006",
    )
    assert assessment.state is CompositeStageRoutingState.NEEDS_STAGE_EVIDENCE


def test_unbound_or_wrong_stage_evidence_blocks_proposal():
    assessment = assess_composite_stage_routing(
        stage_code="CHASSI",
        sector_evidence=(
            sector("CORTE E DOBRA", 9, "supabase:corte", "CHASSI"),
            sector("SOLDA", 2, "supabase:solda", "TETO"),
        ),
        aggregate_capacity_per_day=4,
        aggregate_capacity_unit="estruturas/dia",
        capacity_source_ref="sheet:CAP-006",
    )
    assert assessment.state is CompositeStageRoutingState.NEEDS_STAGE_EVIDENCE
    assert assessment.constituent_sectors == ("CORTE E DOBRA",)


def test_multiple_sectors_without_aggregate_capacity_remain_incomplete():
    assessment = assess_composite_stage_routing(
        stage_code="CHASSI",
        sector_evidence=(
            sector("CORTE E DOBRA", 9, "supabase:corte", "CHASSI"),
            sector("SOLDA", 2, "supabase:solda", "CHASSI"),
        ),
        aggregate_capacity_per_day=None,
        aggregate_capacity_unit=None,
        capacity_source_ref=None,
    )
    assert assessment.state is CompositeStageRoutingState.NEEDS_CAPACITY_EVIDENCE
    assert assessment.canonical_mutation is False


def test_blank_capacity_provenance_remains_incomplete():
    assessment = assess_composite_stage_routing(
        stage_code="CHASSI",
        sector_evidence=(
            sector("CORTE E DOBRA", 9, "supabase:corte", "CHASSI"),
            sector("SOLDA", 2, "supabase:solda", "CHASSI"),
        ),
        aggregate_capacity_per_day=4,
        aggregate_capacity_unit="estruturas/dia",
        capacity_source_ref="   ",
    )
    assert assessment.state is CompositeStageRoutingState.NEEDS_CAPACITY_EVIDENCE
    assert "" not in assessment.evidence_refs


def test_existing_canonical_route_is_not_recreated():
    assessment = assess_composite_stage_routing(
        stage_code="CHASSI",
        sector_evidence=(
            sector("CORTE E DOBRA", 9, "supabase:corte", "CHASSI"),
            sector("SOLDA", 2, "supabase:solda", "CHASSI"),
        ),
        aggregate_capacity_per_day=4,
        aggregate_capacity_unit="estruturas/dia",
        capacity_source_ref="sheet:CAP-006",
        canonical_route_count=1,
    )
    assert assessment.state is CompositeStageRoutingState.CANONICAL_ROUTE_EXISTS
    assert assessment.canonical_mutation is False


def test_invalid_capacity_never_enters_proposal():
    try:
        assess_composite_stage_routing(
            stage_code="CHASSI",
            sector_evidence=(
                sector("CORTE E DOBRA", 9, "supabase:corte", "CHASSI"),
                sector("SOLDA", 2, "supabase:solda", "CHASSI"),
            ),
            aggregate_capacity_per_day=float("nan"),
            aggregate_capacity_unit="estruturas/dia",
            capacity_source_ref="sheet:CAP-006",
        )
    except ValueError as exc:
        assert "finite" in str(exc)
    else:
        raise AssertionError("non-finite capacity must fail closed")
