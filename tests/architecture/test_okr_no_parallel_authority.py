import ast
from pathlib import Path


FORBIDDEN_CLASS_NAMES = {
    "OkrOrchestrator",
    "OKRRouter",
    "OkrEvidenceRepository",
    "OkrLearningEngine",
    "OkrSymbiont",
    "OkrDecisionLifecycle",
}


def _defined_classes(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    }


def test_okr_integration_does_not_define_parallel_authorities():
    root = Path("src/elo")
    violations = []
    for path in root.rglob("*.py"):
        forbidden = _defined_classes(path) & FORBIDDEN_CLASS_NAMES
        violations.extend(f"{path}:{name}" for name in sorted(forbidden))

    assert violations == [], "parallel OKR authorities found: " + ", ".join(violations)


def test_okr_bridge_names_do_not_count_as_parallel_authorities():
    bridge = Path("src/elo/application/use_cases/okr_symbiont_bridge.py")
    classes = _defined_classes(bridge)

    assert "OkrSymbiontBridge" in classes
    assert "OkrSymbiont" not in classes
    assert classes.isdisjoint(FORBIDDEN_CLASS_NAMES)
