"""Candidate-only registry contract for session writer handles."""
from dataclasses import dataclass
from enum import StrEnum
import hashlib

class WriterDisposition(StrEnum):
    CANDIDATE_ONLY = "CANDIDATE_ONLY"
    BLOCKED = "BLOCKED"

@dataclass(frozen=True)
class SessionWriterHandle:
    session_id: str
    tenant_id: str
    principal_id: str
    writer_ref: str
    provenance_ref: str
    durable: bool = False

@dataclass(frozen=True)
class WriterAssessment:
    session_id: str
    disposition: WriterDisposition
    write_permitted: bool
    handle_digest: str
    reason: str
    provenance_ref: str

def assess_session_writer(handle: SessionWriterHandle) -> WriterAssessment:
    raw = "|".join((handle.session_id, handle.tenant_id, handle.principal_id,
                    handle.writer_ref, handle.provenance_ref, str(handle.durable)))
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    if not all((handle.session_id, handle.tenant_id, handle.principal_id,
                handle.writer_ref, handle.provenance_ref)):
        return WriterAssessment(handle.session_id, WriterDisposition.BLOCKED, False, digest,
                                "missing_session_writer_controls", handle.provenance_ref)
    return WriterAssessment(handle.session_id, WriterDisposition.CANDIDATE_ONLY, False, digest,
                            "writer_handle_requires_canonical_session_authority",
                            handle.provenance_ref)
