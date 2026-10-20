from src.elo.core.resource_registry_builder import build_registry


def test_build_registry_indexes_repository_directories_and_database_addresses():
    result = build_registry(
        repository_files=["docs/A.md", "docs/sub/B.md", "docs/A.md", "src/x.py"],
        database_tables=["excedentes", "lista_mae"],
        database_views=["vw_excedentes_com_lista_mae"],
    )

    by_address = {item["physical_address"]: item for item in result["records"]}

    assert by_address["docs"]["resource_type"] == "repository_directory"
    assert by_address["docs/sub"]["resource_type"] == "repository_directory"
    assert by_address["docs/A.md"]["provider"] == "github"
    assert by_address["public.excedentes"]["resource_type"] == "database_table"
    assert by_address["public.excedentes"]["aliases"] == [
        "tabela excedente",
        "tabela excedentes",
        "excedente",
    ]
    assert by_address["public.vw_excedentes_com_lista_mae"]["resource_type"] == "database_view"


def test_registry_is_deterministic():
    first = build_registry(repository_files=["b.md", "a.md"], database_tables=["z", "a"])
    second = build_registry(repository_files=["a.md", "b.md"], database_tables=["a", "z"])

    assert first == second



def test_canonical_artifact_keeps_stable_identity_and_avoids_duplicate_path():
    result = build_registry(
        repository_files=["01-meta-architecture/ELO_ARCHITECTURE_MASTER.md"],
        canonical_artifacts=[{
            "artifact_id": "ELO.ARCH.01.MASTER",
            "concept_id": "ELO.ARCHITECTURE.MASTER",
            "canonical_path": "01-meta-architecture/ELO_ARCHITECTURE_MASTER.md",
            "legacy_paths": ["01-meta-arquitetura/ELO_ARCHITECTURE_MASTER.md"],
            "authority": "ARCHITECTURE",
        }],
    )

    matches = [
        item for item in result["records"]
        if item["physical_address"] == "01-meta-architecture/ELO_ARCHITECTURE_MASTER.md"
    ]
    assert len(matches) == 1
    assert matches[0]["resource_id"] == "ELO.ARCH.01.MASTER"
    assert matches[0]["resource_type"] == "governed_document"
    assert "01-meta-arquitetura/ELO_ARCHITECTURE_MASTER.md" in matches[0]["aliases"]
