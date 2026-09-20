# ELO — Hermes Candidate Evaluation Matrix

**Status:** CONTROLLED VALIDATION PLAN  
**Base:** `main` @ `a1b651d9d9f377d706f99247d184d7e732a4e253`  
**Rule:** registration is not promotion; every candidate remains candidate-only until measured, repeatable evidence passes Evolution Gate and explicit ELO governance authorizes implementation.

| Candidate | Existing ELO owner | Primary measurable metric | Direction | Required evidence | Main boundary |
|---|---|---|---|---|---|
| EXT-CONTEXTREF-HERMES | ELO Context | reference resolution accuracy | maximize | provenance + bounded resolution | no context authority |
| EXT-CHECKPOINT-HERMES | ELO State Recovery | recovery integrity rate | maximize | deterministic restore/recovery | no second state authority |
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
