"""Canonical cognitive-core boundary for the ELO prototype."""

from __future__ import annotations

from typing import Any

from elo.interface.contracts import CognitiveRequest


class CognitiveCore:
    """Deterministic core for the first executable vertical slice.

    RAG, persistent memory, autonomous agents and advanced decisioning remain
    governed extension points rather than hidden implementations here.
    """

    def process(self, request: CognitiveRequest) -> dict[str, Any]:
        if not request.tenant_id:
            raise ValueError("tenant_id is required")
        return {
            "response": {"type": "analysis", "content": request.message},
            "confidence": 1.0,
            "domain": request.domain,
            "provenance": {
                "request_id": request.request_id,
                "correlation_id": request.correlation_id,
                "tenant_id": request.tenant_id,
                "domain": request.domain,
                "principal_id": request.principal_id,
                "provider": "elo-deterministic-core",
                "evidence_refs": [],
                "policy_decision": "ALLOW",
                "validation_status": "validated",
            },
        }


__all__ = ["CognitiveCore"]
