"""Deterministic contract tests for ELO Lab persistence investigation.

This test surface does not claim live Supabase connectivity. It verifies the
minimum evidence gate that a live adapter must satisfy before reporting
PERSISTENCE_CONFIRMED.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MemoryEvidence:
    memory_id: str
    so: str
    calculation_id: str
    evidence_id: str
    scan_id: str
    formula: str
    result: str


@dataclass(frozen=True)
class PersistenceProbe:
    reported_status: str
    database_rows: tuple[MemoryEvidence, ...]


def validate_persistence(probe: PersistenceProbe) -> str:
    """Return the only admissible gate result for a persistence probe."""
    rows = probe.database_rows
    ids = [row.memory_id for row in rows]

    if len(ids) != len(set(ids)):
        return "FAIL:DUPLICATE_MEMORY_ID"

    if probe.reported_status == "SAVED" and not rows:
        return "FAIL:FALSE_PERSISTENCE_CONFIRMATION"

    for row in rows:
        if not all(
            (
                row.memory_id,
                row.so,
                row.calculation_id,
                row.evidence_id,
                row.scan_id,
                row.formula,
                row.result,
            )
        ):
            return "FAIL:INCOMPLETE_PROVENANCE"

    if probe.reported_status == "SAVED":
        return "PASS:PERSISTENCE_CONFIRMED"

    return "NOT_SAVED"


def replay_calculation(row: MemoryEvidence) -> str:
    """Provide a deterministic replay token from persisted calculation inputs."""
    return f"{row.so}|{row.calculation_id}|{row.formula}|{row.result}"


def test_saved_requires_real_database_evidence():
    probe = PersistenceProbe("SAVED", ())
    assert validate_persistence(probe) == "FAIL:FALSE_PERSISTENCE_CONFIRMATION"


def test_saved_requires_unique_memory_ids():
    row = MemoryEvidence("mem-1", "SO-TEST", "calc-1", "ev-1", "scan-1", "1+1", "2")
    probe = PersistenceProbe("SAVED", (row, row))
    assert validate_persistence(probe) == "FAIL:DUPLICATE_MEMORY_ID"


def test_saved_requires_complete_provenance_chain():
    row = MemoryEvidence("mem-1", "SO-TEST", "calc-1", "ev-1", "scan-1", "", "2")
    probe = PersistenceProbe("SAVED", (row,))
    assert validate_persistence(probe) == "FAIL:INCOMPLETE_PROVENANCE"


def test_saved_is_confirmed_only_after_persisted_evidence_is_valid():
    row = MemoryEvidence("mem-1", "SO-TEST", "calc-1", "ev-1", "scan-1", "1+1", "2")
    probe = PersistenceProbe("SAVED", (row,))
    assert validate_persistence(probe) == "PASS:PERSISTENCE_CONFIRMED"


def test_replay_has_enough_information_to_reconstruct_calculation():
    row = MemoryEvidence("mem-1", "SO-TEST", "calc-1", "ev-1", "scan-1", "1+1", "2")
    assert replay_calculation(row) == "SO-TEST|calc-1|1+1|2"


def test_not_saved_does_not_become_a_false_positive():
    row = MemoryEvidence("mem-1", "SO-TEST", "calc-1", "ev-1", "scan-1", "1+1", "2")
    probe = PersistenceProbe("NOT_SAVED", (row,))
    assert validate_persistence(probe) == "NOT_SAVED"
