"""Entrada do workflow cognitivo via issue.

Lê payload da issue, roda CRL, devolve delta.

Refs: ADR-0014, ADR-0015.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from elo.cognitive.runtime.bootstrap import build_default_crl
from elo.cognitive.runtime.crl import CRLContext


def parse_issue_body(body: str) -> dict[str, Any]:
    start = body.find("<!-- elo-request-payload")
    end = body.find("-->", start)
    if start == -1 or end == -1:
        return {"question": body.strip()}

    raw = body[start + len("<!-- elo-request-payload"):end].strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"payload inválido: {exc}") from exc


def run_cognitive_request(payload: dict[str, Any]) -> dict[str, Any]:
    request_id = payload.get("request_id", "issue-request")
    ctx = CRLContext(request_id=request_id)
    ctx.payload.update(payload)

    crl = build_default_crl()
    result = crl.run(ctx)

    return {
        "request_id": request_id,
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
        "stages": result.audit,
    }


def main() -> int:
    body = os.environ.get("ISSUE_BODY", "")
    output_path = Path(os.environ.get("OUTPUT_PATH", "cognitive_result.json"))

    try:
        payload = parse_issue_body(body)
        result = run_cognitive_request(payload)
    except Exception as exc:
        result = {"error": str(exc), "request_id": "issue-request"}
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
