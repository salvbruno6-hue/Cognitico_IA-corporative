from pathlib import Path


def test_audit_solidification_contract_covers_remaining_live_gates() -> None:
    path = Path("docs/evolution/AUDIT_SOLIDIFICATION_GATE_2026-09-07.md")
    text = path.read_text(encoding="utf-8")

    required = (
        "SESSION → GITHUB IDENTITY → ELO OPERATOR → CAPABILITY → SCOPE",
        "CALCULATION → EVIDENCE → RESULT → EXPERIENCE → EVALUATION → LEARNING CANDIDATE → GOVERNED LEARNING → EVOLUTION GATE",
        "LAB_ONLY",
        "ExecutionRouter",
        "no expired session is considered active",
        "95 calculations currently have no linked row",
    )
    for phrase in required:
        assert phrase in text
