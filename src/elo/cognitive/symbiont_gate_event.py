"""Event-driven external gate perception for the Symbiont.

The caller supplies an already received external event. This module performs
only deterministic translation into the existing observation contract.
No polling, timer, scheduler, merge, or authorization is performed here.
"""

from __future__ import annotations

from typing import Any, Mapping

from elo.cognitive.symbiont_gate_perception import ExternalGateObservation


TERMINAL_GATE_STATES = frozenset({"SUCCESS", "PASSED", "COMPLETED", "MERGED"})
NON_TERMINAL_GATE_STATES = frozenset({"QUEUED", "IN_PROGRESS", "PENDING", "CANCELLED"})


def observe_github_gate_event(
    *,
    gate_id: str,
    event: Mapping[str, Any],
) -> ExternalGateObservation:
    """Translate a received GitHub check/workflow event into the gate contract."""
    raw = event.get("conclusion")
    if raw is None:
        raw = event.get("status")
    state = str(raw or "PENDING").upper()

    evidence = event.get("evidence_ref") or event.get("run_id") or event.get("html_url")
    evidence_ref = str(evidence) if evidence is not None else None

    return ExternalGateObservation(
        gate_id=gate_id,
        state=state,
        evidence_ref=evidence_ref,
    )


__all__ = ["observe_github_gate_event"]
