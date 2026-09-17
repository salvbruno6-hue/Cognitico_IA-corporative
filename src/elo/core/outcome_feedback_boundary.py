"""Non-destructive boundary between operational and systemic outcome feedback.

The operational contract remains the lightweight record produced directly from
an execution outcome. The systemic contract is a derived interpretation layer.
This module translates between the two without renaming, deleting, or mutating
either contract.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .outcome_feedback import OutcomeFeedback as OperationalOutcomeFeedback
from .systemic_primitives import OutcomeFeedback as SystemicOutcomeFeedback


@dataclass(frozen=True)
class OutcomeFeedbackTranslation:
    """Preserve the operational record alongside its derived systemic view."""

    operational: OperationalOutcomeFeedback
    systemic: SystemicOutcomeFeedback


def to_systemic_outcome_feedback(
    operational: OperationalOutcomeFeedback,
    *,
    variance: Optional[str] = None,
    observed_at: Optional[datetime] = None,
) -> SystemicOutcomeFeedback:
    """Translate operational feedback into a derived systemic representation.

    ``variance`` and ``observed_at`` are supplied by the systemic interpretation
    layer when available. They are intentionally not inferred from the
    operational ``assessment`` because that would turn a semantic assessment
    into an unsupported systemic claim.
    """
    return SystemicOutcomeFeedback(
        decision_id=operational.decision_id,
        expected=operational.expected,
        observed=operational.observed,
        variance=variance,
        evidence_ids=operational.evidence_ids,
        observed_at=observed_at,
    )


def translate_outcome_feedback(
    operational: OperationalOutcomeFeedback,
    *,
    variance: Optional[str] = None,
    observed_at: Optional[datetime] = None,
) -> OutcomeFeedbackTranslation:
    """Create a provenance-preserving operational/systemic pair."""
    systemic = to_systemic_outcome_feedback(
        operational,
        variance=variance,
        observed_at=observed_at,
    )
    return OutcomeFeedbackTranslation(
        operational=operational,
        systemic=systemic,
    )
