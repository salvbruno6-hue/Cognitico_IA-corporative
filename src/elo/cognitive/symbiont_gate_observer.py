"""Reference observer adapter for governed external GitHub gates.

This module only translates an external status into ExternalGateObservation.
It does not poll, schedule, merge, authorize, or mutate canonical state.
"""

from __future__ import annotations

from typing import Any, Mapping

from elo.cognitive.symbiont_gate_perception import ExternalGateObservation


def github_gate_observer_from_status(
    gate_id: str,
    status_payload: Mapping[str, Any],
) -> ExternalGateObservation:
    state = str(status_payload.get("state", "PENDING")).upper()
    evidence_ref = status_payload.get("evidence_ref")
    return ExternalGateObservation(
        gate_id=gate_id,
        state=state,
        evidence_ref=str(evidence_ref) if evidence_ref else None,
    )


__all__ = ["github_gate_observer_from_status"]
