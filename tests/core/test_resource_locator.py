from src.elo.core.resource_locator import (
    AmbiguousResourceError,
    ResourceLocator,
    ResourceRecord,
    UnknownResourceError,
)


RECORDS = (
    ResourceRecord(
        resource_id="ELO.DB.TABLE.EXCEDENTES",
        resource_type="database_table",
        provider="supabase",
        logical_name="excedentes",
        physical_address="public.excedentes",
        scope="tenant",
        authority="ELO",
        provenance="Elo-forge",
    ),
    ResourceRecord(
        resource_id="ELO.ORCAMENTO.METODOLOGIA",
        resource_type="repository_file",
        provider="github",
        logical_name="metodologia de orçamento",
        physical_address="04-knowledge-handbook/MULTITEINER_METODOLOGIA_ORCAMENTO_ELO.md",
        aliases=("metodologia orçamento",),
        authority="CORE",
        provenance="Cognitico_IA-corporative",
    ),
)


def test_resolve_table_by_semantic_name():
    result = ResourceLocator(RECORDS).resolve("excedentes")

    assert result.matched_by == "logical_name"
    assert result.physical_address == "public.excedentes"


def test_resolve_file_by_stable_identity():
    result = ResourceLocator(RECORDS).resolve("ELO.ORCAMENTO.METODOLOGIA")

    assert result.matched_by == "resource_id"
    assert result.physical_address.endswith("MULTITEINER_METODOLOGIA_ORCAMENTO_ELO.md")


def test_alias_resolves_to_same_resource():
    result = ResourceLocator(RECORDS).resolve("metodologia orçamento")

    assert result.record.resource_id == "ELO.ORCAMENTO.METODOLOGIA"


def test_unknown_resource_is_blocked():
    try:
        ResourceLocator(RECORDS).resolve("nao-cadastrado")
    except UnknownResourceError:
        pass
    else:
        raise AssertionError("unknown resources must not be guessed")


def test_ambiguous_identity_is_rejected():
    try:
        ResourceLocator(
            RECORDS
            + (
                ResourceRecord(
                    resource_id="ELO.OTHER",
                    resource_type="database_table",
                    provider="supabase",
                    logical_name="excedentes",
                    physical_address="public.other",
                ),
            )
        )
    except AmbiguousResourceError:
        pass
    else:
        raise AssertionError("ambiguous resource names must be rejected")
