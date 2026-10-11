"""Run the Symbiont deep capability filter in controlled CI.

No business operation, Hermes invocation, promotion, deployment, or canonical
mutation is performed here.
"""
from __future__ import annotations

import json

from elo.agent_intake.symbiont_capability_filter import FilterDisposition
from elo.agent_intake.symbiont_filtered_candidates import run_filtered_candidate_evaluation


def main() -> int:
    decisions = run_filtered_candidate_evaluation()
    payload = [
        {
            "candidate_id": item.candidate_id,
            "disposition": item.disposition.value,
            "owner_preserved": item.owner_preserved,
            "objective_preserved": item.objective_preserved,
            "functional_gain_proven": item.functional_gain_proven,
            "reasons": item.reasons,
        }
        for item in decisions
    ]
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if decisions and all(
        item.disposition is FilterDisposition.ACCEPT for item in decisions
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
