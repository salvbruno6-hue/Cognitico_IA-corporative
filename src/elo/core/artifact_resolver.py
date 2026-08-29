"""Canonical documentary artifact resolution for ELO.

This resolver maps stable ``artifact_id``/``concept_id`` identities to the
canonical documentary path while accepting explicitly registered legacy paths
as compatibility aliases. It does not mutate the canonical registry and does
not create a second source resolver.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any, Mapping


@dataclass(frozen=True)
class ArtifactRecord:
    artifact_id: str
    concept_id: str
    canonical_path: str
    legacy_paths: tuple[str, ...] = ()
    classification: str = ""
    authority: str = ""
    language: str = ""


@dataclass(frozen=True)
class ArtifactResolution:
    record: ArtifactRecord
    requested: str
    matched_by: str
    resolved_path: str
    is_legacy_alias: bool


class ArtifactResolutionError(ValueError):
    """Base error for invalid documentary artifact resolution."""


class UnknownArtifactError(ArtifactResolutionError):
    """Raised when neither an identity nor a registered path is known."""


class AmbiguousArtifactError(ArtifactResolutionError):
    """Raised when a lookup could map to multiple documentary artifacts."""


class ArtifactResolver:
    """Resolve documentary artifacts by stable identity or registered path.

    The resolver is deliberately independent from ``SourceResolver``. It
    resolves documentary addresses; ``SourceResolver`` remains responsible
    for governed external source retrieval and authorization.
    """

    def __init__(self, records: tuple[ArtifactRecord, ...]) -> None:
        self._records = tuple(records)
        self._by_artifact_id: dict[str, ArtifactRecord] = {}
        self._by_concept_id: dict[str, ArtifactRecord] = {}
        self._by_path: dict[str, ArtifactRecord] = {}

        for record in self._records:
            self._register(self._by_artifact_id, record.artifact_id, record)
            self._register(self._by_concept_id, record.concept_id, record)
            self._register_path(record.canonical_path, record)
            for path in record.legacy_paths:
                self._register_path(path, record)

    @classmethod
    def from_registry(cls, payload: Mapping[str, Any]) -> "ArtifactResolver":
        records = tuple(
            ArtifactRecord(
                artifact_id=str(item["artifact_id"]),
                concept_id=str(item["concept_id"]),
                canonical_path=_normalise_path(str(item["canonical_path"])),
                legacy_paths=tuple(
                    _normalise_path(str(path)) for path in item.get("legacy_paths", ())
                ),
                classification=str(item.get("classification", "")),
                authority=str(item.get("authority", "")),
                language=str(item.get("language", "")),
            )
            for item in payload.get("records", ())
        )
        return cls(records)

    def resolve(self, identifier: str) -> ArtifactResolution:
        key = _normalise_identifier(identifier)
        if not key:
            raise UnknownArtifactError("artifact identifier/path is required")

        record = self._by_artifact_id.get(key)
        if record is not None:
            return ArtifactResolution(record, identifier, "artifact_id", record.canonical_path, False)

        record = self._by_concept_id.get(key)
        if record is not None:
            return ArtifactResolution(record, identifier, "concept_id", record.canonical_path, False)

        record = self._by_path.get(_normalise_path(key))
        if record is not None:
            legacy = _normalise_path(key) in record.legacy_paths
            return ArtifactResolution(record, identifier, "legacy_path" if legacy else "canonical_path", record.canonical_path, legacy)

        raise UnknownArtifactError(f"unknown ELO documentary artifact: {identifier}")

    def canonical_path(self, identifier: str) -> str:
        return self.resolve(identifier).resolved_path

    def records(self) -> tuple[ArtifactRecord, ...]:
        return self._records

    @staticmethod
    def _register(index: dict[str, ArtifactRecord], key: str, record: ArtifactRecord) -> None:
        if key in index and index[key] != record:
            raise AmbiguousArtifactError(f"duplicate documentary identity: {key}")
        index[key] = record

    def _register_path(self, path: str, record: ArtifactRecord) -> None:
        path = _normalise_path(path)
        if path in self._by_path and self._by_path[path] != record:
            raise AmbiguousArtifactError(f"path mapped to multiple artifacts: {path}")
        self._by_path[path] = record


def _normalise_path(path: str) -> str:
    value = path.strip().replace("\\", "/")
    if not value:
        return ""
    return str(PurePosixPath(value))


def _normalise_identifier(value: str) -> str:
    return value.strip()
