import math

from elo.agent_intake.hermes_model_capability_metadata import (
    MetadataDisposition,
    ModelCapabilityMetadata,
    assess_model_capability_metadata,
)


def make_metadata(**overrides):
    values = dict(
        model_id="model-1",
        capabilities=frozenset({"reasoning"}),
        context_window=128000,
        input_cost=1.0,
        output_cost=2.0,
        training_tier="verified",
        provenance_ref="evidence:model-1",
    )
    values.update(overrides)
    return ModelCapabilityMetadata(**values)


def test_valid_metadata_is_candidate_only():
    result = assess_model_capability_metadata(make_metadata())
    assert result.disposition is MetadataDisposition.CANDIDATE_ONLY
    assert result.routing_permitted is False
    assert result.warning is None


def test_unverified_training_tier_warns_without_authorizing():
    result = assess_model_capability_metadata(make_metadata(training_tier="unknown"))
    assert result.warning == "training_tier_requires_policy_review"
    assert result.routing_permitted is False


def test_unrecognized_training_tier_warns_without_authorizing():
    result = assess_model_capability_metadata(make_metadata(training_tier="unreviewed"))
    assert result.warning == "training_tier_requires_policy_review"
    assert result.routing_permitted is False


def test_missing_or_whitespace_controls_are_blocked():
    assert assess_model_capability_metadata(make_metadata(provenance_ref="")).disposition is MetadataDisposition.BLOCKED
    assert assess_model_capability_metadata(make_metadata(model_id=" ")).disposition is MetadataDisposition.BLOCKED
    assert assess_model_capability_metadata(make_metadata(training_tier=" ")).disposition is MetadataDisposition.BLOCKED
    assert assess_model_capability_metadata(make_metadata(capabilities=frozenset())).disposition is MetadataDisposition.BLOCKED


def test_invalid_or_non_finite_cost_is_blocked():
    for value in (-1.0, math.nan, math.inf):
        result = assess_model_capability_metadata(make_metadata(input_cost=value))
        assert result.disposition is MetadataDisposition.BLOCKED


def test_digest_uses_unambiguous_structured_encoding():
    combined = assess_model_capability_metadata(make_metadata(capabilities=frozenset({"a,b"})))
    separate = assess_model_capability_metadata(make_metadata(capabilities=frozenset({"a", "b"})))
    assert combined.metadata_digest != separate.metadata_digest


def test_metadata_does_not_create_routing_authority():
    result = assess_model_capability_metadata(make_metadata())
    assert result.routing_permitted is False
