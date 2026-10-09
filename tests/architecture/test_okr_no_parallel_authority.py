from pathlib import Path


FORBIDDEN_SYMBOLS = {
    "OkrOrchestrator",
    "OKRRouter",
    "OkrEvidenceRepository",
    "OkrLearningEngine",
    "OkrSymbiont",
    "OkrDecisionLifecycle",
}


def test_okr_integration_does_not_create_parallel_authority_symbols():
    root = Path("src/elo")
    violations = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for symbol in FORBIDDEN_SYMBOLS:
            if symbol in text:
                violations.append(f"{path}:{symbol}")

    assert violations == [], "parallel OKR authorities found: " + ", ".join(violations)


def test_okr_files_do_not_define_router_or_orchestrator_classes():
    root = Path("src/elo")
    violations = []
    for path in root.rglob("*okr*.py"):
        text = path.read_text(encoding="utf-8")
        if "class OkrOrchestrator" in text or "class OKRRouter" in text:
            violations.append(str(path))

    assert violations == []
