from elo.cognitive.partial_route_evidence import (
    OrderedOperationEvidence,
    PartialRouteState,
    RouteFragmentLink,
    assess_partial_route,
)


def op(fragment, sequence, operation, source="supabase:evidence"):
    return OrderedOperationEvidence(
        fragment_id=fragment,
        stage_code="CHASSI",
        sector=fragment,
        sequence=sequence,
        operation=operation,
        source_ref=source,
    )


def test_independent_ordered_fragments_preserve_local_order_but_not_global_order():
    assessment = assess_partial_route(
        stage_code="CHASSI",
        operations=(
            op("CORTE_COLUNAS", 1, "CORTE EM GUILHOTINA"),
            op("CORTE_COLUNAS", 2, "CORTE PLASMA CNC"),
            op("CORTE_COLUNAS", 3, "DOBRA EM VIRADEIRA"),
            op("SOLDA_PREPARACAO", 1, "SOLDA TETO"),
            op("SOLDA_PREPARACAO", 2, "SOLDA FUNDO"),
            op("SOLDA_PREPARACAO", 3, "PREPARACAO DE PECAS E FUROS"),
        ),
    )

    assert assessment.state is PartialRouteState.CROSS_FRAGMENT_ORDER_UNPROVEN
    assert assessment.unresolved_fragment_pairs == (("CORTE_COLUNAS", "SOLDA_PREPARACAO"),)
    assert assessment.next_required_condition == "complete_acyclic_cross_fragment_precedence"
    assert assessment.canonical_mutation is False


def test_explicit_cross_fragment_precedence_can_form_route_proposal():
    assessment = assess_partial_route(
        stage_code="CHASSI",
        operations=(
            op("CORTE", 1, "CORTAR"),
            op("CORTE", 2, "DOBRAR"),
            op("PREPARAR", 1, "PREPARAR"),
            op("SOLDAR", 1, "SOLDAR"),
        ),
        fragment_links=(
            RouteFragmentLink("CORTE", "PREPARAR", "source:precedence-1"),
            RouteFragmentLink("PREPARAR", "SOLDAR", "source:precedence-2"),
        ),
    )

    assert assessment.state is PartialRouteState.READY_FOR_ROUTE_PROPOSAL
    assert tuple(item[0] for item in assessment.ordered_fragments) == (
        "CORTE",
        "PREPARAR",
        "SOLDAR",
    )
    assert assessment.canonical_mutation is False


def test_partial_links_do_not_fake_complete_global_order():
    assessment = assess_partial_route(
        stage_code="CHASSI",
        operations=(op("A", 1, "A"), op("B", 1, "B"), op("C", 1, "C")),
        fragment_links=(RouteFragmentLink("A", "B", "source:a-b"),),
    )
    assert assessment.state is PartialRouteState.CROSS_FRAGMENT_ORDER_UNPROVEN
    assert ("A", "C") in assessment.unresolved_fragment_pairs
    assert ("B", "C") in assessment.unresolved_fragment_pairs


def test_cycle_never_becomes_route_proposal():
    assessment = assess_partial_route(
        stage_code="CHASSI",
        operations=(op("A", 1, "A"), op("B", 1, "B")),
        fragment_links=(
            RouteFragmentLink("A", "B", "source:a-b"),
            RouteFragmentLink("B", "A", "source:b-a"),
        ),
    )
    assert assessment.state is PartialRouteState.CROSS_FRAGMENT_ORDER_UNPROVEN


def test_duplicate_sequence_within_fragment_fails_closed():
    assessment = assess_partial_route(
        stage_code="CHASSI",
        operations=(op("CORTE", 1, "A"), op("CORTE", 1, "B")),
    )
    assert assessment.state is PartialRouteState.INVALID_FRAGMENT_ORDER


def test_operations_from_other_stage_do_not_supply_chassi_evidence():
    assessment = assess_partial_route(
        stage_code="CHASSI",
        operations=(
            OrderedOperationEvidence("X", "ACABAMENTO", "X", 1, "A", "source:x"),
            OrderedOperationEvidence("X", "ACABAMENTO", "X", 2, "B", "source:x"),
        ),
    )
    assert assessment.state is PartialRouteState.INSUFFICIENT_ORDER_EVIDENCE
