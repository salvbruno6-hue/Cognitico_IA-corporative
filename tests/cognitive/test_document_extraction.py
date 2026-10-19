from elo.cognitive.reasoning.document_extraction import (
    extract_documented_requirements,
    iter_claims,
    normalize_key,
    parse_explicit_requirement,
    split_text_segments,
)
from elo.cognitive.reasoning.requirement_analysis import (
    RequirementSourceType,
    RequirementState,
    audit_requirement,
)


def test_split_text_segments_preserves_line_locator_and_text():
    segments = split_text_segments(
        source_reference="SO-203.26",
        text="Tipo: 40 HC\n\nPiso: vinílico\n",
    )

    assert [segment.locator for segment in segments] == ["line:1", "line:3"]
    assert segments[0].text == "Tipo: 40 HC"
    assert segments[1].text == "Piso: vinílico"


def test_explicit_key_value_becomes_documented_claim_with_document_provenance():
    nodes = extract_documented_requirements(
        source_reference="SO-203.26",
        text="Container: 40 HC",
        requirement_prefix="SO-203.26",
        subject="container",
        evidence_ids=("document-evidence",),
    )

    assert len(nodes) == 1
    claim = nodes[0].claims[0]
    assert claim.state is RequirementState.DOCUMENTED
    assert claim.provenance.source_type is RequirementSourceType.DOCUMENT
    assert claim.provenance.source_reference == "SO-203.26#line:1"
    assert claim.value == "40 HC"
    assert nodes[0].text == "Container: 40 HC"


def test_bullet_key_value_is_supported_without_interpreting_value():
    nodes = extract_documented_requirements(
        source_reference="SO-203.26",
        text="- MDF espessura: 18 mm nominal",
        requirement_prefix="SO-203.26",
        subject="interior",
    )

    claim = nodes[0].claims[0]
    assert claim.predicate == "mdf.espessura"
    assert claim.value == "18 mm nominal"


def test_ambiguous_prose_does_not_create_documented_fact():
    nodes = extract_documented_requirements(
        source_reference="SO-203.26",
        text="O container deverá ser adequado ao uso e receber acabamento conforme projeto.",
        requirement_prefix="SO-203.26",
        subject="container",
    )

    assert nodes == ()


def test_no_inference_is_introduced_for_missing_technical_parameter():
    nodes = extract_documented_requirements(
        source_reference="SO-203.26",
        text="Janela quantidade: 2",
        requirement_prefix="SO-203.26",
        subject="container",
    )

    claims = iter_claims(nodes)
    assert len(claims) == 1
    assert claims[0].predicate == "janela.quantidade"
    assert all(claim.state is RequirementState.DOCUMENTED for claim in claims)
    assert all(claim.predicate != "janela.reforco" for claim in claims)


def test_same_input_is_idempotent_and_stable():
    kwargs = dict(
        source_reference="SO-203.26",
        text="Tipo: 40 HC\nPiso: vinílico",
        requirement_prefix="SO-203.26",
        subject="container",
    )
    first = extract_documented_requirements(**kwargs)
    second = extract_documented_requirements(**kwargs)

    assert first == second
    assert [node.metadata["origin_hash"] for node in first] == [
        node.metadata["origin_hash"] for node in second
    ]


def test_duplicate_identical_lines_at_distinct_locations_remain_distinct_evidence():
    nodes = extract_documented_requirements(
        source_reference="SO-203.26",
        text="Piso: vinílico\nPiso: vinílico",
        requirement_prefix="SO-203.26",
        subject="container",
    )

    assert len(nodes) == 2
    assert nodes[0].metadata["locator"] == "line:1"
    assert nodes[1].metadata["locator"] == "line:2"
    assert nodes[0].metadata["origin_hash"] != nodes[1].metadata["origin_hash"]


def test_normalize_key_changes_only_key_shape():
    assert normalize_key("  Porta Metálica / Tipo ") == "porta.met.lica.tipo"


def test_extraction_output_is_auditable_by_existing_contract():
    node = extract_documented_requirements(
        source_reference="SO-203.26",
        text="Piso: vinílico",
        requirement_prefix="SO-203.26",
        subject="container",
        evidence_ids=("doc-1",),
    )[0]

    trace = audit_requirement(node)
    assert trace["requirement_id"] == "SO-203.26:R1"
    assert trace["source_claims"][0]["state"] == "DOCUMENTED"
    assert trace["source_claims"][0]["source_reference"] == "SO-203.26#line:1"
    assert trace["evidence_ids"] == ("doc-1",)


def test_parse_explicit_requirement_returns_none_without_colon_contract():
    segment = split_text_segments(source_reference="fixture", text="apenas texto livre")[0]
    assert parse_explicit_requirement(segment) is None
