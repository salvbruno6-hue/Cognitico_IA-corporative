"""Candidate-only model capability metadata contract."""
from dataclasses import dataclass
from enum import StrEnum
import hashlib


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


def assess_model_capability_metadata(metadata: ModelCapabilityMetadata) -> MetadataAssessment:
    digest_source = "|".join((
        metadata.model_id,
        ",".join(sorted(metadata.capabilities)),
        str(metadata.context_window),
        str(metadata.input_cost),
        str(metadata.output_cost),
        metadata.training_tier,
    ))
    digest = hashlib.sha256(digest_source.encode("utf-8")).hexdigest()

    if not metadata.model_id or not metadata.provenance_ref:
        return MetadataAssessment(metadata.model_id, MetadataDisposition.BLOCKED, False,
                                  "missing_model_metadata_controls", digest, metadata.provenance_ref)

    if metadata.context_window <= 0 or metadata.input_cost < 0 or metadata.output_cost < 0:
        return MetadataAssessment(metadata.model_id, MetadataDisposition.BLOCKED, False,
                                  "invalid_model_metadata_values", digest, metadata.provenance_ref)

    warning = (
        "training_tier_requires_policy_review"
        if metadata.training_tier.lower() in {"unknown", "experimental", "unverified"}
        else None
    )
    return MetadataAssessment(metadata.model_id, MetadataDisposition.CANDIDATE_ONLY, False,
                              warning, digest, metadata.provenance_ref)
