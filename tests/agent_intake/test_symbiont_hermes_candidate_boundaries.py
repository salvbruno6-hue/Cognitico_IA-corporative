from elo.agent_intake.hermes_model_capability_metadata import (
    MetadataDisposition,
    ModelCapabilityMetadata,
    assess_model_capability_metadata,
)
from elo.agent_intake.hermes_session_writer_registry import (
    SessionWriterHandle,
    WriterDisposition,
    assess_session_writer,
)


def test_symbiont_model_observation_cannot_route():
    result = assess_model_capability_metadata(ModelCapabilityMetadata(
        model_id="candidate-model",
        capabilities=frozenset({"reasoning", "tools"}),
        context_window=64000,
        input_cost=0.5,
        output_cost=1.0,
        training_tier="experimental",
        provenance_ref="hermes:model-capability:evidence",
    ))
    assert result.disposition is MetadataDisposition.CANDIDATE_ONLY
    assert result.routing_permitted is False
    assert result.provenance_ref


def test_symbiont_session_observation_cannot_write():
    result = assess_session_writer(SessionWriterHandle(
        session_id="session-candidate",
        tenant_id="tenant",
        principal_id="principal",
        writer_ref="hermes:writer",
        provenance_ref="hermes:session-writer:evidence",
        durable=True,
    ))
    assert result.disposition is WriterDisposition.CANDIDATE_ONLY
    assert result.write_permitted is False
    assert result.provenance_ref


def test_missing_provenance_blocks_both_candidate_classes():
    model = assess_model_capability_metadata(ModelCapabilityMetadata(
        model_id="candidate-model",
        capabilities=frozenset(),
        context_window=1,
        input_cost=0,
        output_cost=0,
        training_tier="verified",
        provenance_ref="",
    ))
    writer = assess_session_writer(SessionWriterHandle(
        session_id="session",
        tenant_id="tenant",
        principal_id="principal",
        writer_ref="writer",
        provenance_ref="",
    ))
    assert model.disposition is MetadataDisposition.BLOCKED
    assert writer.disposition is WriterDisposition.BLOCKED
    assert model.routing_permitted is False
    assert writer.write_permitted is False
