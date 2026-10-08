import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANDIDATE_FILES = (
    REPO_ROOT / "src/elo/agent_intake/hermes_model_capability_metadata.py",
    REPO_ROOT / "src/elo/agent_intake/hermes_session_writer_registry.py",
)

FORBIDDEN_IMPORT_ROOTS = {
    "requests", "httpx", "urllib", "socket", "subprocess", "supabase",
    "psycopg", "psycopg2", "sqlalchemy",
}

FORBIDDEN_CALL_ROOTS = {
    "requests", "httpx", "urllib", "socket", "subprocess", "supabase",
    "psycopg", "psycopg2", "sqlalchemy",
}


def _root_name(call):
    node = call.func
    while isinstance(node, ast.Attribute):
        node = node.value
    return node.id if isinstance(node, ast.Name) else None


def test_candidate_contracts_have_no_external_or_persistence_imports():
    for path in CANDIDATE_FILES:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported_roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])
        assert not (imported_roots & FORBIDDEN_IMPORT_ROOTS), (path, imported_roots)


def test_candidate_contracts_do_not_call_external_or_persistence_clients():
    for path in CANDIDATE_FILES:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        call_roots = {_root_name(node) for node in ast.walk(tree) if isinstance(node, ast.Call)}
        call_roots.discard(None)
        assert not (call_roots & FORBIDDEN_CALL_ROOTS), (path, call_roots)
