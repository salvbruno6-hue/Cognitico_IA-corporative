# ELO Real Capability Audit Matrix

## Purpose

Use this matrix to prevent architectural claims from being confused with executable evidence.

## Evidence states

`PASS` = reproducibly executed and evidenced.
`PARTIAL` = implementation exists but end-to-end proof is incomplete.
`DEFINED` = contract/specification exists without sufficient executable proof.
`DUPLICATED` = more than one overlapping canonical candidate exists.
`BLOCKED` = required runtime/external evidence unavailable.
`HISTORICAL` = retained for provenance only.

| Test group | What must be proven | Current assessment | Next test |
|---|---|---|---|
| Identity/Boundary | One Cognitive authority; no second Core | PASS/architecturally evidenced | regression |
| Context | tenant/domain/principal/session/request/correlation | PASS | adversarial |
| Source/Provenance | authorized retrieval and continuous provenance | PASS/PARTIAL runtime | provider-unavailable |
| Memory | observation/evidence/knowledge/decision separation | PASS | admission adversarial |
| Core Loop | Context→Evidence→Diagnosis→Recommendation | PASS | end-to-end |
| Scenarios | canonical scenario ownership | DUPLICATED | #56 consolidation |
| Systemic Reasoning | cross-domain dependencies and impacts | PARTIAL/PASS | integrated fixture |
| Specialists | governed consultation and feedback | PASS/PARTIAL | genuine specialist evidence |
| Execution | authorization before irreversible action | PASS | negative paths |
| Resilience | timeout/retry/degradation/recovery | PASS deterministic / live BLOCKED | OPS evidence |
| Budgeting | SO→solution→quantity→composition→cost→validation | PARTIAL | ELO-024 fixture suite |
| Pricing | source current price and provenance | DEFINED/PARTIAL | authorized price fixtures |
| Logistics | mobilization/travel/stay/resource cost logic | DEFINED/PARTIAL | logistics fixtures |
| Budget vs Actual | outcome comparison without history mutation | DEFINED | outcome fixture |
| Learning | reusable reasoning without copying historical values | CONTRACT/PARTIAL | learning test |
| Autonomous loop | bounded continuation/correction/replan/escalation | IMPLEMENTED/CONTRACT | full-cycle test |
| Baseline v1.0 | all critical matrix evidence green | BLOCKED | #92/#156 closure |

## Decision rule

No capability may be declared fully autonomous solely because its contract exists or because a unit suite is green. The claim requires executable evidence for the relevant path and preserved architectural boundaries.

## Budgeting acceptance threshold

ELO is considered capable of autonomous governed budgeting only when all budgeting rows required for the requested class of quotation are `PASS`, including:

- requirement normalization;
- model/base selection;
- excess/delta calculation;
- quantity calculation;
- composition;
- cost/pricing provenance;
- labor;
- logistics;
- indirects;
- PTS reconciliation;
- scenario/sensitivity;
- uncertainty/gap handling;
- recommendation versus authorization;
- budget × actual;
- learning provenance.

A missing material input must produce `GAP` and/or a governed follow-up, never a fabricated value.
