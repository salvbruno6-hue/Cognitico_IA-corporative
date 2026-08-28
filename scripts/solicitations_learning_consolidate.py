"""Extract and consolidate genuinely new budget knowledge from solicitation learning inputs."""
from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

EVOLUTION = Path("memory/evolution")
OUTPUT = Path("08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS")
SO_RE = re.compile(r"\b(?:SO\s*)?\d{1,4}[./-]\d{2,4}\b", re.I)


def _normalize(value: str) -> str:
    value = SO_RE.sub("<SO>", value)
    return re.sub(r"\s+", " ", value.strip().lower())


def _concept_key(category: str, statement: str) -> str:
    payload = f"{category.strip().lower()}|{_normalize(statement)}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def _load_json(path: Path) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _sources() -> list[dict]:
    records: list[dict] = []
    if not EVOLUTION.exists():
        return records
    for path in sorted(EVOLUTION.glob("*.json")):
        record = _load_json(path)
        if not record or record.get("domain") != "ANALISE_SOLICITACOES":
            continue
        content = record.get("content")
        if isinstance(content, str) and content.strip():
            records.append(record)
    return records


def _canonical() -> dict[str, dict]:
    result: dict[str, dict] = {}
    if not OUTPUT.exists():
        return result
    for path in sorted(OUTPUT.glob("*.json")):
        if path.name == "index.json":
            continue
        record = _load_json(path)
        if not record:
            continue
        statement = str(record.get("statement", ""))
        if statement:
            result[_concept_key(str(record.get("category", "PRECEDENT")), statement)] = record
    return result


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    records = _sources()
    canonical = _canonical()
    groups: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        category = str(record.get("category", "PRECEDENT"))
        groups[_concept_key(category, str(record["content"]).strip())].append(record)

    created: list[dict] = []
    enriched: list[dict] = []
    reused: list[dict] = []

    for concept_key, observations in sorted(groups.items()):
        first = observations[0]
        statement = str(first["content"]).strip()
        existing = canonical.get(concept_key)
        evidence_refs = sorted({str(r.get("evolution_id")) for r in observations if r.get("evolution_id")})
        solicitation_ids = sorted({str(r.get("source_id")) for r in observations if r.get("source_id")})

        if existing:
            old_evidence = set(existing.get("evidence_refs", []))
            old_sos = set(existing.get("solicitation_ids", []))
            new_evidence = sorted(set(evidence_refs) - old_evidence)
            new_sos = sorted(set(solicitation_ids) - old_sos)
            if new_evidence or new_sos:
                existing["evidence_refs"] = sorted(old_evidence | set(evidence_refs))
                existing["solicitation_ids"] = sorted(old_sos | set(solicitation_ids))
                existing["recurrence_count"] = max(int(existing.get("recurrence_count", 0)), len(existing["evidence_refs"]))
                (OUTPUT / f"{existing['learning_id'].replace(':', '_')}.json").write_text(json.dumps(existing, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                enriched.append(existing["learning_id"])
            else:
                reused.append(existing["learning_id"])
            continue

        learning_id = f"sol-learning:{concept_key}"
        candidate = {
            "learning_id": learning_id,
            "category": "LEARNING_CANDIDATE" if len(observations) > 1 else "PRECEDENT",
            "statement": statement,
            "recurrence_count": len(observations),
            "solicitation_ids": solicitation_ids,
            "evidence_refs": evidence_refs,
            "status": "CAPTURED",
            "provenance": {"source_domain": "ANALISE_SOLICITACOES", "concept_key": concept_key},
        }
        (OUTPUT / f"{learning_id.replace(':', '_')}.json").write_text(json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        created.append(candidate)

    index = sorted([*canonical.values(), *created], key=lambda x: str(x.get("learning_id", "")))
    (OUTPUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"source_observations": len(records), "new_knowledge_created": len(created), "existing_knowledge_enriched": len(enriched), "already_canonical_reused": len(reused), "productive": bool(created or enriched)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
