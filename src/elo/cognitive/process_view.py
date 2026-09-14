"""Governed Cognitive boundary for process views.

The boundary is deliberately provider-neutral: CURRENT and DEVIATION require
explicit evidence. When no governed observation exists, the result is UNKNOWN
rather than fabricated telemetry.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class ProcessViewState(str, Enum):
    REFERENCE = "REFERENCE"
    CURRENT = "CURRENT"
    DEVIATION = "DEVIATION"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ProcessViewRequest:
    tenant_id: str
    process_id: str
    principal_id: str
    evidence_ids: tuple[str, ...] = ()
    scope: str = ""


@dataclass(frozen=True)
class ProcessViewResponse:
    tenant_id: str
    process_id: str
    state: ProcessViewState
    evidence_ids: tuple[str, ...]
    source_ref: str | None
    observed_value: str | None
    expected_value: str | None
    gap: str | None


class ProcessViewProvider(Protocol):
    def read(self, request: ProcessViewRequest) -> ProcessViewResponse: ...


class GovernedProcessView:
    """Validate a provider response without becoming a telemetry authority."""

    def __init__(self, provider: ProcessViewProvider) -> None:
        self.provider = provider

    def resolve(self, request: ProcessViewRequest) -> ProcessViewResponse:
        self._validate_request(request)
        response = self.provider.read(request)
        self._validate_response(request, response)
        return response

    @staticmethod
    def _validate_request(request: ProcessViewRequest) -> None:
        if not request.tenant_id or not request.process_id or not request.principal_id:
            raise ValueError("tenant, process and principal are required")
        if request.scope and request.scope != request.tenant_id:
            raise ValueError("process view scope does not match tenant")

    @staticmethod
    def _validate_response(request: ProcessViewRequest, response: ProcessViewResponse) -> None:
        if response.tenant_id != request.tenant_id or response.process_id != request.process_id:
            raise ValueError("process view identity mismatch")
        if response.state in {ProcessViewState.CURRENT, ProcessViewState.DEVIATION}:
            if not response.evidence_ids or not response.source_ref:
                raise ValueError("CURRENT/DEVIATION requires governed evidence and source")
        if response.state == ProcessViewState.UNKNOWN and not response.gap:
            raise ValueError("UNKNOWN requires an explicit GAP")
        if response.state == ProcessViewState.DEVIATION and not response.gap:
            raise ValueError("DEVIATION requires an explicit GAP")
