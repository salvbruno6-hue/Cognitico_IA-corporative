"""Provider-neutral runtime capability discovery for ELO.

Local tools and remote providers are capabilities, not architectural
requirements. Secrets are never represented in the registry.
"""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Callable, Mapping


class CapabilityStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


_FORBIDDEN_METADATA_FRAGMENTS = ("api_key", "apikey", "token", "password", "secret", "authorization")


def _safe_metadata(metadata: Mapping[str, str]) -> Mapping[str, str]:
    if any(
        any(fragment in key.casefold() for fragment in _FORBIDDEN_METADATA_FRAGMENTS)
        for key in metadata
    ):
        raise ValueError("secret values must not be stored in capability metadata")
    return dict(metadata)


@dataclass(frozen=True)
class CapabilityProbe:
    kind: str
    name: str
    version: str | None = None
    health_check: Callable[[], bool] | None = field(default=None, repr=False, compare=False)
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _safe_metadata(self.metadata)

    def probe(self) -> CapabilityStatus:
        if self.health_check is None:
            return CapabilityStatus.UNKNOWN
        try:
            return CapabilityStatus.AVAILABLE if self.health_check() else CapabilityStatus.UNAVAILABLE
        except Exception:
            return CapabilityStatus.UNAVAILABLE


@dataclass(frozen=True)
class CapabilitySnapshot:
    name: str
    kind: str
    status: CapabilityStatus
    version: str | None
    metadata: Mapping[str, str] = field(default_factory=dict)


class CapabilityRegistry:
    """Discover capabilities without making any provider mandatory."""

    def __init__(self, capabilities: tuple[CapabilityProbe, ...] = ()) -> None:
        self._capabilities = {item.name: item for item in capabilities}

    def register(self, capability: CapabilityProbe) -> None:
        self._capabilities[capability.name] = capability

    def snapshot(self) -> tuple[CapabilitySnapshot, ...]:
        return tuple(
            CapabilitySnapshot(
                name=item.name,
                kind=item.kind,
                status=item.probe(),
                version=item.version,
                metadata=_safe_metadata(item.metadata),
            )
            for item in self._capabilities.values()
        )

    def get_available(self, kind: str | None = None) -> tuple[CapabilitySnapshot, ...]:
        return tuple(
            item for item in self.snapshot()
            if item.status == CapabilityStatus.AVAILABLE and (kind is None or item.kind == kind)
        )

    @staticmethod
    def safe_metadata(metadata: Mapping[str, str]) -> Mapping[str, str]:
        """Allow only non-secret capability metadata; reject secret-like keys."""
        return _safe_metadata(metadata)
