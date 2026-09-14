"""Provider-neutral, evidence-first media boundary for ELO.

Media is an input/transformation capability, not a second evidence or learning
authority. External processors may supply observations; ELO keeps provenance,
identity and promotion governance.
"""
from dataclasses import dataclass
from typing import Mapping


class MediaBoundaryError(ValueError):
    pass


@dataclass(frozen=True)
class MediaObservation:
    media_id: str
    tenant_id: str
    media_kind: str
    source_ref: str
    evidence_ids: tuple[str, ...]
    provenance: Mapping[str, str]
    transformation: str | None = None


class GovernedMediaBoundary:
    _SECRET_KEYS = {"password", "token", "access_token", "refresh_token", "api_key", "service_role"}

    def accept(self, observation: MediaObservation) -> MediaObservation:
        if not observation.media_id or not observation.tenant_id or not observation.media_kind:
            raise MediaBoundaryError("media identity, tenant and kind are required")
        if not observation.source_ref or not observation.evidence_ids:
            raise MediaBoundaryError("source_ref and evidence_ids are required")
        if any(key.lower() in self._SECRET_KEYS for key in observation.provenance):
            raise MediaBoundaryError("secret-bearing provenance is forbidden")
        if any(not item for item in observation.evidence_ids):
            raise MediaBoundaryError("evidence IDs must be non-empty")
        return observation
