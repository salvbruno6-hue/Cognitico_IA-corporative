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
from elo.agent_intake.elo_flow_cadence import CadenceOutcome
from elo.agent_intake.flow_learning import FlowAdaptation, FlowAdaptationEngine, FlowOutcomeRecord
from elo.agent_intake.governed_flow_router import GovernedFlowRouter, NextFlowResolution


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

    def execute_flow_step(
        self,
        request: HermesExecutionRequest,
        *,
        capability: str,
        endpoint: str,
        origin_flow: str,
        relation_id: str,
        next_flow: str,
        evidence: Mapping[str, object] | None,
        provenance_refs: tuple[str, ...],
        router: GovernedFlowRouter,
        learning: FlowAdaptationEngine,
        transport: Transport | None = None,
    ) -> tuple[SymbiontExecutionReceipt, FlowAdaptation, NextFlowResolution]:
        """Execute through Hermes, persist the outcome, then ask ELO for the next flow.

        Symbiont remains the transport/execution boundary. ELO owns persistence
        of the learning record, adaptation state and next-flow decision.
        """
        receipt = self.execute(
            request,
            capability=capability,
            endpoint=endpoint,
            transport=transport,
        )
        outcome = self._cadence_outcome(receipt.result.status)
        adaptation = learning.record(
            FlowOutcomeRecord(
                relation_id=relation_id,
                origin_flow=origin_flow,
                target_flow=next_flow,
                outcome=outcome.value,
                success=outcome is CadenceOutcome.PASS,
                evidence_refs=tuple(
                    str(item.get("id", ""))
                    for item in receipt.result.evidence
                    if isinstance(item, Mapping) and item.get("id")
                ),
                provenance_refs=provenance_refs,
                metrics=tuple(
                    (str(key), float(value))
                    for key, value in receipt.result.metrics.items()
                    if isinstance(value, (int, float))
                ),
            )
        )
        routing = router.resolve_next(
            origin_flow=origin_flow,
            outcome=outcome,
            evidence=evidence,
            provenance_refs=provenance_refs,
        )
        return receipt, adaptation, routing

    @staticmethod
    def _cadence_outcome(status: str) -> CadenceOutcome:
        mapping = {
            "completed": CadenceOutcome.PASS,
            "partial": CadenceOutcome.RETEST,
            "blocked": CadenceOutcome.BLOCKED,
            "failed": CadenceOutcome.REJECT,
        }
        try:
            return mapping[status]
        except KeyError as exc:
            raise ValueError(f"unsupported Hermes status for flow cadence: {status}") from exc

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
