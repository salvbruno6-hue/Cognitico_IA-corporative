import pytest

from elo.core.artifact_resolver import (
    AmbiguousArtifactError,
    ArtifactRecord,
    ArtifactResolver,
    UnknownArtifactError,
)


RECORDS = (
    ArtifactRecord(
        artifact_id="ELO.ARCH.01.MASTER",
        concept_id="ELO.ARCHITECTURE.MASTER",
        canonical_path="01-meta-architecture/ELO_ARCHITECTURE_MASTER.md",
        legacy_paths=("01-meta-arquitetura/ELO_ARCHITECTURE_MASTER.md",),
        authority="ARCHITECTURE",
    ),
)


def test_resolve_by_artifact_id_returns_canonical_path():
    result = ArtifactResolver(RECORDS).resolve("ELO.ARCH.01.MASTER")

    assert result.matched_by == "artifact_id"
    assert result.resolved_path == "01-meta-architecture/ELO_ARCHITECTURE_MASTER.md"
    assert result.is_legacy_alias is False


def test_resolve_by_legacy_path_returns_same_canonical_identity():
    result = ArtifactResolver(RECORDS).resolve("01-meta-arquitetura/ELO_ARCHITECTURE_MASTER.md")

    assert result.matched_by == "legacy_path"
    assert result.record.concept_id == "ELO.ARCHITECTURE.MASTER"
    assert result.resolved_path == "01-meta-architecture/ELO_ARCHITECTURE_MASTER.md"
    assert result.is_legacy_alias is True


def test_resolve_by_concept_id_returns_canonical_path():
    result = ArtifactResolver(RECORDS).resolve("ELO.ARCHITECTURE.MASTER")

    assert result.matched_by == "concept_id"
    assert result.is_legacy_alias is False


def test_unknown_identifier_is_explicit():
    with pytest.raises(UnknownArtifactError):
        ArtifactResolver(RECORDS).resolve("missing-artifact")


def test_duplicate_path_is_rejected_as_ambiguous():
    duplicate = ArtifactRecord(
        artifact_id="ELO.OTHER.01",
        concept_id="ELO.OTHER",
        canonical_path="01-meta-architecture/ELO_ARCHITECTURE_MASTER.md",
    )

    with pytest.raises(AmbiguousArtifactError):
        ArtifactResolver(RECORDS + (duplicate,))
