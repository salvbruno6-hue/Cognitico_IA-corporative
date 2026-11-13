from __future__ import annotations

import json

import pytest

from elo.cognitive.reasoning.llm_inference import (
    GovernedLLMInferenceProvider,
    LLMInferenceRuntime,
    parse_inference_envelope,
)
from elo.cognitive.reasoning.requirement_analysis import (
    RequirementNode,
    RequirementSourceType,
    RequirementState,
    ResolutionAttemptKind,
)
from elo.cognitive.reasoning.requirement_resolution import RequirementResolutionFlow
from elo.cognitive.routing.execution_routing import RoutingDecision
from elo.cognitive.routing.model_selection import ModelCandidate
from elo.integrations.ai_provider import AIResponse


class FakeIntelligenceRouter:
    def __init__(self, output: str, *, provider: str = "openai", model: str = "test-model"):
        self.output = output
        self.provider = provider
        self.model = model
        self.calls = 0
        self.last_request = None

    def route_and_execute(self, request, *, models=None, preferred_models=None, **kwargs):
        self.calls += 1
        self.last_request = request
        model_id = f"{self.provider}:{self.model}"
        assert models
        assert any(candidate.model_id == model_id for candidate in models)
        return (
            RoutingDecision(
                capability=request.capability,
                model_id=model_id,
                tool_id=None,
                rationale="fixture",
            ),
            AIResponse(
                request_id=request.request_id,
                provider=self.provider,
                model=self.model,
                output=self.output,
                provenance={"fixture": "true"},
            ),
        )


def _runtime() -> LLMInferenceRuntime:
    return LLMInferenceRuntime(
        tenant_id="tenant-a",
        specialist_id="requirement-inference",
        capability="requirement_inference",
        models=(
            ModelCandidate(
                model_id="openai:test-model",
                capabilities=frozenset({"requirement_inference"}),
                quality=1.0,
                evidence=1.0,
            ),
        ),
        request_namespace="test-requirement-inference",
        context="Only governed fixture evidence is available.",
    )


def _node(*, entity: str | None = "MLT-C08") -> RequirementNode:
    return RequirementNode(
        requirement_id="REQ-01",
        text="Determine the governed installation allowance",
        entity=entity,
    )


@pytest.mark.parametrize(
    "output",
    (
        "free-form answer",
        "{broken-json",
        "{}",
        json.dumps({"state": "INFERRED", "value": ""}),
        json.dumps({"state": "UNKNOWN", "value": "12"}),
        json.dumps({"state": "KNOWN", "value": "12"}),
        json.dumps({"state": "INFERRED", "value": "12", "confidence": 0.99}),
    ),
)
def test_invalid_or_authoritative_model_output_never_becomes_claim(output):
    router = FakeIntelligenceRouter(output)
    provider = GovernedLLMInferenceProvider(router=router, runtime=_runtime())

    result = provider.resolve(_node(), "installation.allowance", ())

    assert router.calls == 1
    assert result.claims == ()
    assert len(result.evidence_ids) == 1
    assert result.evidence_ids[0].startswith("evidence:llm-inference:")


def test_model_cannot_redirect_requirement_or_entity_identity():
    output = json.dumps(
        {
            "state": "INFERRED",
            "value": "12%",
            "requirement_id": "OTHER",
            "entity": "OTHER-ENTITY",
        }
    )
    router = FakeIntelligenceRouter(output)
    provider = GovernedLLMInferenceProvider(router=router, runtime=_runtime())

    result = provider.resolve(_node(), "installation.allowance", ())

    assert result.claims == ()


def test_inferred_hypothesis_is_bound_to_target_and_requires_human_validation():
    router = FakeIntelligenceRouter(
        json.dumps({"state": "INFERRED", "value": "12%"})
    )
    provider = GovernedLLMInferenceProvider(router=router, runtime=_runtime())

    result = provider.resolve(_node(), "installation.allowance", ())

    assert len(result.claims) == 1
    claim = result.claims[0]
    assert claim.requirement_id == "REQ-01"
    assert claim.subject == "MLT-C08"
    assert claim.predicate == "installation.allowance"
    assert claim.value == "12%"
    assert claim.state is RequirementState.INFERRED
    assert claim.requires_human_validation is True
    assert claim.provenance.source_type is RequirementSourceType.LLM_INFERENCE
    assert claim.provenance.validation_status == "UNVERIFIED"
    assert claim.provenance.reasoning_method == "controlled-llm-inference:v1"
    assert claim.provenance.evidence_ids == result.evidence_ids
    assert "12%" not in claim.provenance.source_reference

    assert router.last_request is not None
    assert router.last_request.tenant_id == "tenant-a"
    assert router.last_request.metadata == {
        "requirement_id": "REQ-01",
        "parameter": "installation.allowance",
        "entity": "MLT-C08",
        "inference_method": "controlled-llm-inference:v1",
    }


def test_canonical_flow_keeps_llm_hypothesis_human_gated_not_fact():
    router = FakeIntelligenceRouter(
        json.dumps({"state": "INFERRED", "value": "12%"})
    )
    provider = GovernedLLMInferenceProvider(router=router, runtime=_runtime())
    flow = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.INFERENCE: provider}
    )

    result = flow.resolve(
        node=_node(),
        parameter="installation.allowance",
    )

    assert result.executed_order == (ResolutionAttemptKind.INFERENCE,)
    assert result.assessment.state is RequirementState.HUMAN_VALIDATION_REQUIRED
    assert result.assessment.human_validation_required is True
    assert all(claim.state is not RequirementState.KNOWN for claim in result.claims)


def test_conflict_remains_fail_closed_in_canonical_flow():
    router = FakeIntelligenceRouter(
        json.dumps({"state": "CONFLICT", "value": "12% versus 15%"})
    )
    provider = GovernedLLMInferenceProvider(router=router, runtime=_runtime())
    flow = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.INFERENCE: provider}
    )

    result = flow.resolve(
        node=_node(),
        parameter="installation.allowance",
    )

    assert result.assessment.state is RequirementState.CONFLICT
    assert result.assessment.human_validation_required is True
    assert result.claims[-1].requires_human_validation is True


def test_no_usable_hypothesis_is_not_fabricated_or_confirmed_gap():
    router = FakeIntelligenceRouter("")
    provider = GovernedLLMInferenceProvider(router=router, runtime=_runtime())
    flow = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.INFERENCE: provider}
    )

    result = flow.resolve(
        node=_node(),
        parameter="installation.allowance",
    )

    assert result.claims == ()
    assert result.assessment.state is RequirementState.GAP_CANDIDATE
    assert result.assessment.state is not RequirementState.GAP_CONFIRMED
    assert result.attempts[0].kind is ResolutionAttemptKind.INFERENCE
    assert result.attempts[0].evidence_ids


def test_missing_target_entity_fails_before_model_execution():
    router = FakeIntelligenceRouter(
        json.dumps({"state": "INFERRED", "value": "12%"})
    )
    provider = GovernedLLMInferenceProvider(router=router, runtime=_runtime())

    with pytest.raises(ValueError, match="explicit target entity"):
        provider.resolve(_node(entity=None), "installation.allowance", ())

    assert router.calls == 0


def test_strict_parser_accepts_only_allowed_public_envelope():
    assert parse_inference_envelope(
        json.dumps({"state": "ASSUMPTION_REQUIRED", "value": "Use 12% pending approval"})
    ) == (
        RequirementState.ASSUMPTION_REQUIRED,
        "Use 12% pending approval",
    )
