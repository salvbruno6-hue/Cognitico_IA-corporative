"""Governed admission boundary between external information and ELO memory."""

from dataclasses import dataclass
from typing import Literal, Mapping

AdmissionOutcome = Literal[
    "REJECT",
    "ARCHIVE",
    "OBSERVATION",
    "EVIDENCE",
    "KNOWLEDGE_CANDIDATE",
    "KNOWLEDGE",
    "DECISION",
    "POLICY",
    "LESSON_LEARNED",
    "ARCHITECTURAL_PROPOSAL",
]


@dataclass(frozen=True)
class AdmissionRequest:
    """Authorized information submitted for retention classification."""

    tenant_id: str
    domain: str
    source_type: str
    source_id: str
    content: str
    provenance: Mapping[str, str]
    authorized: bool = False
    relevant: bool = True
    evidence_available: bool = False
    decision_relevant: bool = False
    architectural_change_proposed: bool = False


@dataclass(frozen=True)
class AdmissionResult:
    outcome: AdmissionOutcome
    reason: str


class KnowledgeAdmission:
    """Deterministic first gate; policy engines can extend this contract later."""

    def evaluate(self, request: AdmissionRequest) -> AdmissionResult:
        if not request.authorized:
            return AdmissionResult("REJECT", "retention is not authorized")
        if not request.tenant_id or not request.domain:
            return AdmissionResult("REJECT", "tenant_id and domain are required")
        if not request.provenance:
            return AdmissionResult("REJECT", "provenance is required")
        if not request.relevant:
            return AdmissionResult("ARCHIVE", "information is not relevant to active knowledge")
        if request.architectural_change_proposed:
            return AdmissionResult(
                "ARCHITECTURAL_PROPOSAL",
                "architectural change requires an explicit governance gate",
            )
        if request.decision_relevant:
            return AdmissionResult("DECISION", "information is relevant to a governed decision")
        if request.evidence_available:
            return AdmissionResult("EVIDENCE", "retained information has supporting evidence")
        return AdmissionResult(
            "OBSERVATION",
            "authorized relevant information retained as non-canonical observation",
        )
