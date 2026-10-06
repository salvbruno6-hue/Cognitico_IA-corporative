from elo.agent_intake.hermes_session_writer_registry import (
    SessionWriterHandle, WriterDisposition, assess_session_writer,
)

def make_handle(**overrides):
    values = dict(session_id="session-1", tenant_id="tenant-1",
                  principal_id="principal-1", writer_ref="writer-1",
                  provenance_ref="evidence:writer-1", durable=True)
    values.update(overrides)
    return SessionWriterHandle(**values)

def test_valid_handle_is_candidate_only():
    result = assess_session_writer(make_handle())
    assert result.disposition is WriterDisposition.CANDIDATE_ONLY
    assert result.write_permitted is False

def test_missing_provenance_is_blocked():
    result = assess_session_writer(make_handle(provenance_ref=""))
    assert result.disposition is WriterDisposition.BLOCKED
    assert result.write_permitted is False

def test_missing_identity_is_blocked():
    result = assess_session_writer(make_handle(principal_id=""))
    assert result.disposition is WriterDisposition.BLOCKED

def test_durable_handle_does_not_create_write_authority():
    result = assess_session_writer(make_handle(durable=True))
    assert result.write_permitted is False
