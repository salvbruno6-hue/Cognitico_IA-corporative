from elo.cognitive.hermes_capability_extractor import (
    PATTERN_RULES,
    extract_patterns,
    to_external_pattern,
    to_observation,
)
from elo.cognitive.symbiont_capability_absorption import SymbiontCapabilityAbsorber
from elo.cognitive.symbiont_pattern_intake import SymbiontPatternIntake
from elo.core.evolution_gate import EvolutionClassification


HERMES_COMMIT = "278a7d1cc07daa3d0b73934673afccf2310a30b1"


def _snapshot():
    return {path: f"evidence for {path}" for _, pattern in PATTERN_RULES for path in pattern.evidence_paths}


def test_extracts_only_evidence_backed_patterns():
    patterns = extract_patterns(_snapshot())
    assert {p.capability_id for p in patterns} == {"HERMES-CAP-001", "HERMES-CAP-002", "HERMES-CAP-003"}


def test_missing_evidence_prevents_pattern_extraction():
    snapshot = _snapshot()
    snapshot.pop("elo_bridge/contract.py")
    patterns = extract_patterns(snapshot)
    assert "HERMES-CAP-001" not in {p.capability_id for p in patterns}
    assert "HERMES-CAP-002" not in {p.capability_id for p in patterns}
    assert "HERMES-CAP-003" in {p.capability_id for p in patterns}


def test_extracted_pattern_enters_existing_governed_intake():
    pattern = extract_patterns(_snapshot())[0]
    external = to_external_pattern(pattern, tenant_id="tenant-a", source_commit=HERMES_COMMIT)
    decision = SymbiontPatternIntake().classify(external)
    assert decision.classification is EvolutionClassification.COMPATIBLE
    assert decision.candidate_creation_allowed is True


def test_capability_absorption_produces_candidate_only():
    pattern = extract_patterns(_snapshot())[0]
    external = to_external_pattern(pattern, tenant_id="tenant-a", source_commit=HERMES_COMMIT)
    decision = SymbiontPatternIntake().classify(external)
    observation = to_observation(pattern, tenant_id="tenant-a", source_commit=HERMES_COMMIT)
    candidate = SymbiontCapabilityAbsorber.absorb(
        observation,
        decision,
        validation_contract="ELO Evolution Gate + evidence + regression validation",
    )
    assert candidate is not None
    assert candidate.state.value == "CANDIDATE"
    assert candidate.provenance["provider"] == "ELO-Hermes-Agent"


def test_extraction_has_no_write_or_authority_surface():
    assert not hasattr(__import__("elo.cognitive.hermes_capability_extractor", fromlist=["x"]), "write")
    assert not hasattr(__import__("elo.cognitive.hermes_capability_extractor", fromlist=["x"]), "promote")
