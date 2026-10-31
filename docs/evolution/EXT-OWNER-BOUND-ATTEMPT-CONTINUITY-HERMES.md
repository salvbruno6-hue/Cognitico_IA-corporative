# EXT-OWNER-BOUND-ATTEMPT-CONTINUITY-HERMES

Status: CANDIDATE — not promoted until CI, review and Evolution Gate pass.

## Discovery

Hermes hardening observed on 2026-10-28/29 preserves an already-admitted attempt across transient runtime/transport loss while keeping authorization or unsafe conditions non-retryable. The 2026-10-29 process-owner work further strengthens child/process ownership, bounded recovery and owner-death cleanup.

## Existing ELO owner

This is a refinement of the canonical `ELO ExecutionBoundary` and ELO-156 operational resilience. It is not a new Retry Engine, Router, Runtime Manager, Memory owner or authorization authority.

## Candidate invariant

`existing admission + attempt identity + owner identity + failure classification + bounded retry budget -> retry same attempt only for transient failure`

Governance refusal is terminal for continuity. Retry cannot create, refresh, broaden or infer authorization.

## Scope

The candidate classifier:

- requires request, attempt, owner and authorization identity;
- permits continuity only for declared transient transport/owner lifecycle conditions;
- preserves the same attempt and existing authorization rather than minting a new one;
- stops on authorization, scope or evidence refusal;
- stops after a bounded retry budget;
- fails closed for malformed controls.

It does not dispatch work, sleep/back off, execute Hermes, mutate business data, alter routing, or prove production resilience.

## Relationship to existing evidence

ELO-156 already proves deterministic retry/degradation semantics but models attempts independently. This candidate closes the narrower repository-local gap: continuity must preserve the identity and authorization of the admitted attempt and must never reinterpret a governance refusal as transient infrastructure failure.

## Promotion evidence required

1. focused tests pass;
2. repository behavioral/regression gates pass;
3. independent review has no unresolved findings;
4. Evolution Gate passes;
5. no duplicate owner or parallel authority is introduced.

Production/runtime behavior remains INDETERMINATE until directly observed.