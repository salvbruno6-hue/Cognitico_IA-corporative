#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from elo.cognitive.symbiont_capability_evolution import diagnose_capability_status


def _bool(payload: Mapping[str, Any], key: str) -> bool:
    value = payload.get(key)
    if not isinstance(value, bool):
        raise ValueError(f"{key} must be an explicit boolean")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Symbiont capability status diagnosis.")
    parser.add_argument("--input", required=True, help="JSON status input")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("input must be a JSON object")

    report = diagnose_capability_status(
        capability_id=str(payload["capability_id"]),
        capability_name=str(payload["capability_name"]),
        owner=str(payload["owner"]),
        authority=str(payload["authority"]),
        contract_present=_bool(payload, "contract_present"),
        implementation_present=_bool(payload, "implementation_present"),
        tests_present=_bool(payload, "tests_present"),
        evidence_present=_bool(payload, "evidence_present"),
        runtime_integrated=_bool(payload, "runtime_integrated"),
        operational_evidence=_bool(payload, "operational_evidence"),
        production_outcome=_bool(payload, "production_outcome"),
        governance_approved=bool(payload.get("governance_approved", False)),
        contract_refs=tuple(payload.get("contract_refs", ())),
        implementation_refs=tuple(payload.get("implementation_refs", ())),
        test_refs=tuple(payload.get("test_refs", ())),
        evidence_refs=tuple(payload.get("evidence_refs", ())),
        runtime_refs=tuple(payload.get("runtime_refs", ())),
        operational_refs=tuple(payload.get("operational_refs", ())),
        production_refs=tuple(payload.get("production_refs", ())),
        governance_refs=tuple(payload.get("governance_refs", ())),
        blockers=tuple(payload.get("blockers", ())),
    )
    print(json.dumps(report.as_dict(), ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
