"""ELO APRENDER — cognitive consolidation for Análise de Solicitações.

Primary source: the GPT project/data source named "Análise de Solicitações".
Canonical destination: 08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/.
Git stores cognitive knowledge; Supabase stores quantitative calculation memory.
memory/evolution is auxiliary history/evidence and never replaces source investigation.

IMPORTANT: "Análise de Solicitações" is a project/source boundary, not a
repository directory. The executor must receive/access that project source
through its mounted/runtime source adapter. It must not fall back to Dropbox or
invent a repository path as the primary source.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS"
EVOLUTION = ROOT / "memory/evolution"

# Runtime adapter: the project "Análise de Solicitações" is the authoritative
# source. Its actual mounted path is supplied by the host/runtime, rather than
# inferred from GitHub, Dropbox, or an arbitrary repository directory.
PROJECT_SOURCE_ENV = "ELO_ANALISE_SOLICITACOES_ROOT"
SOURCE_PROJECT_NAME = "Análise de Solicitações"

CALCULATION_CHAIN = (
    "input", "source", "premise", "formula", "subcalculation", "result", "validation"
)


def _normalize(value: str) -> str:
    return " ".join(value.lower().split())


def _candidate_id(normalized: str) -> str:
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:24]


def _source_root() -> Path | None:
    """Resolve the GPT project source only through the runtime adapter."""
    configured = os.environ.get(PROJECT_SOURCE_ENV, "").strip()
    if not configured:
        return None
    candidate = Path(configured).expanduser()
    return candidate if candidate.exists() else None


def _source_files() -> list[Path]:
    root = _source_root()
    if root is None:
        return []
    if root.is_file():
        return [root]
    return sorted(p for p in root.rglob("*") if p.is_file())


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _extract_so(text: str, fallback: str = "") -> str:
    match = re.search(r"\bSO\s*[-_/]?(\d{1,4})(?:[./_-](\d{2,4}))?\b", text, re.I)
    if not match:
        match = re.search(r"\b(\d{1,4})[./](?:26|2026)\b", text, re.I)
    if not match:
        return fallback
    return f"SO {match.group(1)}.{match.group(2) or '26'}"


def _calculation_candidates(text: str) -> list[dict]:
    """Capture explicit quantitative evidence; never invent a formula or result."""
    patterns = (
        r"[^\n]{0,180}\b\d+(?:[.,]\d+)?\s*[×x*÷/]\s*\d+(?:[.,]\d+)?[^\n]{0,180}",
        r"[^\n]{0,180}\b\d+(?:[.,]\d+)?\s*(?:m²|m2|m|un\.?|ponto|dias?|meses?|R\$)[^\n]{0,180}",
    )
    found: list[dict] = []
    seen: set[str] = set()
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.I):
            raw = " ".join(match.group(0).split())
            if raw not in seen:
                seen.add(raw)
                found.append({"raw": raw})
    return found


def _scan_primary_sources() -> list[dict]:
    records = []
    source_root = _source_root()
    if source_root is None:
        return records
    for path in _source_files():
        text = _read_text(path)
        if not text.strip():
            continue
        relative = str(path.relative_to(source_root))
        records.append({
            "so": _extract_so(text, path.parent.name),
            "source": relative,
            "source_project": SOURCE_PROJECT_NAME,
            "source_type": path.suffix.lower().lstrip("."),
            "source_hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "text_length": len(text),
            "calculation_candidates": _calculation_candidates(text),
        })
    return records


def _load_existing_concepts() -> dict[str, dict]:
    concepts: dict[str, dict] = {}
    if not OUTPUT.exists():
        return concepts
    for path in OUTPUT.rglob("*.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        values = payload if isinstance(payload, list) else [payload]
        for item in values:
            if not isinstance(item, dict):
                continue
            statement = item.get("statement") or item.get("title") or item.get("concept")
            if statement:
                concepts[_candidate_id(_normalize(str(statement)))] = item
    return concepts


def _load_evolution_auxiliary() -> list[dict]:
    records = []
    if not EVOLUTION.exists():
        return records
    for path in sorted(EVOLUTION.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if record.get("domain") == "ANALISE_SOLICITACOES":
            records.append(record)
    return records


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)

    # Primary investigation is the GPT project source. Evolution Memory is
    # auxiliary evidence only and cannot substitute the primary investigation.
    source_root = _source_root()
    primary_records = _scan_primary_sources()
    auxiliary_records = _load_evolution_auxiliary()
    existing = _load_existing_concepts()

    manifest = {
        "schema_version": "elo-aprender-cognitive-v4",
        "primary_source_project": SOURCE_PROJECT_NAME,
        "primary_source_adapter": PROJECT_SOURCE_ENV,
        "primary_source_status": "FOUND" if source_root else "SOURCE_NOT_ACCESSIBLE",
        "primary_source_records": primary_records,
        "auxiliary_evolution_records": len(auxiliary_records),
        "existing_concepts": len(existing),
        "git_destination": str(OUTPUT.relative_to(ROOT)),
        "git_role": "cognitive_knowledge",
        "supabase_role": "quantitative_calculation_memory",
        "calculation_chain": list(CALCULATION_CHAIN),
        "governance": [
            "CASO", "PRECEDENT", "LEARNING_CANDIDATE", "VALIDATED_LEARNING",
            "CONCEPTUAL_KNOWLEDGE", "INSTRUCTIONAL_KNOWLEDGE", "RULE",
        ],
        "rules": {
            "primary_source_is_gpt_project": True,
            "reinvestigate_existing_solicitations": True,
            "new_knowledge_requires_governance_and_persistence_confirmation": True,
            "new_calculation_requires_supabase_persistence_confirmation": True,
            "precedent_never_promoted_to_rule_automatically": True,
            "never_invent_data_formula_evidence_or_ids": True,
            "laboratory_only_when_explicitly_called": True,
            "evolution_memory_is_auxiliary": True,
            "do_not_use_dropbox_as_primary_source": True,
            "do_not_assume_repo_directory_is_project_source": True,
        },
    }

    # Auditable scan artifact. This deliberately does not simulate Supabase
    # writes or claim learning persistence before actual confirmation.
    target = OUTPUT / "_elo_cognitive_scan.json"
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": "SCAN_COMPLETED" if source_root else "SOURCE_NOT_ACCESSIBLE",
        "primary_source_project": SOURCE_PROJECT_NAME,
        "primary_source_status": manifest["primary_source_status"],
        "primary_source_files": len(primary_records),
        "calculation_candidates": sum(len(r["calculation_candidates"]) for r in primary_records),
        "existing_concepts": len(existing),
        "auxiliary_evolution_records": len(auxiliary_records),
        "supabase_persistence": "NOT_SIMULATED",
        "next_step": "governance_then_confirmed_git_and_supabase_persistence",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
