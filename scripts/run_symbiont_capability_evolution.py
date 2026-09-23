#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from elo.cognitive.symbiont_capability_evolution import CapabilityMetric, review_capabilities


def _valid_metric(item: Any) -> bool:
    return (
        isinstance(item, Mapping)
        and isinstance(item.get("item"), str)
        and "baseline" in item
        and "current" in item
        and isinstance(item.get("direction"), str)
        and isinstance(item.get("evidence_refs"), (list, tuple))
        and isinstance(item.get("measurement_period"), str)
    )


def metrics_from_production_runs(runs: Sequence[Mapping[str, Any]]) -> tuple[CapabilityMetric, ...]:
    """Reuse capability metrics already emitted by governed production runs.

    This is an adapter, not a measurement engine. Only metrics explicitly
    emitted under details.report.capability_metrics are consumed. Operational
    counters are never promoted into capability metrics implicitly.
    """
    metrics: list[CapabilityMetric] = []
    for run in runs:
        details = run.get("details")
        if not isinstance(details, Mapping):
            continue
        report = details.get("report")
        if not isinstance(report, Mapping):
            continue
        raw_metrics = report.get("capability_metrics")
        if not isinstance(raw_metrics, list):
            continue
        run_id = str(run.get("id", ""))
        for item in raw_metrics:
            if not _valid_metric(item):
                continue
            refs = tuple(str(ref) for ref in item["evidence_refs"])
            if run_id:
                refs = tuple(dict.fromkeys((*refs, f"elo_automation_runs:{run_id}")))
            metrics.append(
                CapabilityMetric(
                    item=str(item["item"]),
                    baseline=float(item["baseline"]) if item["baseline"] is not None else None,
                    current=float(item["current"]) if item["current"] is not None else None,
                    direction=str(item["direction"]),
                    evidence_refs=refs,
                    measurement_period=str(item["measurement_period"]),
                )
            )
    return tuple(metrics)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--production-runs", default="")
    args = parser.parse_args()

    payload = json.loads(Path(args.report).read_text(encoding="utf-8"))

    metrics = tuple(
        CapabilityMetric(
            item=str(item["item"]),
            baseline=item.get("baseline"),
            current=item.get("current"),
            direction=str(item.get("direction", "")),
            evidence_refs=tuple(item.get("evidence_refs", ())),
            measurement_period=str(item.get("measurement_period", "")),
        )
        for item in payload.get("capability_metrics", [])
    )

    if args.production_runs:
        runs = json.loads(Path(args.production_runs).read_text(encoding="utf-8"))
        if isinstance(runs, list):
            metrics = metrics_from_production_runs(runs)

    review = review_capabilities(
        metrics=metrics,
        evidence_refs=tuple(payload.get("evidence_refs", ())),
    )
    output = {
        "trigger_id": review.trigger_id,
        "status": review.status,
        "canonical_mutation": review.canonical_mutation,
        "metrics": [
            {
                "item": m.item,
                "baseline": m.baseline,
                "current": m.current,
                "delta": m.delta,
                "direction": m.direction,
                "evidence_refs": list(m.evidence_refs),
                "measurement_period": m.measurement_period,
            }
            for m in review.metrics
        ],
        "actions": [
            {
                "item": a.item,
                "exact_action": a.exact_action,
                "priority": a.priority,
                "start_here": a.start_here,
                "rationale": a.rationale,
            }
            for a in review.actions
        ],
        "evidence_refs": list(review.evidence_refs),
    }
    print(json.dumps(output, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
