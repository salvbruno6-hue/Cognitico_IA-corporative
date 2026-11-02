# ELO Objective Continuity — Governed Activation Sequence

Status: PREPARED / NOT LIVE
Date: 2026-11-02
Related: #1137, #1143, #1145, PRs #1135, #1142, #1146
Owners: ELO Governance / elo-authz / strategic-objective-domain / Objective Continuity

## Purpose

Close the activation path from the permanent ELO purpose anchor to a real resumable Objective without creating state, authority or permission by convention.

The target chain is:

```text
ELO mission
  -> ELO-OBJ-ROOT-001
  -> persisted strategic Objective
  -> elo-authz authorization
  -> Objective Continuity checkpoint
  -> next_trigger + next_elo_prompt
  -> bounded replay
  -> evidence/progress
  -> CONTINUE | CORRECT | REPLAN | ESCALATE | COMPLETE
```

## Verified state on 2026-11-02

### GitHub canon

- Objective Continuity architecture is reconciled: ELO Cognitivo decides, ELO Web is runtime, Supabase persists, elo-authz authorizes.
- The Web Cognitive Core owns continuity decision policy; the checkpoint adapter owns persistence/CAS.
- `prefinalize` requires a strategic Objective registry row before a checkpoint can be created.
- continuation grants are resource-bound and tenant-bound in the canonical source.
- `authorize_strategic_write` is implemented in GitHub canon with tenant scope, action/resource binding, capability verification and short authorization receipt.
- `PCP_ADMIN` drift remediation is prepared and canonicalized as a non-live candidate.

### Supabase live

- `elo_strategic_objectives`, `elo_strategic_key_results` and `elo_strategic_kr_snapshot_bindings` are absent.
- active Objective Continuity checkpoints: 0.
- active authorization grants: 0.
- live `elo-authz` is version 15 and predates the canonical strategic-write extension and the later continuation tenant/resource hardening.
- active capability catalog contains `ADMIN`, `CANONICAL_WRITE`, `APPROVE`, `PROPOSE`, `REVIEW`.
- live `CANONICAL_ADMIN` has zero material role-capability assignments, while the canonical baseline grants it the baseline capability set.

## Activation order

The order is mandatory. A later step must not be executed to compensate for an earlier missing authority.

### Gate 1 — Deploy canonical `elo-authz`

Deploy the exact `main` implementation of `supabase/functions/elo-authz` through the repository's governed manual deployment path.

Required evidence after deployment:

- live source contains `authorize_strategic_write`;
- live source includes the strategic action mapping for `PROPOSE`, `REVIEW`, `APPROVE`, `CANONICAL_WRITE`;
- live continuation lookup binds `resource_id` and `tenant_id`;
- JWT verification remains enabled;
- deployment source corresponds to the intended `main` commit.

This deployment requires the workflow's explicit deployment confirmation. A conversational instruction is not substituted for that control.

### Gate 2 — Recover the canonical administrative baseline

The verified drift `CANONICAL_ADMIN -> zero capabilities` creates an authorization bootstrap deadlock because critical structural actions require both the canonical role and its material capability.

Recovery must use the prepared candidate:

`docs/implementation/sql/ELO_AUTHZ_CANONICAL_ADMIN_BASELINE_RECOVERY_CANDIDATE.sql`

It restores only the capability set materially defined by the canonical authorization baseline:

- `READ`;
- `ADMIN`;
- `CANONICAL_WRITE`;
- `APPROVE`.

It must not assign `PROPOSE` or `REVIEW`, and it must not invent a role/capability.

Promotion/application requires an explicit governed production permission step. Technical service-role/database access is not authorization evidence.

### Gate 3 — Apply authorization drift remediation

Promote/apply the already-reviewed `PCP_ADMIN` debt resolution only after re-reading the exact live graph.

Required precondition:

- exact equality with the embedded 38-policy snapshot, including schema/table/policy/command/permissiveness/roles/USING/WITH CHECK;
- expected 38 policies / 50 occurrences;
- expected function consumer;
- no additional consumer.

Required result:

- `elo_private.has_capability()` returns to explicit material capability semantics;
- `has_admin_role()` is the bounded database administrative-role predicate;
- no RLS reference to orphan `PCP_ADMIN` remains;
- `lista_mae_guard()` no longer uses `current_user` as caller evidence inside `SECURITY DEFINER`.

### Gate 4 — Provision the strategic owner schema

Execute #1137 only after Gates 1–3 are verified.

Order:

1. Objective/KR owner schema;
2. measurement binding schema after the Objective/KR owner exists.

After schema application, prove:

- RLS/grants/triggers/constraints match the approved candidates;
- no productive Objective/KR row was implicitly inserted;
- service role remains persistence transport, not authorization authority.

### Gate 5 — Explicitly assign delegated strategic capability

A productive Objective proposal requires a registered operator with:

- active canonical identity;
- active ELO session;
- `ENTERPRISE/<tenant>` scope;
- explicit `PROPOSE` capability on an active role.

`PROPOSE`, `REVIEW` and `APPROVE` are delegated capabilities. This activation sequence does not choose recipients or assign them automatically.

### Gate 6 — Materialize the first operational Objective

The first operational Objective must be derived from `ELO-OBJ-ROOT-001`, backed by evidence and persisted through the governed strategic writer using an `elo-authz` receipt.

It must not be created in the continuity checkpoint table first.

Required provenance:

- parent/root reference to `ELO-OBJ-ROOT-001`;
- tenant;
- objective identity/title;
- evidence refs;
- authorization ref;
- state/status compatible with the strategic domain contract.

### Gate 7 — Bootstrap Objective Continuity

Only after the Objective exists:

1. obtain canonical continuation authorization for `continue_objective:<objective_id>`;
2. create/resume the workstream through the canonical runtime;
3. persist checkpoint with CAS/state version;
4. persist `next_trigger` and `next_elo_prompt` when continuation is allowed;
5. re-read checkpoint and authorization evidence.

No automation text or conversational memory is a checkpoint.

### Gate 8 — Run the first real replay

The next ChatGPT wake-up must read the live store and replay exactly one persisted handoff.

No-progress handling remains:

```text
CONTINUE -> CORRECT -> REPLAN -> ESCALATE
```

Terminal states clear the next handoff.

## Completion definition

The capability is **constructed** when the code/contracts/candidates and ordered activation gates are canonical and validated.

The capability is **live-operational** only when all eight gates have runtime evidence.

Until production authorization for deployment/schema/permission changes is supplied through the required governance controls, the correct runtime state remains fail-closed. No checkpoint should be fabricated merely to make the automation appear active.
