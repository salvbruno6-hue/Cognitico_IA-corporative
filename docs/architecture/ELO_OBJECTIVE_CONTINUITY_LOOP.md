# ELO Objective Continuity Loop

## Purpose

Keep ELO persistent on a governed objective across repeated executions, chat/process restarts and repetitive workstreams without creating a second objective authority, supervisor, scheduler or execution engine.

## Canonical ownership

Objective Continuity separates **semantic authority**, **production runtime**, **durable checkpoint persistence**, **authorization** and **reference implementations**. These responsibilities must not be collapsed into one component.

- Strategic purpose/root anchor: `ELO-OBJ-ROOT-001` in `00-enterprise-manifest/02_Objetivos.md`.
- Strategic objective identity and approved targets: existing OKR contracts/repository under `strategic-objective-domain`.
- Cognitive supervision and next-action policy: ELO Cognitivo.
- Production runtime: `apps/elo-web` / ELO Web.
- Durable production checkpoint store: `public.elo_objective_continuity_checkpoints` in the canonical Supabase project.
- Authorization: `elo-authz`; persistence credentials or service-role access never grant objective/action authority.
- Replanning: existing ELO-010 semantics / governed decision path.
- Learning: Symbiont + Evolution Gate + Governed Learning.
- Scheduling/wakeup: external ChatGPT automation or future canonical scheduler; scheduling does not become objective authority.

### Python/Symbiont boundary

`src/elo/cognitive/objective_continuity.py` and `SymbiontExecutionStore` remain executable canonical evidence for Objective Continuity semantics, restart/replay behavior, no-progress progression and stale-checkpoint protection. They may support non-Web/runtime validation contexts.

They are **not a production dependency of ELO Web** and must not be reintroduced as an external runtime service merely to execute Objective Continuity. The production ELO Web implementation must remain behaviorally compatible with the canonical semantics and must be protected by parity/regression tests.

`public.elo_objective_continuity_checkpoints` is a persistence owner for the production checkpoint projection. It is not a second cognitive authority, Objective registry, scheduler, authorization source or execution engine.

## Stable binding

Each workstream is durably bound by:

```text
tenant_id + objective_id + workstream_id
```

The same objective/workstream therefore resumes the same production checkpoint after a new chat, process restart or scheduled wakeup.

For the Python reference implementation, the same binding is deterministically projected to `objective_execution_id`; this deterministic ID is an implementation detail of that runtime and does not replace the production composite identity above.

## Loop

```text
PURPOSE / ROOT OBJECTIVE
  -> GOVERNED OPERATIONAL OBJECTIVE
  -> WORKSTREAM
  -> CHECKPOINT
  -> EXECUTE ONE BOUNDED CYCLE
  -> RECORD EVIDENCE + PROGRESS TOKEN
  -> ELO COGNITIVE DECISION
  -> CONTINUE | CORRECT | REPLAN | ESCALATE | COMPLETE
  -> PERSIST CHECKPOINT WITH CAS(state_version)
  -> PERSIST NEXT_TRIGGER + NEXT_ELO_PROMPT WHEN CONTINUATION IS ALLOWED
  -> NEXT WAKEUP / NEW CHAT / SAME CHAT
```

The persistence module may store a decision already produced by the cognitive authority, but it must not become an independent decision authority.

## Progress discipline

A cycle must provide an objective-relevant `progress_token` and evidence. Repeating the same token means the method did not create measurable progress.

Default behavior:

| repeated no-progress streak | decision |
|---:|---|
| 0 | `CONTINUE` |
| 1 | `CORRECT` |
| 2-3 | `REPLAN` |
| 4+ | `ESCALATE` |

Progress resets the streak to zero. High/critical risk, missing authority, scope expansion or exhausted autonomy budget also escalate.

Production and reference implementations must preserve this semantic table unless a later governed decision changes the policy centrally. A persistence adapter must never introduce its own thresholds silently.

## Idempotency and replay protection

Every production cycle is bound to the persistent `state_version`. A stale checkpoint cannot be replayed after the state advances.

The production store must use compare-and-set semantics when advancing an existing checkpoint. A successful write must be re-read before a next handoff is exposed.

`next_trigger` and `next_elo_prompt` are derived persisted state in the **same checkpoint**. Their binding must match:

