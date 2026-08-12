"""Process authorized conversation bridge events persisted in GitHub.

This is the first zero-cost persistence adapter: GitHub is the event inbox and
Evolution Memory projection. A database/vector store is deliberately not
required. The script is idempotent by conversation_id/evolution_id.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

from elo.core import EvolutionMemory, KnowledgeAdmission
from elo.core.conversation_bridge import ChatBridge, ChatBridgeEvent
from elo.core.conversation_intake import ConversationIntake

INBOX = Path("events/conversations/inbox")
EVOLUTION = Path("memory/evolution")


def main() -> int:
    EVOLUTION.mkdir(parents=True, exist_ok=True)
    memory = EvolutionMemory()
    intake = ConversationIntake(KnowledgeAdmission(), memory)
    bridge = ChatBridge(intake)
    processed = 0
    rejected = 0

    for path in sorted(INBOX.glob("*.json")):
        try:
            event = ChatBridgeEvent.from_json(path.read_text(encoding="utf-8"))
            result = bridge.ingest(event)
        except (ValueError, PermissionError, json.JSONDecodeError) as exc:
            rejected += 1
            print(f"REJECT {path}: {exc}")
            continue

        if result.evolution_id:
            record = memory.get(result.evolution_id)
            if record is not None:
                target = EVOLUTION / f"{record.evolution_id.replace(':', '_')}.json"
                target.write_text(
                    json.dumps(
                        {
                            "evolution_id": record.evolution_id,
                            "tenant_id": record.tenant_id,
                            "domain": record.domain,
                            "source_type": record.source_type,
                            "source_id": record.source_id,
                            "content": record.content,
                            "status": record.status,
                            "confidence": record.confidence,
                            "tags": record.tags,
                            "provenance": dict(record.provenance),
                            "created_at": record.created_at.isoformat(),
                        },
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                    + "\n",
                    encoding="utf-8",
                )
                processed += 1
        else:
            rejected += 1
            print(f"NO-RETENTION {path}: {result.admission.outcome} — {result.admission.reason}")

    print(f"processed={processed} rejected_or_archived={rejected}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
