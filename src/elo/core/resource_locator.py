"""Fast, deterministic resolution of governed ELO resource addresses.

This locator is a navigation/index layer. It does not authorize access, read
resources, mutate canonical knowledge, or create learning.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any


class ResourceResolutionError(ValueError):
    """Base error for resource address resolution."""


class UnknownResourceError(ResourceResolutionError):
    """Raised when a logical resource or registered address is unknown."""


class AmbiguousResourceError(ResourceResolutionError):
    """Raised when an identity/address maps to multiple resources."""


@dataclass(frozen=True)
class ResourceRecord:
    resource_id: str
    resource_type: str
    provider: str
    logical_name: str
    physical_address: str
    canonical: bool = True
    status: str = "ACTIVE"
    scope: str = ""
    authority: str = ""
    provenance: str = ""
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class ResourceResolution:
    record: ResourceRecord
    requested: str
    matched_by: str
    physical_address: str


class ResourceLocator:
    """Resolve a resource identity/name/address without performing the read."""

    def __init__(self, records: tuple[ResourceRecord, ...]) -> None:
        self._by_id: dict[str, ResourceRecord] = {}
        self._by_name: dict[str, ResourceRecord] = {}
        self._by_address: dict[str, ResourceRecord] = {}

        for record in records:
            self._register(self._by_id, record.resource_id, record)
            self._register(self._by_name, record.logical_name, record)
            self._register(self._by_address, record.physical_address, record)
            for alias in record.aliases:
                self._register(self._by_name, alias, record)

    @classmethod
    def from_registry(cls, payload: Mapping[str, Any]) -> "ResourceLocator":
        records = tuple(
            ResourceRecord(
                resource_id=str(item["resource_id"]),
                resource_type=str(item["resource_type"]),
                provider=str(item["provider"]),
                logical_name=str(item["logical_name"]),
                physical_address=str(item["physical_address"]),
                canonical=bool(item.get("canonical", True)),
                status=str(item.get("status", "ACTIVE")),
                scope=str(item.get("scope", "")),
                authority=str(item.get("authority", "")),
                provenance=str(item.get("provenance", "")),
                aliases=tuple(str(value) for value in item.get("aliases", ())),
            )
            for item in payload.get("records", ())
        )
        return cls(records)

    def resolve(self, requested: str) -> ResourceResolution:
        key = requested.strip()
        if not key:
            raise UnknownResourceError("resource identifier/address is required")

        record = self._by_id.get(key)
        if record:
            return ResourceResolution(record, requested, "resource_id", record.physical_address)

        record = self._by_name.get(key)
        if record:
            return ResourceResolution(record, requested, "logical_name", record.physical_address)

        record = self._by_address.get(key)
        if record:
            return ResourceResolution(record, requested, "physical_address", record.physical_address)

        raise UnknownResourceError(f"unknown ELO resource: {requested}")

    def address(self, requested: str) -> str:
        return self.resolve(requested).physical_address

    def records(self) -> tuple[ResourceRecord, ...]:
        return tuple(self._by_id.values())

    @staticmethod
    def _register(
        index: dict[str, ResourceRecord],
        key: str,
        record: ResourceRecord,
    ) -> None:
        if key in index and index[key] != record:
            raise AmbiguousResourceError(f"resource key maps to multiple resources: {key}")
        index[key] = record
