"""Evidence-first capture, deduplication and conflict detection for ELO knowledge."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Mapping


class KnowledgeCaptureError(ValueError):
    """Raised when a knowledge observation cannot enter the capture boundary."""


@dataclass(frozen=True)
class KnowledgeObservation:
    observation_id: str
    tenant_id: str
    domain: str
    title: str
    concept: str
    evidence_ids: tuple[str, ...]
    provenance: Mapping[str, str]
    confidence: str
    fingerprint: str
    state: str = "OBSERVATION"


@dataclass(frozen=True)
class KnowledgeCaptureResult:
    status: str
    fingerprint: str
    reason: str


class NativeKnowledgeCapture:
    """Prepare knowledge observations without becoming a second memory authority."""

    _SECRET_KEYS = {"password", "token", "access_token", "refresh_token", "api_key", "service_role"}

    @staticmethod
    def fingerprint(*, domain: str, title: str, concept: str) -> str:
        normalized = "|".join(
            re.sub(r"\s+", " ", value.strip().lower())
            for value in (domain, title, concept)
        )
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    def capture(
        self,
        *,
        observation_id: str,
        tenant_id: str,
        domain: str,
        title: str,
        concept: str,
        evidence_ids: tuple[str, ...] | list[str],
        provenance: Mapping[str, str],
        confidence: str = "UNKNOWN",
        existing_fingerprints: tuple[str, ...] = (),
        existing_concepts: tuple[str, ...] = (),
    ) -> KnowledgeCaptureResult | KnowledgeObservation:
        required = {
            "observation_id": observation_id,
            "tenant_id": tenant_id,
            "domain": domain,
            "title": title,
            "concept": concept,
        }
        if any(not str(value).strip() for value in required.values()):
            raise KnowledgeCaptureError("observation identity and knowledge fields are required")
        if not evidence_ids:
            raise KnowledgeCaptureError("at least one evidence id is required")
        if not provenance.get("source_ref") or not provenance.get("source_commit"):
            raise KnowledgeCaptureError("provenance requires source_ref and source_commit")
        if any(key.lower() in self._SECRET_KEYS for key in provenance):
            raise KnowledgeCaptureError("secret-bearing provenance is forbidden")
        if confidence not in {"HIGH", "MEDIUM", "LOW", "UNKNOWN"}:
            raise KnowledgeCaptureError("confidence is invalid")
        fp = self.fingerprint(domain=domain, title=title, concept=concept)
        if fp in set(existing_fingerprints):
            return KnowledgeCaptureResult("DUPLICATE", fp, "existing fingerprint matches")
        if concept.strip().lower() in {c.strip().lower() for c in existing_concepts}:
            return KnowledgeCaptureResult("CONFLICT_REVIEW", fp, "existing concept requires reconciliation")
        return KnowledgeObservation(
            observation_id=observation_id,
            tenant_id=tenant_id,
            domain=domain.strip(),
            title=title.strip(),
            concept=concept.strip(),
            evidence_ids=tuple(evidence_ids),
            provenance=dict(provenance),
            confidence=confidence,
            fingerprint=fp,
        )
