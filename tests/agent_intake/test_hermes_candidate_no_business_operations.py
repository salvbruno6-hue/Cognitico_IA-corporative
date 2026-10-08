import ast
from pathlib import Path

CANDIDATE_FILES = (
    Path("src/elo/agent_intake/hermes_model_capability_metadata.py"),
    Path("src/elo/agent_intake/hermes_session_writer_registry.py"),
)

FORBIDDEN_IMPORT_ROOTS = {
    "requests", "httpx", "urllib", "socket", "subprocess", "supabase",
    "psycopg", "psycopg2", "sqlalchemy",
}


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


def test_candidate_contracts_do_not_expose_business_operation_verbs():
    forbidden = {"execute", "persist", "write", "route", "dispatch", "merge", "promote"}
    for path in CANDIDATE_FILES:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        functions = {node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        assert not (functions & forbidden), (path, functions)
