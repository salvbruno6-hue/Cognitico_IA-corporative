"""Canonical contracts for evidence-grounded ELO reasoning."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class ClaimStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    UNVERIFIED = "UNVERIFIED"
    CONTRADICTED = "CONTRADICTED"


class FindingType(str, Enum):
    FACT = "FACT"
    INFERENCE = "INFERENCE"
    HYPOTHESIS = "HYPOTHESIS"
    RISK = "RISK"
    OPPORTUNITY = "OPPORTUNITY"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    evidence_id: str
    claim: str
    quality: float = 0.0
    relevance: float = 0.0
    supports: bool = True
    provenance: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ReasoningFinding:
    finding_id: str
    statement: str
    finding_type: FindingType
    status: ClaimStatus
    confidence: float
    evidence_refs: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    contradictions: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CritiqueResult:
    critique_id: str
    finding_id: str
    strengths: tuple[str, ...] = ()
    weaknesses: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
    alternative_hypotheses: tuple[str, ...] = ()
    confidence_adjustment: float = 0.0
    recommendation: str = "REVIEW"


@dataclass(frozen=True, slots=True)
class ReasoningResult:
    reasoning_id: str
    query: str
    findings: tuple[ReasoningFinding, ...]
    critiques: tuple[CritiqueResult, ...]
    overall_confidence: float
    evidence_refs: tuple[str, ...] = ()
    unresolved_questions: tuple[str, ...] = ()
    provenance: Mapping[str, Any] = field(default_factory=dict)
