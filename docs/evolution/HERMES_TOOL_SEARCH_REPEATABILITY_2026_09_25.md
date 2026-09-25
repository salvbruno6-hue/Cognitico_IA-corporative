# Hermes Tool Search — Repeatability

## Candidate

- Candidate: `EXT-TOOL-SEARCH-HERMES`
- Owner: `ELO Model/Tool Routing`
- State: `candidate_only`
- Canonical mutation: `false`

## Reused mechanisms

This stage reuses the existing `hermes_tool_search_measurement` and
`hermes_tool_search_quality` contracts. No second router, registry, memory
authority, or promotion authority is introduced.

## Controlled repeatability result

Three deterministic quality runs were evaluated together with the existing
representation-footprint probe:

| Metric | Result |
|---|---:|
| Quality runs | 3/3 equivalent |
| Quality regressions | 0 |
| Unreachable selections | 0 |
| Representation reduction | 90% |
| Footprint repeatability | PASS |
| Overall repeatability | PASS |
| Technical result | `EVOLUTION_GATE_REQUIRED` |

The 90% value remains a controlled representation-footprint metric, not a
production token-savings claim.

## Governance interpretation

The candidate now has a deterministic chain of evidence: measured footprint
reduction, task-quality equivalence, and repeatability. The existing candidate
measurement semantics therefore reach `EVOLUTION_GATE_REQUIRED`.

This is not canonical promotion and does not authorize production deployment.
The next stage is the existing Evolution Gate followed by explicit ELO review.

## Loop position

`MEASUREMENT → TASK-QUALITY VALIDATION → REPEATABILITY ✓ → EVOLUTION GATE → ELO REVIEW`
