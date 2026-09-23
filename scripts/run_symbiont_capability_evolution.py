#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from elo.cognitive.symbiont_capability_evolution import CapabilityMetric, review_capabilities


def _valid_metric(item: Any) -> bool:
    if not isinstance(item, Mapping):
        return False
    if not isinstance(item.get("item"), str) or not item["item"].strip():
        return False
    if "baseline" not in item or "current" not in item:
        return False
    if not isinstance(item.get("direction"), str) or item["direction"].strip().lower() not in {"maximize", "minimize"}:
        return False
    refs = item.get("evidence_refs")
    if not isinstance(refs, (list, tuple)) or not refs or any(not str(ref).strip() for ref in refs):
        return False
    period = item.get("measurement_period")
    return isinstance(period, str) and bool(period.strip())


def metrics_from_production_runs(runs: Sequence[Mapping[str, Any]]) -> tuple[CapabilityMetric, ...]:
    """Consume only explicit capability metrics emitted by governed production runs."""
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
            metrics.append(CapabilityMetric(
                item=str(item["item"]),
                baseline=float(item["baseline"]) if item["baseline"] is not None else None,
                current=float(item["current"]) if item["current"] is not None else None,
                direction=str(item["direction"]),
                evidence_refs=refs,
                measurement_period=str(item["measurement_period"]),
            ))
    return tuple(metrics)


def metric_feed_diagnostics(runs: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    runs_with_metrics = valid_metrics = rejected_metrics = 0
    for run in runs:
        details = run.get("details")
        report = details.get("report") if isinstance(details, Mapping) else None
        raw_metrics = report.get("capability_metrics") if isinstance(report, Mapping) else None
        if not isinstance(raw_metrics, list):
            continue
        if raw_metrics:
            runs_with_metrics += 1
        for item in raw_metrics:
            if _valid_metric(item):
                valid_metrics += 1
            else:
                rejected_metrics += 1
    return {
        "runs_with_capability_metrics": runs_with_metrics,
        "valid_metrics": valid_metrics,
        "rejected_metrics": rejected_metrics,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--production-runs", default="")
    args = parser.parse_args()
    payload = json.loads(Path(args.report).read_text(encoding="utf-8"))
    feed_diagnostics = {"runs_with_capability_metrics": 0, "valid_metrics": 0, "rejected_metrics": 0}
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
            feed_diagnostics = metric_feed_diagnostics(runs)
            metrics = metrics_from_production_runs(runs)
    review = review_capabilities(metrics=metrics, evidence_refs=tuple(payload.get("evidence_refs", ())))
    output = {
        "trigger_id": review.trigger_id,
        "status": review.status,
        "canonical_mutation": review.canonical_mutation,
        "metrics": [
            {"item": m.item, "baseline": m.baseline, "current": m.current, "delta": m.delta,
             "direction": m.direction, "evidence_refs": list(m.evidence_refs),
             "measurement_period": m.measurement_period}
            for m in review.metrics
        ],
        "actions": [
            {"item": a.item, "exact_action": a.exact_action, "priority": a.priority,
             "start_here": a.start_here, "rationale": a.rationale}
            for a in review.actions
        ],
        "evidence_refs": list(review.evidence_refs),
        "production_feed": feed_diagnostics,
    }
    print(json.dumps(output, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
