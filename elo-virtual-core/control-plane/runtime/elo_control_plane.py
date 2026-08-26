"""Runtime do ELO Control Plane.

O ELO é o orquestrador; interfaces periféricas apenas submetem solicitações.
Sem credenciais embutidas: integrações recebem segredos por ambiente.
"""
from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"


@dataclass
class Decision:
    request_id: str
    decision: str
    route: str
    operation: str
    reason: str
    evidence_required: bool = True


class PolicyError(Exception):
    pass


class Policy:
    def __init__(self, path: Path | None = None):
        self.path = path or CONFIG / "permission_policy.json"
        self.data = json.loads(self.path.read_text(encoding="utf-8"))

    def authorize(self, principal: str, operation: str, source: str | None = None) -> bool:
        if self.data.get("default_decision") == "deny" and not source:
            raise PolicyError("source_required")
        operations = self.data.get("operations", {})
        rule = operations.get(operation, {"default": "deny"})
        if rule.get("default") == "deny":
            raise PolicyError(f"operation_denied:{operation}")
        if source:
            src = self.data.get("sources", {}).get(source)
            if not src or operation not in src.get("allowed_operation", []):
                raise PolicyError(f"source_not_authorized:{source}:{operation}")
        return True


class ELOControlPlane:
    def __init__(self):
        self.policy = Policy()

    def classify(self, text: str) -> str:
        terms = text.lower()
        operational = (
            "taxonomia", "mlt", "m01", "m02", "kit", "lista mãe",
            "material", "modelo", "dimensão", "estrutura modular",
            "estrutura modular", "supabase", "elo-forge"
        )
        return "supabase_elo_forge" if any(t in terms for t in operational) else "local"

    def plan(self, text: str, operation: str = "read") -> dict[str, Any]:
        route = self.classify(text)
        if route == "supabase_elo_forge":
            self.policy.authorize("elo_core", operation, route)
        return {"route": route, "operation": operation, "query": text}

    def handle(self, text: str, operation: str = "read") -> dict[str, Any]:
        request_id = str(uuid.uuid4())
        plan = self.plan(text, operation)
        result = Decision(request_id, "authorized", plan["route"], operation,
                          "ELO classified and routed the request")
        return {"request_id": request_id, "decision": asdict(result), "plan": plan}


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(prog="elo")
    sub = parser.add_subparsers(dest="command", required=True)
    q = sub.add_parser("query")
    q.add_argument("text")
    args = parser.parse_args()
    if args.command == "query":
        print(json.dumps(ELOControlPlane().handle(args.text), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
