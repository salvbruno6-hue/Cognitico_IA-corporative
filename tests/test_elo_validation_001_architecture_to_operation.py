from dataclasses import dataclass

import pytest

from elo.core.canonical_identity import CanonicalIdentityRegistry, EloCanonicalIdentity
from elo.core.diagnostic_scenarios import (
    DiagnosticLens,
    DiagnosticObservation,
    DiagnosticScenarioEngine,
    DiagnosticStatus,
)
from elo.core.source_resolver import RetrievedSource, SourceResolutionRequest, SourceResolver


@dataclass
class Adapter:
    kind: str = "GITHUB"
    capability: str = "architecture_review"
    available_state: bool = True
    results: tuple[RetrievedSource, ...] = ()

    def available(self) -> bool:
        return self.available_state

    def retrieve(self, candidate, request):
        return self.results


def request(**overrides):
    values = dict(
        query="architecture",
        tenant_id="tenant-a",
        domain="PCP",
        principal_id="specialist-pcp",
        session_id="session-1",
        request_id="request-1",
        correlation_id="corr-1",
        conversation_id="conversation-1",
        authorization_scope="read:architecture",
    )
    values.update(overrides)
    return SourceResolutionRequest(**values)


def candidate():
    from elo.core.source_discovery import SourceCandidate

    return SourceCandidate(
        kind="GITHUB",
        reason="authorized source lookup",
        priority=1,
        query="architecture",
        required_capability="architecture_review",
    )


def test_canonical_identity_is_read_only_and_change_requires_governance():
    identity = EloCanonicalIdentity(
        name="ELO",
        purpose="governed cognitive operation",
        architecture_version="test",
        cognitive_core_path="Core",
        principles=("canonical authority",),
        canonical_boundaries=("Cognitive/Core/Forge",),
        governance_policy="Evolution Gate",
        current_verified_state="TEST",
        metadata={},
    )
    registry = CanonicalIdentityRegistry(identity)

    assert registry.get() == identity
    proposal = registry.propose_change("test boundary change")
    assert proposal["type"] == "ARCHITECTURAL_CHANGE_PROPOSAL"
    assert proposal["requires_governance_gate"] == "true"
    with pytest.raises(ValueError):
        registry.propose_change("   ")


def test_source_resolution_rejects_missing_identity_and_authorization_context():
    resolver = SourceResolver()
    with pytest.raises(ValueError, match="tenant_id"):
        resolver.resolve(candidate(), request(tenant_id=""))
    with pytest.raises(ValueError, match="authorization_scope"):
        resolver.resolve(candidate(), request(authorization_scope=""))


def test_source_resolution_preserves_tenant_domain_principal_and_provenance():
    source = RetrievedSource(
        source_id="source-1",
        source_type="repository",
        content="architecture evidence",
        provenance={"provider": "test"},
    )
    resolver = SourceResolver((Adapter(results=(source,)),))

    result = resolver.resolve(candidate(), request())

    assert result.status == "RETRIEVED_TO_TEMPORAL"
    record = result.temporal_records[0]
    assert record.provenance["provider"] == "test"
    assert record.provenance["tenant_id"] == "tenant-a"
    assert record.provenance["domain"] == "PCP"
    assert record.provenance["principal_id"] == "specialist-pcp"
    assert record.provenance["source_id"] == "source-1"


def test_source_resolution_degrades_without_provider_and_never_invents_evidence():
    unavailable = Adapter(available_state=False)
    resolver = SourceResolver((unavailable,))

    result = resolver.resolve(candidate(), request())

    assert result.status == "UNAVAILABLE"
    assert result.retrieved == ()
    assert result.temporal_records == ()
    assert result.gap is not None


def test_source_resolution_blocks_capability_mismatch():
    unauthorized = Adapter(capability="write.repository")
    resolver = SourceResolver((unauthorized,))

    result = resolver.resolve(candidate(), request())

    assert result.status == "UNAUTHORIZED"
    assert result.retrieved == ()


def test_canonical_scenario_engine_blocks_conflicting_specialist_evidence():
    engine = DiagnosticScenarioEngine()
    scenario = engine.create("conflict", "qual a causa?")
    scenario = scenario.__class__(
        scenario_id=scenario.scenario_id,
        question=scenario.question,
        observations=(
            DiagnosticObservation(
                evidence_id="ev-a",
                dimension="capacity",
                value=0.9,
                statement="turno insuficiente",
                lens=DiagnosticLens.CAPACITY,
                status=DiagnosticStatus.CONFLICTING,
            ),
        ),
    )

    result = engine.compare((scenario,))

    assert result["status"] == "BLOCKED"
    assert result["requires_human_decision"] is True


def test_canonical_scenario_engine_keeps_duplicate_authority_out_of_compatibility_layer():
    engine = DiagnosticScenarioEngine()
    scenario = engine.create("scenario-1", "avaliar capacidade")
    result = engine.compare((scenario,))

    assert result["status"] == "INSUFFICIENT"
    assert result["requires_human_decision"] is True
    assert result["scenarios"] == ("scenario-1",)


def test_scenario_reasoning_does_not_execute_actions_or_mutate_evidence():
    engine = DiagnosticScenarioEngine()
    observation = DiagnosticObservation(
        evidence_id="ev-1",
        dimension="capacity",
        value=0.9,
        statement="capacidade restrita",
        confidence=0.9,
        lens=DiagnosticLens.CAPACITY,
    )
    scenario = engine.create("scenario-2", "avaliar capacidade")
    scenario = scenario.__class__(
        scenario_id=scenario.scenario_id,
        question=scenario.question,
        observations=(observation,),
    )

    before = scenario.observations
    result = engine.compare((scenario,))

    assert scenario.observations == before
    assert "execute" not in result
    assert result["status"] == "COMPARABLE"
