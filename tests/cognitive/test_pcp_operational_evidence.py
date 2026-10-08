from elo.cognitive.pcp_confrontation import confront
from elo.cognitive.pcp_operational_evidence import build_operational_evidence_package


def test_operational_evidence_package_composes_domain_facts():
    package = build_operational_evidence_package((
        confront(
            dimension="CAPACIDADE", key="C1",
            planned=100, actual=90, variance=-10,
            evidence_ids=("E1",),
        ),
        confront(
            dimension="MATERIAL", key="M1",
            planned=50, actual=None,
            evidence_ids=("E2",),
        ),
    ), source_kind="SUPABASE", source_ref="pcp-test")
    assert len(package.confrontations) == 2
    assert package.diagnosis.status == "DADOS_INCOMPLETOS"
    assert package.evidence_ids == ("E1", "E2")
    assert package.source_kind == "SUPABASE"


def test_package_does_not_invent_evidence():
    package = build_operational_evidence_package((
        confront(
            dimension="PRAZO", key="P1",
            planned="2026-09-10", actual="2026-09-12",
        ),
    ), source_kind="SUPABASE")
    assert package.evidence_ids == ()
