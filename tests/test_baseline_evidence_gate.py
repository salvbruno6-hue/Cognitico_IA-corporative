import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs/governance/elo_baseline_gate_manifest.json"


def load_manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_baseline_gate_manifest_is_canonical_and_complete():
    manifest = load_manifest()
    assert manifest["gate"] == "ELO-092-Baseline-Evidence"
    assert manifest["canonical_owner"] == "#92"
    assert manifest["state_target"] == "EVIDENCED_BASELINE"
    assert len(manifest["required_paths"]) >= 5
    assert len(manifest["required_test_contracts"]) >= 5
    assert len(manifest["required_governance_terms"]) >= 4


def test_required_paths_exist():
    manifest = load_manifest()
    missing = [path for path in manifest["required_paths"] if not (ROOT / path).is_file()]
    assert not missing, f"missing baseline evidence paths: {missing}"


def test_required_test_contracts_exist_as_source_symbols():
    manifest = load_manifest()
    missing = []
    for contract in manifest["required_test_contracts"]:
        path, symbol = contract.split("::", 1)
        source = (ROOT / path).read_text(encoding="utf-8")
        if f"def {symbol}(" not in source:
            missing.append(contract)
    assert not missing, f"missing executable evidence contracts: {missing}"


def test_governance_invariants_are_explicit():
    manifest = load_manifest()
    documents = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in manifest["required_paths"]
        if path.endswith(".md")
    ).lower()
    missing = [
        term for term in manifest["required_governance_terms"]
        if term.lower() not in documents
    ]
    assert not missing, f"missing governance invariants: {missing}"


def test_gate_does_not_claim_production_readiness():
    document = (ROOT / "docs/governance/ELO_BASELINE_EVIDENCE_GATE.md").read_text(
        encoding="utf-8"
    ).lower()
    assert "does not mean" in document
    assert "production ready" in document
    assert "baseline v1.0 frozen" in document
