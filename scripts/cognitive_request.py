"""Entrada do workflow cognitivo via issue.

Aceita:
  - JSON block (retrocompatível)
  - Linguagem natural (protocolo ELO)

Refs: ELO-NATURAL-LANGUAGE-PROTOCOL, ADR-0014, ADR-0015.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from elo.cognitive.runtime.bootstrap import build_default_crl
from elo.cognitive.runtime.crl import CRLContext
from elo.cognitive.runtime.intake.natural_language import parse_natural_request
from elo.cognitive.runtime.humanization.humanizer import Humanizer


def parse_issue_body(body: str) -> dict[str, Any]:
    return parse_natural_request(body)


def _attach_human_response(result: dict) -> dict:
    """Adiciona campo 'human_response' ao resultado."""
    try:
        humanizer = Humanizer()
        result["human_response"] = humanizer.humanize(result)
    except Exception as exc:
        result["human_response"] = (
            "Houve uma falha ao formatar a resposta. "
            "O resultado bruto permanece disponível."
        )
        result["humanization_error"] = str(exc)
    return result


def run_cognitive_request(payload: dict[str, Any]) -> dict[str, Any]:
    if "error" in payload:
        return _attach_human_response(payload)

    intent = payload.get("intent")

    if intent == "o_que_sabe":
        from elo.cognitive.runtime.knowledge.so_resolver import SOResolver
        resolver = SOResolver()
        return _attach_human_response({
            "intent": intent,
            "so_context": resolver.resolve(payload.get("so_id", "")),
        })

    if intent == "status_decisao":
        from elo.cognitive.runtime.store.memory_store import DecisionStore
        lifecycle = DecisionStore().load(payload.get("decision_id", ""))
        if lifecycle is None:
            return _attach_human_response({
                "intent": intent,
                "found": False,
            })
        return _attach_human_response({
            "intent": intent,
            "found": True,
            "state": lifecycle.state.value,
            "decision_id": lifecycle.decision.decision_id,
        })

    if intent == "lista_abertas":
        from elo.cognitive.runtime.store import paths
        decisions_dir = paths.DECISIONS_DIR
        items = []
        if decisions_dir.exists():
            for d in decisions_dir.iterdir():
                p = d / "lifecycle.json"
                if p.exists():
                    data = json.loads(p.read_text(encoding="utf-8"))
                    if data.get("state") in payload.get("state_filter", []):
                        items.append({
                            "decision_id": data.get("canonical_key"),
                            "state": data.get("state"),
                        })
        return _attach_human_response({
            "intent": intent,
            "count": len(items),
            "items": items,
        })

    request_id = payload.get("request_id", "issue-request")
    ctx = CRLContext(request_id=request_id)
    ctx.payload.update(payload)

    crl = build_default_crl()
    result = crl.run(ctx)

    return _attach_human_response({
        "request_id": request_id,
        "intent": intent,
        "decision_id": result.stage_results.get("decision_id"),
        "final_state": (
            result.stage_results["lifecycle"].state.value
            if "lifecycle" in result.stage_results
            else None
        ),
        "escalation": result.stage_results.get("escalation"),
        "decision_brief": result.stage_results.get("decision_brief"),
        "delta": (
            result.stage_results["delta"].to_dict()
            if result.stage_results.get("delta") is not None
            else None
        ),
        "directives": (
            [d.to_dict() for d in result.stage_results["delta"].directives]
            if result.stage_results.get("delta") is not None
            and hasattr(result.stage_results["delta"], "directives")
            else []
        ),
        "stages": result.audit,
    })


def main() -> int:
    body = os.environ.get("ISSUE_BODY", "")
    output_path = Path(os.environ.get("OUTPUT_PATH", "cognitive_result.json"))

    try:
        payload = parse_issue_body(body)
        result = run_cognitive_request(payload)
    except Exception as exc:
        result = _attach_human_response({
            "error": str(exc),
            "request_id": "issue-request",
        })
        output_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    output_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