- `objective_id`;
- `workstream_id`;
- `checkpoint_version = state_version`;
- `progress_token = last_progress_token`;
- `next_action`.

If any binding is absent or inconsistent, the wakeup fails closed and must not reconstruct a handoff from chat memory or automation text.

Reference-runtime deterministic operation keys remain evidence for the same idempotency principle; they are not a second production state owner.

## Authorization boundary

A checkpoint does not authorize its own continuation.

Before a production replay, `elo-authz` must prove an explicit, unexpired and non-revoked grant bound to:

```text
continue_objective:<objective_id>
```

Conversational approval, a persisted prompt, service-role credentials, GitHub write access or the existence of `ELO-OBJ-ROOT-001` do not substitute for canonical authorization.

If authorization cannot be proven, the cycle performs no state mutation.

## Root objective relationship

`ELO-OBJ-ROOT-001` is a permanent strategic anchor for why governed objectives exist. It is not itself an infinite execution checkpoint.

An operational objective may derive from it only when the operational objective has its own:

- tenant/scope;
- evidence;
- bounded workstream;
- acceptance/completion criteria;
- authorization boundary;
- persistent checkpoint lifecycle.

Changing the root purpose requires governance outside Objective Continuity.

## Repetitive flows

A repetitive flow is valid only when each repetition advances an objective-relevant marker, for example:

```text
batch:1 -> batch:2 -> batch:3
validated_items:10 -> 20 -> 30
remaining_gaps:7 -> 5 -> 2 -> 0
```

Repeating `batch:1 -> batch:1 -> batch:1` is not treated as persistence; it is treated as stagnation and forces correction/replanning/escalation.

## ChatGPT automation boundary

ChatGPT automation may wake the objective loop periodically. It must:

1. read the real production checkpoint store at every wakeup;
2. return idle without creating state when there is no ACTIVE checkpoint;
3. validate persisted `next_trigger` and `next_elo_prompt` against the same checkpoint;
4. validate canonical `elo-authz` continuation authority;
5. perform at most one bounded replay;
6. record objective-relevant evidence/progress;
7. persist the next checkpoint with CAS and re-read it;
8. stop notifying when there is no material change;
9. escalate when the loop requires authority or a root-objective change.

Automation may adapt operational method, priority, decomposition and next action only inside approved scope. It may not autonomously change ELO purpose, identity, governance boundaries, human-approved strategic target or action authority.

Automation text and conversational memory are never checkpoints.

## Production implementation rule

ELO Web may reconstruct Objective Continuity for the Web runtime, as permitted by the ELO Web decoupling decision, but the reconstruction must preserve the canonical semantic contract.

The production implementation must keep these concerns separated:

```text
ELO Cognitivo / governed decision
        -> Objective Continuity decision result
        -> persistence adapter/store
        -> persisted checkpoint + handoff
```

A module whose responsibility is checkpoint persistence must not independently become the cognitive decision owner merely because it has access to `no_progress_streak`, `risk_level` or `max_cycles`.

## Test acceptance criteria

The capability is accepted only if executable tests prove:

- checkpoint survives independent requests/process restarts in the production persistence boundary;
- no-progress streak survives restart;
- stagnation transitions through `CORRECT -> REPLAN -> ESCALATE`;
- objective-relevant progress resets stagnation;
- repetitive flow reaches completion;
- stale checkpoint replay is blocked by `state_version` CAS;
- two workstreams under the same objective remain isolated;
- a multi-cycle flow can restart after every cycle and still reach completion;
- production Web decision semantics remain in parity with the canonical Objective Continuity contract;
- persistence cannot silently choose a different decision policy;
- `ESCALATE`, `COMPLETE` or `human_required=true` persist no next trigger/prompt;
- invalid persisted handoff fails closed;
- missing/expired/revoked continuation authority performs no write;
- the root objective cannot be used as authorization or as an unbounded checkpoint.

## Current production status

As of 2026-11-02:

- ELO Web is the official production runtime;
- `public.elo_objective_continuity_checkpoints` is present in the canonical Supabase project;
- the live checkpoint table currently has no objective state;
- no current authorization grant exists for autonomous objective continuation;
- `ELO-OBJ-ROOT-001` is canonical in GitHub;
- strategic Objective/KR persistence remains a separate boundary and must not be fabricated inside the checkpoint store.

This status describes observed runtime state; it does not itself authorize schema, identity, grant or objective-data mutation.
