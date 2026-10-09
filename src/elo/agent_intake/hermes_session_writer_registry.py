"""Candidate-only registry contract for session writer handles."""
from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json


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


def _canonical_digest(handle: SessionWriterHandle) -> str:
    payload = {
        "durable": handle.durable,
        "principal_id": handle.principal_id,
        "provenance_ref": handle.provenance_ref,
        "session_id": handle.session_id,
        "tenant_id": handle.tenant_id,
        "writer_ref": handle.writer_ref,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def assess_session_writer(handle: SessionWriterHandle) -> WriterAssessment:
    digest = _canonical_digest(handle)
    required = (handle.session_id, handle.tenant_id, handle.principal_id,
                handle.writer_ref, handle.provenance_ref)
    if not all(isinstance(value, str) and value.strip() for value in required):
        return WriterAssessment(handle.session_id, WriterDisposition.BLOCKED, False, digest,
                                "missing_session_writer_controls", handle.provenance_ref)
    return WriterAssessment(handle.session_id, WriterDisposition.CANDIDATE_ONLY, False, digest,
                            "writer_handle_requires_canonical_session_authority",
                            handle.provenance_ref)
