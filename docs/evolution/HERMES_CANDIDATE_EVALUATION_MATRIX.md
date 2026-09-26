# ELO — Hermes Candidate Evaluation Matrix

**Status:** CONTROLLED FUNCTIONAL EVIDENCE ACCEPTED  
**Base:** `main` @ `a1b651d9d9f377d706f99247d184d7e732a4e253`  
**Rule:** registration is not promotion; every candidate remains candidate-only until measured, repeatable evidence passes Evolution Gate and explicit ELO governance authorizes implementation.

| Candidate | Existing ELO owner | Primary measurable metric | Direction | Required evidence | Main boundary |
|---|---|---|---|---|---|
| EXT-CONTEXTREF-HERMES | ELO Context | reference resolution accuracy | maximize | provenance + bounded resolution | no context authority |
| EXT-CHECKPOINT-HERMES | ELO State Recovery | unsafe replay block rate | maximize | stale-checkpoint version guard + ordinary recovery integrity | no second state authority |
| EXT-HOOK-HERMES | ELO Workflow/Automation | guardrail interception coverage | maximize | lifecycle evidence + no bypass | no execution authority |
| EXT-ROUTE-HERMES | ELO Model/Tool Routing | successful policy-routed execution rate | maximize | fallback/credential evidence | no routing authority |
| EXT-PROFILE-HERMES | ELO Agent Context & Delegation | profile isolation compliance | maximize | isolation + provenance | no shared-state mutation |
| EXT-BATCH-HERMES | ELO Evaluation & Learning | valid evaluation throughput | maximize | batch provenance + bounded intake | no automatic promotion |
| EXT-MEMPROVIDER-HERMES | ELO Memory | evidence retrieval precision | maximize | provider provenance + digest | no memory authority |
| EXT-LEARN-HERMES | ELO Knowledge & Skills | validated skill admission precision | maximize | source provenance + governance | no autonomous skill promotion |
| EXT-LEARNING-GRAPH-HERMES | ELO Evolution Memory | evidence-linked relation validity | maximize | relation provenance | graph is not authority |
| EXT-CONTEXT-PLUGIN-HERMES | ELO Context | context task success rate | maximize | adapter compatibility | existing Context remains authority |
| EXT-WORKTREE-HERMES | ELO Forge | isolated workspace integrity | maximize | isolation + merge boundary | no merge authority |
| EXT-MULTIAGENT-HERMES | ELO Agent Delegation | delegated-task completion under authority constraints | maximize | child-agent provenance + bounded scope | no authority transfer |
| EXT-CRON-HERMES | ELO Workflow/Automation | authorized scheduled execution rate | maximize | identity + tenant + authorization + idempotency | scheduler cannot bypass governance |

## Mandatory evaluation sequence

`candidate → bounded adaptation → baseline → controlled test → measured gain → regression check → repeatability → Evolution Gate → ELO Review`

### Decision semantics

- `REJECT`: boundary violation or regression.
- `RETEST`: insufficient or non-repeatable gain.
- `READY_FOR_ELO_REVIEW`: technical evidence passed; governance decision remains.
- `IMPLEMENTATION_AUTHORIZED`: explicit ELO authorization exists; canonical mutation is still separate.
- No candidate may set `canonical_mutation=True` through this evaluation loop.

## Evidence requirements

Each evaluation must record:

1. candidate ID;
2. existing ELO owner;
3. baseline metric;
4. adapted metric;
5. explicit metric direction;
6. regression set;
7. repeatability result;
8. provenance;
9. governance boundary result;
10. final implementation-loop decision.

## Initial execution order

1. EXT-CONTEXT-PLUGIN-HERMES
2. EXT-WORKTREE-HERMES
3. EXT-MULTIAGENT-HERMES
4. EXT-CRON-HERMES
5. EXT-MEMPROVIDER-HERMES
6. EXT-ROUTE-HERMES
7. EXT-PROFILE-HERMES
8. EXT-BATCH-HERMES
9. EXT-LEARN-HERMES
10. EXT-LEARNING-GRAPH-HERMES
11. EXT-CONTEXTREF-HERMES
12. EXT-CHECKPOINT-HERMES
13. EXT-HOOK-HERMES

The order is an execution sequence, not a quality ranking.


## Controlled validation results — 2026-09-26

| Candidate | Current evidence | Functional attribution | Symbiont handoff |
|---|---|---|---|
| EXT-CONTEXT-PLUGIN-HERMES | controlled task gain 0.00 → 1.00 | candidate-attributed | eligible for governed handoff |
| EXT-WORKTREE-HERMES | collision-free concurrent task rate 0.00 → 1.00 | candidate-attributed controlled gain | eligible for governed handoff |
| EXT-MULTIAGENT-HERMES | context isolation rate 0.00 → 1.00 | candidate-attributed controlled gain | eligible for governed handoff |
| EXT-CRON-HERMES | bounded schedule contract | boundary-attributed | RETEST_FUNCTIONAL_VALUE |
| EXT-MEMPROVIDER-HERMES | bounded retrieval contract | boundary-attributed | RETEST_FUNCTIONAL_VALUE |
| EXT-ROUTE-HERMES | bounded routing-plan contract | boundary-attributed | RETEST_FUNCTIONAL_VALUE |
| EXT-PROFILE-HERMES | bounded profile isolation | boundary-attributed | RETEST_FUNCTIONAL_VALUE |
| EXT-BATCH-HERMES | bounded batch intake | boundary-attributed | RETEST_FUNCTIONAL_VALUE |
| EXT-LEARN-HERMES | candidate skill admission contract | boundary-attributed | RETEST_FUNCTIONAL_VALUE |
| EXT-LEARNING-GRAPH-HERMES | baseline 1.00 → adapted 1.00 | no incremental gain | RETEST_FUNCTIONAL_VALUE |
| EXT-CONTEXTREF-HERMES | baseline 1.00 → adapted 1.00 | no incremental gain | RETEST_FUNCTIONAL_VALUE |
| EXT-CHECKPOINT-HERMES | recovery remains 1.00 → 1.00; stale-replay block 0.00 → 1.00 | candidate-attributed controlled gain | eligible for governed handoff |
| EXT-HOOK-HERMES | controlled lifecycle gain 0.00 → 1.00 | candidate-attributed | eligible for governed handoff |

**Interpretation:** contract/boundary integrity is not counted as functional value. Candidate-attributed functional gain is sufficient for the existing Symbiont implementation loop to advance to governed review. For EXT-CHECKPOINT-HERMES, ordinary recovery remains supplied by the existing ELO State Recovery owner; the candidate-specific gain is the independently measured stale-checkpoint replay guard.
