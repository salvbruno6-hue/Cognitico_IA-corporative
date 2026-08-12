"""Safety gates preventing reasoning from becoming unsupported decision execution."""
from __future__ import annotations

from . import ClaimStatus, ReasoningResult


class ReasoningPolicyError(PermissionError):
    """Raised when a reasoning result violates cognitive governance."""


def validate_reasoning_result(result: ReasoningResult) -> None:
    if not result.reasoning_id:
        raise ReasoningPolicyError("reasoning_id is required")
    for finding in result.findings:
        if finding.status in {ClaimStatus.UNVERIFIED, ClaimStatus.CONTRADICTED} and finding.confidence > 0.75:
            raise ReasoningPolicyError("high-confidence reasoning cannot be marked unverified or contradicted")
        if finding.status != ClaimStatus.SUPPORTED and not finding.evidence_refs:
            raise ReasoningPolicyError("non-supported findings require explicit evidence or unresolved state")
    if result.overall_confidence > 0.75 and not result.evidence_refs:
        raise ReasoningPolicyError("high-confidence reasoning requires evidence references")
