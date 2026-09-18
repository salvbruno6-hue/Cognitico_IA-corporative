from pathlib import Path

CONTRACT = Path(__file__).parents[2] / "docs/architecture/ELO_SCAN_INVESTIGATION_GATE.md"


def test_scan_investigation_gate_is_explicit():
    text = CONTRACT.read_text(encoding="utf-8")
    for marker in (
        "REQUEST",
        "OBJECTIVE",
        "HYPOTHESES / PROBABILITIES",
        "RELATION / CASCADE INVESTIGATION",
        "EVIDENCE",
        "COHERENCE TEST",
        "CONCEPT CLASSIFICATION",
        "LEARNING GOVERNANCE",
        "NO OBJECTIVE → NO INVESTIGATION",
        "NO EVIDENCE → NO LEARNING",
        "NO GOVERNANCE → NO PROMOTION",
    ):
        assert marker in text


def test_scan_gate_requires_cross_domain_cascade_investigation():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "DEMANDA" in text
    assert "ALMOXARIFADO" in text
    assert "FORNECEDOR" in text
    assert "ORÇAMENTO" in text
