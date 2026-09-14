"""Provider-neutral capability absorption after governed experimentation.

This is a candidate-generation boundary only. It consumes an already governed
laboratory observation and never writes Core, grants authorization, registers
a provider, mutates memory, or bypasses Evolution Gate.
"""
from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.symbionte_lab import SymbiontLabObservation


@dataclass(frozen=True)
class CapabilityCandidate:
    candidate_id: str
    tenant_id: str
    capability: str
    mechanism: str
    source_ref: str
    source_commit: str
    evidence_ids: tuple[str, ...]
    scope: str
    risk: str
    status: str = "CANDIDATE_ONLY"


class NativeCapabilityAbsorption:
    """Generalize a validated lab observation into a governed candidate."""

    def propose(self, observation: SymbiontLabObservation) -> CapabilityCandidate:
        self._validate(observation)
        return CapabilityCandidate(
            candidate_id=observation.observation_id,
            tenant_id=observation.tenant_id,
            capability=observation.domain,
            mechanism=observation.hypothesis,
            source_ref=observation.source_ref,
            source_commit=observation.source_commit,
            evidence_ids=observation.evidence_ids,
            scope=observation.scope,
            risk=observation.risk,
        )

    @staticmethod
    def _validate(observation: SymbiontLabObservation) -> None:
        required = (
            observation.observation_id,
            observation.tenant_id,
            observation.domain,
            observation.hypothesis,
            observation.source_ref,
            observation.source_commit,
            observation.scope,
        )
        if not all(required) or not observation.evidence_ids:
            raise ValueError("capability absorption requires complete provenance and evidence")
        if observation.tenant_scope and observation.tenant_scope != observation.tenant_id:
            raise ValueError("tenant scope mismatch")
        if observation.regression_status.upper() not in {"PASS", "PASSED", "PASSOU"}:
            raise ValueError("capability absorption requires regression PASS")
        if observation.generalization_status.upper() not in {"CONFIRMED", "CONFIRMADO"}:
            raise ValueError("capability absorption requires confirmed generalization")
        if observation.risk.upper() in {"CRITICAL", "CRITICO"}:
            raise ValueError("critical risk cannot become a capability candidate")
