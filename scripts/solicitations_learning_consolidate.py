"""Consolidate admitted solicitation learning records into candidates."""
from __future__ import annotations
import hashlib
import json
from collections import defaultdict
from pathlib import Path

EVOLUTION = Path("memory/evolution")
OUTPUT = Path("memory/solicitations_learning")

def _normalize(value: str) -> str:
    return " ".join(value.lower().split())

def _candidate_id(normalized: str) -> str:
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:24]

def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    groups: dict[str, list[dict]] = defaultdict(list)
    for path in sorted(EVOLUTION.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if record.get("domain") != "ANALISE_SOLICITACOES":
            continue
        content = record.get("content")
        if not isinstance(content, str) or not content.strip():
            continue
        groups[_normalize(content)].append(record)

    index = []
    for normalized, records in sorted(groups.items()):
        candidate = {
            "learning_id": f"sol-learning:{_candidate_id(normalized)}",
            "category": "LEARNING_CANDIDATE" if len(records) > 1 else "PRECEDENT",
            "statement": records[0]["content"],
            "recurrence_count": len(records),
            "solicitation_ids": sorted({r.get("source_id") for r in records if r.get("source_id")}),
            "evidence_refs": [r.get("evolution_id") for r in records if r.get("evolution_id")],
            "status": "CAPTURED",
        }
        (OUTPUT / f"{candidate['learning_id'].replace(':', '_')}.json").write_text(
            json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        index.append(candidate)

    (OUTPUT / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"candidates={len(index)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
