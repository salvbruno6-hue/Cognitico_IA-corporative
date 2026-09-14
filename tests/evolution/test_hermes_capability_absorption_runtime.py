from dataclasses import dataclass

import pytest

from elo.cognitive.hermes_capability_absorption_runtime import (
    HermesAbsorptionResult,
    HermesCapabilityAbsorptionRuntime,
    HermesSnapshot,
)
from elo.cognitive.hermes_capability_extractor import HERMES_REPOSITORY, PATTERN_RULES

HERMES_COMMIT = "278a7d1cc07daa3d0b73934673afccf2310a30b1"


def _snapshot() -> HermesSnapshot:
    return HermesSnapshot(
        source_repository=HERMES_REPOSITORY,
        source_commit=HERMES_COMMIT,
        files={path: f"verified fixture evidence: {path}" for _, pattern in PATTERN_RULES for path in pattern.evidence_paths},
    )


@dataclass
class FixtureProvider:
    value: HermesSnapshot

    def snapshot(self) -> HermesSnapshot:
        return self.value


def test_runtime_executes_snapshot_to_candidate_pipeline() -> None:
    result = HermesCapabilityAbsorptionRuntime(provider=FixtureProvider(_snapshot())).run(tenant_id="tenant-a")

    assert isinstance(result, HermesAbsorptionResult)
    assert result.source_repository == HERMES_REPOSITORY
    assert result.source_commit == HERMES_COMMIT
    assert {pattern.capability_id for pattern in result.extracted} == {
        "HERMES-CAP-001",
        "HERMES-CAP-002",
        "HERMES-CAP-003",
    }
    assert all(decision.candidate_creation_allowed for decision in result.decisions)
    assert {candidate.capability_id for candidate in result.candidates} == {
        "HERMES-CAP-001",
        "HERMES-CAP-002",
        "HERMES-CAP-003",
    }
    assert all(candidate.state.value == "CANDIDATE" for candidate in result.candidates)


def test_runtime_preserves_snapshot_provenance() -> None:
    result = HermesCapabilityAbsorptionRuntime(provider=FixtureProvider(_snapshot())).run(tenant_id="tenant-a")
    assert all(candidate.source_ref == HERMES_REPOSITORY for candidate in result.candidates)
    assert all(candidate.source_commit == HERMES_COMMIT for candidate in result.candidates)
    assert all(candidate.provenance["source_commit"] == HERMES_COMMIT for candidate in result.candidates)


def test_runtime_rejects_unproven_snapshot() -> None:
    snapshot = _snapshot()
    invalid = HermesSnapshot(source_repository=HERMES_REPOSITORY, source_commit="", files=snapshot.files)
    with pytest.raises(ValueError, match="repository and commit provenance"):
        HermesCapabilityAbsorptionRuntime(provider=FixtureProvider(invalid)).run(tenant_id="tenant-a")


def test_runtime_requires_complete_evidence() -> None:
    snapshot = _snapshot()
    incomplete = dict(snapshot.files)
    incomplete.pop("elo_bridge/contract.py")
    invalid = HermesSnapshot(
        source_repository=HERMES_REPOSITORY,
        source_commit=HERMES_COMMIT,
        files=incomplete,
    )
    result = HermesCapabilityAbsorptionRuntime(provider=FixtureProvider(invalid)).run(tenant_id="tenant-a")
    assert {candidate.capability_id for candidate in result.candidates} == {"HERMES-CAP-003"}
