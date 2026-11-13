"""Governed execution boundary for PCP evidence.

The PCP side may only prepare a canonical observation. Actual lifecycle
execution belongs to the existing ELO/Symbiont authorities.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .pcp_symbiont_handoff import PCPSymbiontHandoff


@dataclass(frozen=True)
class PCPHandoffResult:
    status: str
    observation_id: str
    delegated: bool
    response: Any | None


def delegate_pcp_observation(
    handoff: PCPSymbiontHandoff,
    *,
    canonical_handoff: Callable[[Mapping[str, Any]], Any],
) -> PCPHandoffResult:
    """Delegate to an injected canonical authority; never implement it here."""
    response = canonical_handoff(handoff.observation)
    return PCPHandoffResult(
        status="DELEGATED",
        observation_id=str(handoff.observation["observation_id"]),
        delegated=True,
        response=response,
    )
