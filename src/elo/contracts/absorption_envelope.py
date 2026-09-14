"""Universal fail-closed envelope for governed external mechanism absorption."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


class AbsorptionEnvelopeError(ValueError):
    """Raised when an external mechanism lacks canonical intake evidence."""


@dataclass(frozen=True)
class AbsorptionEnvelope:
    candidate_id: str
    tenant_id: str
    source_ref: str
    source_commit: str
    mechanism: str
    evidence_ids: tuple[str, ...]
    scope: str
    risk: str
    provenance: Mapping[str, str]
    state: str = "CANDIDATE"


class GovernedAbsorptionEnvelope:
    """Validate source→evidence→candidate lineage; never promote or authorize."""

    _SECRET_KEYS = {"password", "token", "access_token", "refresh_token", "api_key", "service_role"}
    _RISKS = {"LOW", "MEDIUM", "HIGH"}

    def prepare(
        self, *, candidate_id: str, tenant_id: str, source_ref: str, source_commit: str,
        mechanism: str, evidence_ids: tuple[str, ...] | list[str], scope: str, risk: str,
        provenance: Mapping[str, str],
    ) -> AbsorptionEnvelope:
        values = (candidate_id, tenant_id, source_ref, source_commit, mechanism, scope)
        if any(not str(v).strip() for v in values):
            raise AbsorptionEnvelopeError("candidate, tenant, source, mechanism and scope are required")
        if not evidence_ids:
            raise AbsorptionEnvelopeError("at least one evidence id is required")
        if risk not in self._RISKS:
            raise AbsorptionEnvelopeError("risk must be LOW, MEDIUM or HIGH")
        if provenance.get("source_ref") != source_ref or provenance.get("source_commit") != source_commit:
            raise AbsorptionEnvelopeError("provenance must match the declared source lineage")
        if any(key.lower() in self._SECRET_KEYS for key in provenance):
            raise AbsorptionEnvelopeError("secret-bearing provenance is forbidden")
        return AbsorptionEnvelope(
            candidate_id=candidate_id.strip(), tenant_id=tenant_id.strip(), source_ref=source_ref.strip(),
            source_commit=source_commit.strip(), mechanism=mechanism.strip(), evidence_ids=tuple(evidence_ids),
            scope=scope.strip(), risk=risk, provenance=dict(provenance),
        )
