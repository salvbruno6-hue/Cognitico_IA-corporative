# Hermes Tool Search → ELO refinement candidate

## Controlled deployment-loop measurement

PR #726 established the ELO-side candidate boundary and passed repository
validation. The next loop stage is measurement, not canonical promotion.

The controlled probe measures **schema representation footprint** only. It
does not invoke Hermes or execute a tool. It compares an eager representation
with a progressive representation and records whether the selected schema
remains reachable.

This is intentionally a laboratory metric, not a production-token benchmark.

### Acceptance boundary

A successful probe can establish only:

- the measurement apparatus is deterministic;
- the representation can show a footprint reduction;
- selected-tool reachability can be checked.

It cannot establish:

- model task-quality equivalence;
- production latency;
- real token savings;
- repeatability across production workloads;
- Evolution Gate approval.

Those remain required before `EXT-TOOL-SEARCH-HERMES` can leave
`candidate_only`.

### Loop state

`MERGED → MEASUREMENT → TASK-QUALITY VALIDATION → REPEATABILITY → EVOLUTION GATE → ELO REVIEW`

## Existing governance

The existing owner remains `ELO Model/Tool Routing`. No new router,
registry, memory authority, or promotion authority is introduced.
