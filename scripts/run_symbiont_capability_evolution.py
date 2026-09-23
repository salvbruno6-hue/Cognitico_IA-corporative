#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
from elo.cognitive.symbiont_capability_evolution import CapabilityMetric, review_capabilities

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.report).read_text(encoding='utf-8'))
    metrics = tuple(CapabilityMetric(item=str(item['item']), baseline=item.get('baseline'), current=item.get('current'), direction=str(item.get('direction', '')), evidence_refs=tuple(item.get('evidence_refs', ())), measurement_period=str(item.get('measurement_period', ''))) for item in payload.get('capability_metrics', []))
    review = review_capabilities(metrics=metrics, evidence_refs=tuple(payload.get('evidence_refs', ())))
    output = {'trigger_id': review.trigger_id, 'status': review.status, 'canonical_mutation': review.canonical_mutation, 'metrics': [{'item':m.item,'baseline':m.baseline,'current':m.current,'delta':m.delta,'direction':m.direction,'evidence_refs':list(m.evidence_refs),'measurement_period':m.measurement_period} for m in review.metrics], 'actions': [{'item':a.item,'exact_action':a.exact_action,'priority':a.priority,'start_here':a.start_here,'rationale':a.rationale} for a in review.actions], 'evidence_refs': list(review.evidence_refs)}
    print(json.dumps(output, ensure_ascii=False, separators=(',', ':')))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
