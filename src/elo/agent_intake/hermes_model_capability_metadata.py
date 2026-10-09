"""Candidate-only model capability metadata contract."""
from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json
import math


class MetadataDisposition(StrEnum):
    CANDIDATE_ONLY = "CANDIDATE_ONLY"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class ModelCapabilityMetadata:
    model_id: str
    capabilities: frozenset[str]
    context_window: int
    input_cost: float
    output_cost: float
    training_tier: str
    provenance_ref: str


@dataclass(frozen=True)
class MetadataAssessment:
    model_id: str
    disposition: MetadataDisposition
    routing_permitted: bool
    warning: str | None
    metadata_digest: str
    provenance_ref: str


def _canonical_digest(metadata: ModelCapabilityMetadata) -> str:
    payload = {
        "capabilities": sorted(metadata.capabilities),
        "context_window": metadata.context_window,
        "input_cost": metadata.input_cost,
        "model_id": metadata.model_id,
        "output_cost": metadata.output_cost,
        "training_tier": metadata.training_tier,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def assess_model_capability_metadata(metadata: ModelCapabilityMetadata) -> MetadataAssessment:
    digest = _canonical_digest(metadata)
    required_text = (metadata.model_id, metadata.training_tier, metadata.provenance_ref)
    capabilities_valid = bool(metadata.capabilities) and all(
        isinstance(capability, str) and capability.strip() for capability in metadata.capabilities
    )
    if not all(isinstance(value, str) and value.strip() for value in required_text) or not capabilities_valid:
        return MetadataAssessment(metadata.model_id, MetadataDisposition.BLOCKED, False,
                                  "missing_model_metadata_controls", digest, metadata.provenance_ref)

    costs_valid = all(
        isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0
        for value in (metadata.input_cost, metadata.output_cost)
    )
    if metadata.context_window <= 0 or not costs_valid:
        return MetadataAssessment(metadata.model_id, MetadataDisposition.BLOCKED, False,
                                  "invalid_model_metadata_values", digest, metadata.provenance_ref)

    recognized_training_tiers = {"verified", "standard", "production"}
    warning = None if metadata.training_tier.strip().lower() in recognized_training_tiers else (
        "training_tier_requires_policy_review"
    )
    return MetadataAssessment(metadata.model_id, MetadataDisposition.CANDIDATE_ONLY, False,
                              warning, digest, metadata.provenance_ref)
