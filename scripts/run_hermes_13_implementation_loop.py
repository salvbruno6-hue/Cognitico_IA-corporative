"""Execute the governed Hermes 13 implementation loop in CI.

This is a controlled evidence execution only. It does not authorize promotion,
production deployment, or canonical mutation.
"""
from __future__ import annotations
import json
from elo.agent_intake.hermes_13_implementation_loop import run_hermes_13_implementation_loop

def main() -> int:
    report = run_hermes_13_implementation_loop()
    payload = {
        "candidate_count": len(report.results),
        "all_candidates_processed": report.all_candidates_processed,
        "authorization_pending": list(report.authorization_pending),
        "results": [
            {
                "candidate_id": item.candidate_id,
                "result": item.result,
                "next_state": item.next_state,
                "canonical_mutation": item.canonical_mutation,
                "evidence_present": item.evidence_present,
            }
            for item in report.results
        ],
        "promotion_authorized": False,
        "production_execution": False,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    if not report.all_candidates_processed:
        return 1
    if any(item.canonical_mutation for item in report.results):
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
