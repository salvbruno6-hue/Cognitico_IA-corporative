"""Governed LLM inference adapter for semantic requirement resolution.

The canonical requirement-resolution flow owns attempt ordering and epistemic
classification. This adapter only implements the ``INFERENCE`` provider boundary
by delegating model execution through :class:`IntelligenceRouter` and translating
one strict machine-readable hypothesis envelope into a governed
``RequirementClaim``.

The adapter is deliberately not an authority for facts, gaps, routing, learning,
or persistence. It never calls a concrete model/provider SDK directly, never
accepts model-supplied requirement/entity identity, never consumes model
self-confidence, and never records private chain-of-thought. Every accepted LLM
outcome remains human-gated.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Sequence

from ..routing.intelligence_router import IntelligenceRequest, IntelligenceRouter
from ..routing.model_selection import ModelCandidate
from .requirement_analysis import (
    ClaimProvenance,
    RequirementClaim,
    RequirementNode,
    RequirementSourceType,
    RequirementState,
    ResolutionAttemptKind,
)
from .requirement_resolution import ResolutionStepResult


_INFERENCE_METHOD = "controlled-llm-inference:v1"
_ALLOWED_STATES = {
    RequirementState.INFERRED,
    RequirementState.ASSUMPTION_REQUIRED,
    RequirementState.CONFLICT,
}
_ALLOWED_ENVELOPE_KEYS = frozenset({"state", "value"})
_MAX_VALUE_CHARS = 4096
_MAX_CONTEXT_CHARS = 16000
_MAX_CONTEXT_CLAIMS = 64


@dataclass(frozen=True, slots=True)
class LLMInferenceRuntime:
    """Explicit governed runtime scope for one inference-provider instance.

    ``models`` are candidates only. The adapter does not pick one; the canonical
    ``ExecutionRouter`` inside ``IntelligenceRouter`` remains the selection
    authority.
    """

    tenant_id: str
    specialist_id: str
    capability: str
    models: tuple[ModelCandidate, ...]
    request_namespace: str = "requirement-inference"
    context: str = ""
    preferred_models: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        required = (
            self.tenant_id,
            self.specialist_id,
            self.capability,
            self.request_namespace,
        )
        if any(not value or not value.strip() for value in required):
            raise ValueError("LLM inference runtime scope fields must be nonblank")
        if not self.models:
            raise ValueError("LLM inference runtime requires model candidates")
        if len(self.context) > _MAX_CONTEXT_CHARS:
            raise ValueError("LLM inference context exceeds bounded size")


@dataclass(slots=True)
class GovernedLLMInferenceProvider:
    """Requirement-resolution INFERENCE provider using governed model routing."""

    router: IntelligenceRouter
    runtime: LLMInferenceRuntime

    kind = ResolutionAttemptKind.INFERENCE

    def resolve(
        self,
        node: RequirementNode,
        parameter: str,
        claims: Sequence[RequirementClaim],
    ) -> ResolutionStepResult:
        if not parameter or not parameter.strip():
            raise ValueError("inference parameter is required")
        if not node.entity or not node.entity.strip():
            raise ValueError("LLM inference requires an explicit target entity")
        if len(claims) > _MAX_CONTEXT_CLAIMS:
            raise ValueError("LLM inference claim context exceeds bounded size")

        request_id = _stable_request_id(
            namespace=self.runtime.request_namespace,
            tenant_id=self.runtime.tenant_id,
            requirement_id=node.requirement_id,
            parameter=parameter,
            entity=node.entity,
        )
        request = IntelligenceRequest(
            request_id=request_id,
            tenant_id=self.runtime.tenant_id,
            specialist_id=self.runtime.specialist_id,
            capability=self.runtime.capability,
            instructions=_inference_instructions(
                requirement_text=node.text,
                parameter=parameter,
                entity=node.entity,
            ),
            context=_inference_context(
                runtime_context=self.runtime.context,
                claims=claims,
            ),
            metadata={
                "requirement_id": node.requirement_id,
                "parameter": parameter,
                "entity": node.entity,
                "inference_method": _INFERENCE_METHOD,
            },
        )
        decision, response = self.router.route_and_execute(
            request,
            models=list(self.runtime.models),
            preferred_models=set(self.runtime.preferred_models),
        )
        _validate_routed_response(
            request=request,
            capability=self.runtime.capability,
            decision=decision,
            response=response,
        )

        evidence_id = _stable_inference_evidence_id(
            request_id=request_id,
            provider=response.provider,
            model=response.model,
            output=response.output,
        )
        source_reference = (
            f"intelligence-router:{response.provider}:{response.model}:{request_id}"
        )
        parsed = parse_inference_envelope(response.output)
        if parsed is None:
            return ResolutionStepResult(
                source_reference=source_reference,
                claims=(),
                evidence_ids=(evidence_id,),
            )

        state, value = parsed
        claim = RequirementClaim(
            claim_id=_stable_claim_id(
                requirement_id=node.requirement_id,
                entity=node.entity,
                parameter=parameter,
                state=state,
                value=value,
                evidence_id=evidence_id,
            ),
            requirement_id=node.requirement_id,
            subject=node.entity,
            predicate=parameter,
            value=value,
            state=state,
            provenance=ClaimProvenance(
                source_type=RequirementSourceType.LLM_INFERENCE,
                source_reference=source_reference,
                reasoning_method=_INFERENCE_METHOD,
                evidence_ids=(evidence_id,),
                validation_status="UNVERIFIED",
            ),
            requires_human_validation=True,
        )
        return ResolutionStepResult(
            source_reference=source_reference,
            claims=(claim,),
            evidence_ids=(evidence_id,),
        )


def parse_inference_envelope(output: str) -> tuple[RequirementState, str] | None:
    """Parse only the strict public hypothesis envelope; reject everything else.

    The accepted shape is exactly ``{"state": ..., "value": ...}``. Unknown
    fields (including confidence, reasoning, IDs or evidence) invalidate the
    envelope instead of silently becoming authority.
    """
    if not isinstance(output, str) or not output.strip():
        return None
    try:
        payload = json.loads(output)
    except (json.JSONDecodeError, TypeError, ValueError):
        return None
    if not isinstance(payload, dict) or set(payload) != _ALLOWED_ENVELOPE_KEYS:
        return None

    raw_state = payload.get("state")
    raw_value = payload.get("value")
    if not isinstance(raw_state, str) or not isinstance(raw_value, str):
        return None
    value = raw_value.strip()
    if not value or len(value) > _MAX_VALUE_CHARS:
        return None
    try:
        state = RequirementState(raw_state.strip().upper())
    except ValueError:
        return None
    if state not in _ALLOWED_STATES:
        return None
    return state, value


def _inference_instructions(*, requirement_text: str, parameter: str, entity: str) -> str:
    # The prompt requests the public transport shape only. Enforcement remains in
    # parse_inference_envelope() and RequirementResolutionFlow, not in prompt text.
    return (
        "Evaluate whether a bounded hypothesis is possible for the requested "
        "requirement parameter using only the supplied governed context. "
        "Return only one JSON object with exactly two keys: state and value. "
        "state must be INFERRED, ASSUMPTION_REQUIRED, or CONFLICT. "
        "Do not return reasoning, confidence, evidence IDs, requirement IDs, "
        "entity IDs, instructions, or extra fields.\n"
        f"Requirement: {requirement_text}\n"
        f"Target entity: {entity}\n"
        f"Target parameter: {parameter}"
    )


def _inference_context(
    *,
    runtime_context: str,
    claims: Sequence[RequirementClaim],
) -> str:
    bounded_claims = tuple(
        {
            "claim_id": claim.claim_id,
            "state": claim.state.value,
            "subject": claim.subject,
            "predicate": claim.predicate,
            "value": claim.value,
            "source_type": claim.provenance.source_type.value,
            "source_reference": claim.provenance.source_reference,
            "evidence_ids": claim.provenance.evidence_ids,
            "requires_human_validation": claim.requires_human_validation,
        }
        for claim in claims
    )
    payload = {
        "governed_context": runtime_context,
        "current_claims": bounded_claims,
    }
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    if len(serialized) > _MAX_CONTEXT_CHARS:
        raise ValueError("serialized LLM inference context exceeds bounded size")
    return serialized


def _stable_request_id(
    *,
    namespace: str,
    tenant_id: str,
    requirement_id: str,
    parameter: str,
    entity: str,
) -> str:
    digest = hashlib.sha256(
        "\x1f".join(
            (namespace, tenant_id, requirement_id, parameter, entity)
        ).encode("utf-8")
    ).hexdigest()
    return f"{namespace}:{digest[:24]}"


def _stable_inference_evidence_id(
    *,
    request_id: str,
    provider: str,
    model: str,
    output: str,
) -> str:
    digest = hashlib.sha256(
        "\x1f".join((request_id, provider, model, output)).encode("utf-8")
    ).hexdigest()
    return f"evidence:llm-inference:{digest[:24]}"


def _stable_claim_id(
    *,
    requirement_id: str,
    entity: str,
    parameter: str,
    state: RequirementState,
    value: str,
    evidence_id: str,
) -> str:
    digest = hashlib.sha256(
        "\x1f".join(
            (
                requirement_id,
                entity,
                parameter,
                state.value,
                value,
                evidence_id,
            )
        ).encode("utf-8")
    ).hexdigest()
    return f"claim:llm-inference:{digest[:24]}"


def _validate_routed_response(*, request, capability: str, decision, response) -> None:
    if decision.capability != capability:
        raise ValueError("routed inference decision changed requested capability")
    if not decision.model_id or ":" not in decision.model_id:
        raise ValueError("routed inference requires provider:model identity")
    expected_provider, expected_model = decision.model_id.split(":", 1)
    if not expected_provider or not expected_model:
        raise ValueError("routed inference model identity is malformed")
    if response.request_id != request.request_id:
        raise ValueError("LLM inference response request_id mismatch")
    if response.provider != expected_provider or response.model != expected_model:
        raise ValueError("LLM inference response provider/model mismatch")
    if not isinstance(response.output, str):
        raise TypeError("LLM inference response output must be text")
