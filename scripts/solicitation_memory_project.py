"""Project authorized conversation events into solicitation-scoped memory.

This projection is intentionally deterministic and does not invent content. It
only uses conversation bridge events already persisted in
``events/conversations/inbox`` and records source event IDs for traceability.

A solicitation is identified canonically from patterns such as ``SO 120.26``
or ``120.26 - FUNBIO``. Localities are detected from an explicit allow-list;
unknown localities are never inferred.
"""

from __future__ import annotations

import json
import re
from collections import OrderedDict
from pathlib import Path

INBOX = Path("events/conversations/inbox")
ROOT = Path("memory/solicitations")
INDEX = ROOT / "index.json"

LOCALITIES = OrderedDict(
    [
        ("BOA_VISTA_RR", ("BOA VISTA", "RR")),
        ("BRASILIA_DF", ("BRASÍLIA", "BRASILIA", "DF")),
        ("LORENA_SP", ("LORENA", "SP")),
        ("SEROPEDICA_RJ", ("SEROPÉDICA", "SEROPEDICA", "RJ")),
        ("MACAPA_AP", ("MACAPÁ", "MACAPA", "AP")),
    ]
)

SO_PATTERNS = (
    re.compile(r"\bSO\s*[-.:]?\s*(\d{1,4})\s*\.\s*(\d{2,4})\b", re.I),
    re.compile(r"\bsolicita(?:c|ç)[aã]o\s+(\d{1,4})\s*\.\s*(\d{2,4})\b", re.I),
)


def canonical_so(text: str) -> str | None:
    for pattern in SO_PATTERNS:
        match = pattern.search(text)
        if match:
            return f"{int(match.group(1))}.{match.group(2)}"
    return None


def detect_localities(text: str) -> list[str]:
    upper = text.upper()
    found: list[str] = []
    for key, aliases in LOCALITIES.items():
        if any(alias in upper for alias in aliases):
            found.append(key)
    return found


def load_events() -> list[dict]:
    events: list[dict] = []
    if not INBOX.exists():
        return events
    for path in sorted(INBOX.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if payload.get("authorized") is not True:
            continue
        payload["_path"] = str(path)
        events.append(payload)
    return events


def build_projection(events: list[dict], solicitation_id: str) -> dict:
    selected = [e for e in events if canonical_so(e.get("content", "")) == solicitation_id]
    # Also accept an explicit correlation/source title containing the canonical ID.
    if not selected:
        selected = [
            e for e in events
            if solicitation_id in " ".join(
                str(e.get(field, "")) for field in ("source_id", "correlation_id", "request_id")
            )
        ]

    localities: OrderedDict[str, dict] = OrderedDict()
    for event in selected:
        for locality in detect_localities(event.get("content", "")):
            localities.setdefault(
                locality,
                {"id": locality, "events": [], "event_count": 0},
            )
            localities[locality]["events"].append(event.get("source_id", event.get("_path")))
            localities[locality]["event_count"] += 1

    return {
        "solicitation_id": solicitation_id,
        "canonical_key": f"SO_{solicitation_id.replace('.', '_')}",
        "source": "authorized_conversation_bridge",
        "event_count": len(selected),
        "localities": list(localities.values()),
        "source_events": [e.get("source_id", e.get("_path")) for e in selected],
    }


def write_projection(projection: dict) -> None:
    solicitation_id = projection["solicitation_id"]
    target_dir = ROOT / f"SO_{solicitation_id.replace('.', '_')}"
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "index.json").write_text(
        json.dumps(projection, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        f"# SO {solicitation_id}",
        "",
        "Memória projetada exclusivamente de eventos de conversa autorizados.",
        "O conteúdo não é enriquecido por inferência; cada dado deve manter sua origem no evento.",
        "",
        "## Localidades identificadas",
    ]
    for locality in projection["localities"]:
        lines.append(f"- {locality['id']}: {locality['event_count']} evento(s)")
    lines.extend(["", "## Eventos de origem"])
    for source in projection["source_events"]:
        lines.append(f"- `{source}`")
    (target_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_global_index(projection: dict) -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    current: list[dict] = []
    if INDEX.exists():
        try:
            current = json.loads(INDEX.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            current = []
    by_id = {item.get("solicitation_id"): item for item in current}
    by_id[projection["solicitation_id"]] = {
        "solicitation_id": projection["solicitation_id"],
        "path": f"SO_{projection['solicitation_id'].replace('.', '_')}/index.json",
        "event_count": projection["event_count"],
        "localities": [item["id"] for item in projection["localities"]],
    }
    INDEX.write_text(
        json.dumps(sorted(by_id.values(), key=lambda item: item["solicitation_id"]), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    events = load_events()
    solicitation_ids = sorted({canonical_so(e.get("content", "")) for e in events if canonical_so(e.get("content", ""))})
    for solicitation_id in solicitation_ids:
        projection = build_projection(events, solicitation_id)
        write_projection(projection)
        update_global_index(projection)
        print(f"projected SO {solicitation_id}: events={projection['event_count']} localities={len(projection['localities'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
