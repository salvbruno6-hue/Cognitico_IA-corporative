"""Governed Symbiont -> Hermes execution bridge.

Symbiont is the connector/translation boundary. ELO Cognitive remains the
authority that constructs and authorizes a HermesExecutionRequest. This module
never grants capabilities, mutates canonical knowledge, or promotes learning.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .agents.hermes_contract import HermesExecutionRequest, HermesExecutionResult
from .agents.hermes_runtime import Transport, execute_via_hermes


@dataclass(frozen=True)
class SymbiontExecutionReceipt:
    """Evidence-bearing receipt for one governed external execution."""

    request_id: str
    capability: str
    result: HermesExecutionResult


class SymbiontHermesBridge:
    """Mediate an already-authorized ELO mission to the external Hermes runtime."""

    def execute(
        self,
        request: HermesExecutionRequest,
        *,
        capability: str,
        endpoint: str,
        transport: Transport | None = None,
    ) -> SymbiontExecutionReceipt:
        """Execute one authorized capability and enforce the return contract."""
        if not capability.strip():
            raise ValueError("capability is required")
        if capability not in request.authorized_capabilities:
            raise ValueError("capability is not authorized by ELO request")

        result = execute_via_hermes(request, endpoint=endpoint, transport=transport)
        self._validate_evidence_contract(request, result)
        return SymbiontExecutionReceipt(
            request_id=request.request_id,
            capability=capability,
            result=result,
        )

    @staticmethod
    def _validate_evidence_contract(
        request: HermesExecutionRequest,
        result: HermesExecutionResult,
    ) -> None:
        """Require the evidence classes requested by ELO before accepting a receipt."""
        required = set(request.evidence_requirements)
        if "execution" in required and not (result.execution or result.evidence):
            raise ValueError("Hermes result is missing required execution evidence")
        if "outcome" in required and not result.outcome:
            raise ValueError("Hermes result is missing required outcome evidence")
        if result.learning_candidate is not None:
            promotion_state = result.learning_candidate.get("promotion_state", "candidate_only")
            if promotion_state not in {"candidate_only", "pending", "rejected"}:
                raise ValueError("Hermes learning candidate has invalid promotion state")


__all__ = ["SymbiontExecutionReceipt", "SymbiontHermesBridge"]
