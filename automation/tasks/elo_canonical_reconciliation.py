"""Deterministic repository reconciliation for ELO canonicality gates."""
from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Iterable

DECISIONS = ("REUSE", "STRENGTHEN", "REFACTOR", "DEPRECATE", "CREATE")
CANONICAL_STRUCTURE_MAP = "02-architecture-library/ELO_REPOSITORY_CANONICAL_STRUCTURE_MAP.md"

# Bounded ownership of the EXISTING read-only live reconciliation facility.
# This is a verified owner resolution, not permission to merge or introduce a
# new authority. Anything outside these exact paths remains unclassified.
LIVE_RECONCILIATION_CONTRACT = "docs/governance/ELO_LIVE_STATE_RECONCILIATION_CONTRACT.md"
LIVE_RECONCILIATION_RUNTIME = "src/elo/infrastructure/live_state_reconciliation.py"
LIVE_RECONCILIATION_CLI = "scripts/run_live_reconciliation.py"
LIVE_RECONCILIATION_WORKFLOW = ".github/workflows/elo-live-reconciliation.yml"
LIVE_RECONCILIATION_SCOPE = frozenset({
    LIVE_RECONCILIATION_CLI,
    LIVE_RECONCILIATION_WORKFLOW,
    "tests/infrastructure/test_live_reconciliation_workflow.py",
    # Self-audit changes require the same proof and normal CI/review gates.
    "automation/tasks/elo_canonical_reconciliation.py",
    "tests/governance/test_elo_canonical_reconciliation.py",
})
SELF_AUDIT_PATHS = {
    "automation/tasks/elo_canonical_reconciliation.py",
    "automation/ELO_MAINTENANCE_COORDINATOR.md",
    "automation/tasks/elo_maintenance_coordinator.py",
}
AUDIT_INFRA_PREFIXES = (".github/", "automation/", "docs/", "tests/")
SOURCE_SUFFIXES = {".py", ".ts", ".tsx", ".js", ".jsx", ".sql", ".yml", ".yaml"}
GENERIC_CONCEPT_TERMS = {"package", "index", "config", "configuration", "readme", "test", "tests", "utils", "types", "app", "css"}
EXPLICIT_OWNER_PATTERN = re.compile(
    r"(?:canonical owner|canonical authority|source of truth)\s*:\s*([^\n#`]+)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ReconciliationEvidence:
    changed_paths: tuple[str, ...]
    candidates: tuple[str, ...]
    references: tuple[str, ...]
    owners: tuple[str, ...]
    source_of_truth: str | None
    canonical_identity: str | None
    duplicate_or_parallel: bool | None
    reuse_analysis_complete: bool
    decision: str | None
    reasons: tuple[str, ...] = field(default_factory=tuple)

    @property
    def waiting_for_evidence(self) -> bool:
        return not self.reuse_analysis_complete or self.duplicate_or_parallel is None


def _text_files(root: Path) -> Iterable[Path]:
    ignored = {".git", ".venv", "venv", "node_modules", "__pycache__"}
    for path in root.rglob("*"):
        if path.is_file() and not any(part in ignored for part in path.parts):
            try:
                if path.stat().st_size <= 1_000_000:
                    yield path
            except OSError:
                continue


def _normalise_terms(terms: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({term.strip().lower() for term in terms if term and term.strip() and term.strip().lower() not in GENERIC_CONCEPT_TERMS}))


def _is_audit_infrastructure(relative: str) -> bool:
    return relative.replace("\\", "/").startswith(AUDIT_INFRA_PREFIXES)


def _explicit_owner_targets(text: str, candidate_stems: set[str]) -> set[str]:
    """Return candidates explicitly named by an owner/source-of-truth declaration."""
    targets: set[str] = set()
    for match in EXPLICIT_OWNER_PATTERN.finditer(text):
        declared = match.group(1).strip().strip("'\"")
        declared_stem = Path(declared.replace("\\", "/")).stem.lower().replace("-", "_")
        if declared_stem in candidate_stems:
            targets.add(declared_stem)
    return targets


def _valid_live_owner_contract(text: str) -> bool:
    """Verify exact metadata in the existing contract front matter."""
    if not text.startswith("---\n"):
        return False
    header, delimiter, _ = text[4:].partition("\n---\n")
    if not delimiter:
        return False
    fields = {}
    for line in header.splitlines():
        match = re.fullmatch(r"([a-z_]+):\s*(.+?)\s*", line)
        if match:
            fields[match.group(1)] = match.group(2)
    return all(fields.get(key) == value for key, value in {
        "artifact_id": "ELO-LIVE-STATE-RECONCILIATION-CONTRACT",
        "owner": "ELO Governance",
        "family": "docs/governance",
        "layer": "governance",
        "type": "contract",
        "authority": "reference",
        "status": "defined",
    }.items())


def _cli_uses_canonical_reconciler(text: str) -> bool:
    """Inspect executable Python syntax rather than accepting comments."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    main = functions.get("main")
    exit_code = functions.get("result_exit_code")
    if main is None or exit_code is None:
        return False

    # A recognized path must have the same top-level execution sequence.
    # This rejects early PASS, dead imports and disconnected extra commands.
    expected_steps = (
        ast.Assign, ast.Assign, ast.If, ast.ImportFrom, ast.ImportFrom,
        ast.Assign, ast.Assign, ast.Try, ast.Assign, ast.Expr, ast.Return,
    )
    if tuple(type(statement) for statement in main.body) != expected_steps:
        return False
    if (
        ast.unparse(main.body[0]) != "url = os.environ.get('SUPABASE_URL', '').strip()"
        or ast.unparse(main.body[1]) != "key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', '').strip()"
        or ast.unparse(main.body[-2]) != "print(json.dumps(output, indent=2, ensure_ascii=False))"
    ):
        return False

    # Only live statements in main's direct execution path count as proof.
    # ast.walk() would also accept dead code under "if False".
    imports = {
        (node.module, name.name)
        for node in main.body if isinstance(node, ast.ImportFrom)
        for name in node.names
    }
    if not {
        ("elo.infrastructure.live_state_reconciliation", "LiveStateReconciliation"),
        ("elo.infrastructure.supabase_rls_reader", "SupabaseRLSStateReader"),
    }.issubset(imports):
        return False

    assignments = {
        node.targets[0].id: ast.unparse(node.value)
        for node in main.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
    }
    if any(assignments.get(name) != expr for name, expr in {
        "reader": "SupabaseRLSStateReader(url, key)",
        "harness": "LiveStateReconciliation()",
        "output": "report.to_dict()",
    }.items()):
        return False

    try_blocks = [node for node in main.body if isinstance(node, ast.Try)]
    if len(try_blocks) != 1 or not any(
        isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == "report"
        and ast.unparse(node.value) == "harness.reconcile(reader)"
        for node in try_blocks[0].body
    ):
        return False

    # Only the known missing-credentials guard is allowed before execution.
    guards = [node for node in main.body if isinstance(node, ast.If)]
    if len(guards) != 1 or ast.unparse(guards[0].test) != "not url or not key":
        return False
    if not guards[0].body or not isinstance(guards[0].body[-1], ast.Return):
        return False
    if ast.unparse(guards[0].body[-1].value) != "1":
        return False
    guarded_try = try_blocks[0]
    if (
        len(guarded_try.body) != 1
        or guarded_try.orelse or guarded_try.finalbody
        or len(guarded_try.handlers) != 1
    ):
        return False
    if not any(
        isinstance(stmt, ast.Return) and ast.unparse(stmt.value) == "2"
        for stmt in guarded_try.handlers[0].body
    ):
        return False
    returns = [node for node in main.body if isinstance(node, ast.Return)]
    if len(returns) != 1 or main.body[-1] is not returns[0]:
        return False

    exit_returns = [
        node for node in exit_code.body if isinstance(node, ast.Return)
    ]
    if len(exit_code.body) not in (1, 2) or not isinstance(exit_code.body[-1], ast.Return):
        return False
    if len(exit_code.body) == 2 and not (
        isinstance(exit_code.body[0], ast.Expr)
        and isinstance(exit_code.body[0].value, ast.Constant)
        and isinstance(exit_code.body[0].value.value, str)
    ):
        return False
    entrypoints = [
        node for node in tree.body if isinstance(node, ast.If)
        and ast.unparse(node.test) == "__name__ == '__main__'"
    ]
    return (
        ast.unparse(returns[0].value) == "result_exit_code(output.get('overall'))"
        and len(exit_returns) == 1
        and ast.unparse(exit_returns[0].value) == "0 if overall == 'PASS' else 3"
        and any(
            ast.unparse(statement) == "sys.exit(main())"
            for entry in entrypoints for statement in entry.body
        )
    )

def _workflow_executes_reconciler(text: str) -> bool:
    """Check the active jobs.reconcile.steps YAML path without extra packages.

    Each level must be a real mapping/list entry at its expected indentation.
    An example inside a YAML scalar or an unrelated env variable cannot pass.
    This intentionally supports only the current simple workflow structure.
    """
    def section(lines: list[str], header: str, indent: int) -> list[str]:
        marker = " " * indent + header
        matches = [i for i, line in enumerate(lines) if line == marker]
        if len(matches) != 1:
            return []
        first = matches[0]
        for last in range(first + 1, len(lines)):
            line = lines[last]
            if line.strip() and not line.lstrip().startswith("#"):
                depth = len(line) - len(line.lstrip(" "))
                if depth <= indent:
                    return lines[first + 1:last]
        return lines[first + 1:]

    root = text.splitlines()
    jobs = section(root, "jobs:", 0)
    job = section(jobs, "reconcile:", 2)
    steps = section(job, "steps:", 4)
    run_step = section(steps, "- name: Run reconciliation", 6)
    return [line.strip() for line in run_step if line.strip()] == [
        "id: reconcile",
        "run: |",
        "set -o pipefail",
        "python scripts/run_live_reconciliation.py \\",
        "| tee reconciliation_report.json",
    ]


def _verified_live_reconciliation_owner(root: Path, changed: set[str]) -> bool:
    """Recognize only the existing, connected read-only reconciliation path.

    This is ownership evidence, never merge authorization. Unknown source,
    executable wiring, or scope stays WAITING_FOR_EVIDENCE.
    """
    if LIVE_RECONCILIATION_CLI not in changed or not changed.issubset(LIVE_RECONCILIATION_SCOPE):
        return False

    contract = root / LIVE_RECONCILIATION_CONTRACT
    runtime = root / LIVE_RECONCILIATION_RUNTIME
    cli = root / LIVE_RECONCILIATION_CLI
    workflow = root / LIVE_RECONCILIATION_WORKFLOW
    structure_map = root / CANONICAL_STRUCTURE_MAP
    if not all(path.is_file() for path in (contract, runtime, cli, workflow, structure_map)):
        return False

    try:
        contract_text = contract.read_text(encoding="utf-8")
        runtime_tree = ast.parse(runtime.read_text(encoding="utf-8"))
        cli_text = cli.read_text(encoding="utf-8")
        workflow_text = workflow.read_text(encoding="utf-8")
        map_text = structure_map.read_text(encoding="utf-8")
    except (OSError, UnicodeError, SyntaxError):
        return False

    runtime_owner = [
        node for node in runtime_tree.body
        if isinstance(node, ast.ClassDef) and node.name == "LiveStateReconciliation"
    ]
    return all((
        _valid_live_owner_contract(contract_text),
        len(runtime_owner) == 1,
        bool(runtime_owner and any(
            isinstance(node, ast.FunctionDef) and node.name == "reconcile"
            for node in runtime_owner[0].body
        )),
        _cli_uses_canonical_reconciler(cli_text),
        _workflow_executes_reconciler(workflow_text),
        "| `src/elo/` | Executable ELO | current implementation core | canonical executable root |" in map_text,
    ))


def reconcile_repository(root: str | Path, changed_paths: Iterable[str], concept_terms: Iterable[str] | None = None) -> ReconciliationEvidence:
    root = Path(root)
    changed = tuple(sorted(set(changed_paths)))
    if not changed:
        return ReconciliationEvidence((), (), (), (), None, None, None, False, None, ("No changed paths supplied",))

    changed_normalised = {p.replace("\\", "/") for p in changed}
    changed_stems = {Path(p).stem.lower().replace("-", "_") for p in changed}
    terms = _normalise_terms(concept_terms or ())
    changed_in_runtime = any(p.startswith("src/elo/") for p in changed_normalised)
    all_files = list(_text_files(root))

    candidates: list[str] = []
    references: list[str] = []
    owners: list[str] = []
    owner_evidence: list[tuple[str, str]] = []
    independent_references: list[str] = []

    for path in all_files:
        relative = str(path.relative_to(root)).replace("\\", "/")
        if relative in changed_normalised:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lower = text.lower()
        path_lower = relative.lower()
        self_audit = relative in SELF_AUDIT_PATHS
        audit_infrastructure = _is_audit_infrastructure(relative)
        stem_hit = any(stem in lower or stem in path_lower for stem in changed_stems)
        concept_hit = bool(terms) and any(term in lower or term in path_lower for term in terms)
        related = stem_hit or concept_hit

        if related and not self_audit and not audit_infrastructure:
            references.append(relative)

        explicit_owner = bool(EXPLICIT_OWNER_PATTERN.search(text))
        if explicit_owner and related and not self_audit and not audit_infrastructure:
            owners.append(relative)
            owner_evidence.append((relative, lower))
        elif related and not self_audit and not audit_infrastructure:
            independent_references.append(relative)

        same_canonical_runtime = changed_in_runtime and path_lower.startswith("src/elo/")
        source_candidate = (
            not self_audit
            and not audit_infrastructure
            and not same_canonical_runtime
            and path.suffix.lower() in SOURCE_SUFFIXES
            and (path.stem.lower().replace("-", "_") in changed_stems or concept_hit)
        )
        if source_candidate:
            candidates.append(relative)

    candidates = sorted(set(candidates))
    references = sorted(set(references))
    owners = sorted(set(owners))
    independent_references = sorted(set(independent_references))
    candidate_stems = {Path(candidate).stem.lower().replace("-", "_") for candidate in candidates}
    owner_targets = {
        stem
        for _, text in owner_evidence
        for stem in _explicit_owner_targets(text, candidate_stems)
    }

    if candidate_stems.intersection(owner_targets):
        duplicate: bool | None = True
        reasons = ["Existing candidate is explicitly identified as canonical source of truth"]
    else:
        duplicate = None
        if candidates:
            reasons = ["Existing executable candidate found, but duplicate/parallel capability is not proven"]
        elif independent_references:
            reasons = ["Related runtime references found, but duplicate/parallel capability is not proven"]
        else:
            reasons = ["Duplicate state is not proven; absence is not sufficient to authorize CREATE"]

    source_of_truth = owners[0] if owners else None
    canonical_identity = next(iter(changed_stems)) if owners and len(changed_stems) == 1 else None
    structure_map = root / CANONICAL_STRUCTURE_MAP

    if changed_in_runtime and structure_map.is_file() and not owner_evidence:
        source_of_truth = CANONICAL_STRUCTURE_MAP
        canonical_identity = "src/elo"
        duplicate = False
        reasons = ["Canonical structure map resolves src/elo as the executable ELO owner"]

    maintenance_changed = all(p.replace("\\", "/") in SELF_AUDIT_PATHS for p in changed)
    if maintenance_changed and structure_map.is_file():
        source_of_truth = CANONICAL_STRUCTURE_MAP
        canonical_identity = "elo-maintenance-governance"
        duplicate = False
        reasons = ["Maintenance/governance infrastructure is audited against the repository canonical map"]

    scoped_live_reconciliation = (
        not candidates
        and not owner_evidence
        and _verified_live_reconciliation_owner(root, changed_normalised)
    )
    if scoped_live_reconciliation:
        source_of_truth = LIVE_RECONCILIATION_RUNTIME
        canonical_identity = "elo-live-state-reconciliation"
        duplicate = False
        owners.append(LIVE_RECONCILIATION_CONTRACT)
        reasons = ["Existing read-only reconciler, governance owner and workflow chain verified"]

    frontend_changed = any(p.startswith("frontend/") for p in changed_normalised)
    if frontend_changed and owners and not candidates and not maintenance_changed:
        source_of_truth = owners[0]
        canonical_identity = "frontend"
        duplicate = False
        reasons = ["Existing canonical frontend surface is being reused; no parallel executable candidate found"]

    complete = bool(canonical_identity and source_of_truth and duplicate is not None)
    decision = (
        "STRENGTHEN" if scoped_live_reconciliation and complete
        else "REUSE" if complete and duplicate
        else "CREATE" if complete
        else None
    )
    if not complete:
        reasons.append("Canonical owner/source of truth not explicitly proven" if source_of_truth is None else "Reconciliation remains WAITING_FOR_EVIDENCE")
        if source_of_truth is not None:
            reasons.append("Reconciliation remains WAITING_FOR_EVIDENCE")

    return ReconciliationEvidence(
        changed_paths=changed,
        candidates=tuple(candidates),
        references=tuple(references),
        owners=tuple(owners),
        source_of_truth=source_of_truth,
        canonical_identity=canonical_identity,
        duplicate_or_parallel=duplicate,
        reuse_analysis_complete=complete,
        decision=decision,
        reasons=tuple(dict.fromkeys(reasons)),
    )


def event_facts(evidence: ReconciliationEvidence) -> dict[str, object]:
    return {
        "canonical_identity_valid": evidence.canonical_identity is not None,
        "canonical_target_resolved": evidence.source_of_truth is not None,
        "source_of_truth_resolved": evidence.source_of_truth is not None,
        "reuse_analysis_complete": evidence.reuse_analysis_complete,
        "duplicate_or_parallel_found": evidence.duplicate_or_parallel,
        "contract_conflict": False if evidence.reuse_analysis_complete else None,
    }
